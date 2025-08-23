#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selective Publisher
- Liest publish.yml|yaml aus dem Repo-Root
- Ermittelt alle Einträge mit build: true -> get_publish_list()
- Bereitet Umgebung vor (PyYAML, optional Pandoc/LaTeX & Emoji-Fonts) -> prepareYAML(), prepare_publishing()
- Baut PDFs für 'file' und 'folder' -> build_pdf()
- Setzt nach erfolgreichem Build das Flag per reset-publish-flag.py zurück -> main()

Aufrufbeispiele:
  python .github/tools/publishing/publisher.py
  python .github/tools/publishing/publisher.py --manifest publish.yml --use-summary
  python .github/tools/publishing/publisher.py --no-apt --only-prepare

Optionen siehe argparse unten.
"""

from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import pathlib
import platform
from typing import Any, Dict, List, Optional, Tuple

# ------------------------------- Utils ------------------------------------- #


def _run(
    cmd: List[str],
    check: bool = True,
    capture: bool = False,
    env: Optional[Dict[str, str]] = None,
) -> subprocess.CompletedProcess:
    kwargs: Dict[str, Any] = {"text": True}
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    if env:
        kwargs["env"] = {**os.environ, **env}
    print("→", " ".join(cmd))
    cp = subprocess.run(cmd, **kwargs)
    if check and cp.returncode != 0:
        if capture:
            print(cp.stdout or "", file=sys.stdout)
            print(cp.stderr or "", file=sys.stderr)
        raise subprocess.CalledProcessError(cp.returncode, cmd)
    return cp


def _which(name: str) -> Optional[str]:
    return shutil.which(name)


def _is_debian_like() -> bool:
    return pathlib.Path("/etc/debian_version").exists()


def _ensure_dir(path: str) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def _download(url: str, dest: str) -> None:
    import urllib.request

    print(f"↓ Download {url} -> {dest}")
    pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        f.write(r.read())


# ----------------------------- YAML Helpers -------------------------------- #


def prepareYAML() -> None:
    """Installiert PyYAML, falls nicht vorhanden."""
    try:
        import yaml  # noqa: F401

        return
    except Exception:
        pass
    py = sys.executable or "python"
    _run([py, "-m", "pip", "install", "--upgrade", "pip"], check=False)
    _run([py, "-m", "pip", "install", "pyyaml"])


def _find_manifest(explicit: Optional[str] = None) -> str:
    if explicit and os.path.exists(explicit):
        return explicit
    for name in ("publish.yml", "publish.yaml"):
        if os.path.exists(name):
            return name
    print("ERROR: publish.yml|yaml nicht im Repo-Root gefunden.", file=sys.stderr)
    sys.exit(2)


def _load_yaml(path: str) -> Dict[str, Any]:
    import yaml

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if "publish" not in data or not isinstance(data["publish"], list):
        print(
            "ERROR: Ungültiges Manifest – Top-Level 'publish' (Liste) fehlt.",
            file=sys.stderr,
        )
        sys.exit(3)
    return data


def _save_yaml(path: str, data: Dict[str, Any]) -> None:
    import yaml

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


# --------------------------- Public API (A) -------------------------------- #


def get_publish_list(manifest_path: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Liest publish.yml und liefert alle Einträge mit build: true als Liste
    [{path, out, type}, ...]
    """
    prepareYAML()
    mpath = _find_manifest(manifest_path)
    data = _load_yaml(mpath)
    res: List[Dict[str, str]] = []
    for e in data.get("publish", []):
        if e.get("build"):
            res.append(
                {
                    "path": str(e.get("path", "")),
                    "out": str(e.get("out", "")),
                    "type": str(e.get("type", "file")),
                }
            )
    return res


# ---------------------- Environment Prep (B / B.1) ------------------------- #


def prepare_publishing(no_apt: bool = False) -> None:
    """
    Installiert die System- und Python-Abhängigkeiten für den PDF-Build.
    - PyYAML (via prepareYAML)
    - Pandoc + LaTeX (apt-get auf Debian/Ubuntu)
    - OpenMoji Font + fc-cache
    - latex-emoji.lua (Pandoc Lua-Filter)
    """
    prepareYAML()  # B.1

    # Pandoc vorhanden?
    have_pandoc = _which("pandoc") is not None
    have_lualatex = _which("lualatex") is not None

    if not (have_pandoc and have_lualatex):
        if no_apt:
            print(
                "WARN: pandoc/lualatex fehlen, --no-apt gesetzt. Bitte vorinstallieren.",
                file=sys.stderr,
            )
        elif _is_debian_like():
            sudo = _which("sudo")
            prefix = [sudo] if sudo else []
            _run(prefix + ["apt-get", "update"])
            _run(
                prefix
                + [
                    "apt-get",
                    "install",
                    "-y",
                    "pandoc",
                    "texlive-luatex",
                    "texlive-fonts-recommended",
                    "texlive-latex-extra",
                    "texlive-lang-cjk",
                    "fonts-dejavu-core",
                    "wget",
                ]
            )
        else:
            print(
                "WARN: Nicht-Debian System erkannt – installiere pandoc/LaTeX manuell.",
                file=sys.stderr,
            )

    # OpenMoji-Font & fc-cache
    font_dir = "/usr/share/fonts/truetype/openmoji"
    font_path = os.path.join(font_dir, "OpenMoji-black-glyf.ttf")
    if not os.path.exists(font_path):
        try:
            sudo = _which("sudo")
            prefix = [sudo] if (sudo and not os.path.exists(font_dir)) else []
            if prefix:
                _run(prefix + ["mkdir", "-p", font_dir])
            else:
                _ensure_dir(font_dir)
            url = "https://github.com/hfg-gmuend/openmoji/raw/master/font/OpenMoji-black-glyf/OpenMoji-black-glyf.ttf"
            tmp_dest = os.path.join("/tmp", "OpenMoji-black-glyf.ttf")
            _download(url, tmp_dest)
            cp_cmd = (
                (prefix + ["cp", tmp_dest, font_path])
                if prefix
                else ["cp", tmp_dest, font_path]
            )
            _run(cp_cmd)
            if _which("fc-cache"):
                _run(["fc-cache", "-f", "-v"], check=False)
        except Exception as e:
            print(f"WARN: Konnte OpenMoji nicht installieren: {e}", file=sys.stderr)

    # latex-emoji.lua Filter
    if not os.path.exists("latex-emoji.lua"):
        try:
            url = "https://gist.githubusercontent.com/zr-tex8r/a5410ad20ab291c390884b960c900537/raw/latex-emoji.lua"
            _download(url, "latex-emoji.lua")
        except Exception as e:
            print(f"WARN: Konnte latex-emoji.lua nicht laden: {e}", file=sys.stderr)


# --------------------------- PDF Build (C) --------------------------------- #

_SUBS = {  # wie im bestehenden Workflow: tiefgestellte Ziffern
    "₀": "$_0$",
    "₁": "$_1$",
    "₂": "$_2$",
    "₃": "$_3$",
    "₄": "$_4$",
    "₅": "$_5$",
    "₆": "$_6$",
    "₇": "$_7$",
    "₈": "$_8$",
    "₉": "$_9$",
}


def _normalize_md(text: str) -> str:
    return "".join(_SUBS.get(ch, ch) for ch in text)


def _get_book_title(folder: str) -> Optional[str]:
    try:
        with open("book.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        root = data.get("root", "") or ""
        if root.startswith("./"):
            root = root[2:]
        if os.path.normpath(root) == os.path.normpath(folder):
            return data.get("title")
    except Exception:
        pass
    return None


def _run_pandoc(
    md_path: str, pdf_out: str, add_toc: bool = False, title: Optional[str] = None
) -> None:
    _ensure_dir(os.path.dirname(pdf_out))
    cmd = [
        "pandoc",
        md_path,
        "-o",
        pdf_out,
        "--pdf-engine",
        "lualatex",
        "-V",
        "mainfont=DejaVu Sans",
        "-V",
        "monofont=DejaVu Sans Mono",
        "-V",
        "emoji=OpenMoji-black-glyf.ttf",
        "--lua-filter=latex-emoji.lua",
        "-M",
        "emojifont=OpenMoji-black-glyf.ttf",
        "-M",
        "color=false",
    ]
    if add_toc:
        cmd.append("--toc")
    if title:
        cmd.extend(["-V", f"title={title}"])
    _run(cmd)


def _extract_md_paths_from_summary(folder: str) -> List[str]:
    summary_path = os.path.join(folder, "summary.md")
    if not os.path.exists(summary_path):
        return []
    paths: List[str] = []
    with open(summary_path, "r", encoding="utf-8") as f:
        for line in f:
            for match in re.findall(r"\(([^)]+\.md)\)", line):
                if not match.startswith(("http://", "https://")):
                    paths.append(os.path.normpath(os.path.join(folder, match)))
    return paths


def _collect_folder_md(folder: str, use_summary: bool) -> List[str]:
    if use_summary:
        md_files = _extract_md_paths_from_summary(folder)
        if md_files:
            return md_files
    # Fallback: alle .md rekursiv, README bevorzugt
    md_files: List[str] = []
    for root, _, files in os.walk(folder):
        for fname in sorted(files):
            if fname.lower().endswith((".md", ".markdown")):
                full = os.path.join(root, fname)
                if fname.lower() == "readme.md":
                    md_files.insert(0, full)
                else:
                    md_files.append(full)
    return md_files


def _concat_md(files: List[str]) -> str:
    parts: List[str] = []
    for p in files:
        try:
            with open(p, "r", encoding="utf-8") as f:
                parts.append(_normalize_md(f.read()))
        except Exception as e:
            print(f"WARN: Konnte {p} nicht lesen: {e}", file=sys.stderr)
    return "\n\n\\newpage\n\n".join(parts)


def _convert_single_file(md_file: str, pdf_out: str) -> None:
    with open(md_file, "r", encoding="utf-8") as f:
        content = _normalize_md(f.read())
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_md = tmp.name
    try:
        _run_pandoc(tmp_md, pdf_out)
    finally:
        try:
            os.unlink(tmp_md)
        except OSError:
            pass


def _convert_folder(folder: str, pdf_out: str, use_summary: bool) -> None:
    md_files = _collect_folder_md(folder, use_summary=use_summary)
    if not md_files:
        print(f"ℹ Keine Markdown-Dateien in {folder} – übersprungen.")
        return
    combined = _concat_md(md_files)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined)
        tmp_md = tmp.name
    try:
        title = _get_book_title(folder)
        _run_pandoc(tmp_md, pdf_out, add_toc=True, title=title)
    finally:
        try:
            os.unlink(tmp_md)
        except OSError:
            pass


def build_pdf(
    path: str,
    out: str,
    typ: str,
    use_summary: bool = False,
    publish_dir: str = "publish",
) -> bool:
    """
    Baut ein PDF gemäß Typ ('file'/'folder'). Gibt True bei Erfolg zurück.
    """
    pdf_out = os.path.join(publish_dir, out)
    print(f"✔ Building {pdf_out} from {path} (type={typ})")
    _ensure_dir(publish_dir)

    # Typ autodetektion, falls leer/ungewohnt
    _typ = (typ or "").lower().strip()
    if not _typ or _typ not in {"file", "folder"}:
        if os.path.isdir(path):
            _typ = "folder"
        else:
            _typ = "file"

    try:
        if _typ == "file":
            _convert_single_file(path, pdf_out)
        elif _typ == "folder":
            _convert_folder(path, pdf_out, use_summary=use_summary)
        else:
            print(f"⚠ Unbekannter type='{typ}' – übersprungen.")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(
            f"ERROR: Pandoc/LaTeX Build fehlgeschlagen (rc={e.returncode}).",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"ERROR: Build-Fehler: {e}", file=sys.stderr)
        return False


# -------------------------------- Main (D) --------------------------------- #


def _write_github_outputs(built: List[str], failed: List[str], manifest: str) -> None:
    gh_out = os.getenv("GITHUB_OUTPUT")
    if gh_out:
        try:
            with open(gh_out, "a", encoding="utf-8") as f:
                f.write(f"built_count={len(built)}\n")
                f.write(f"built_files={json.dumps(built, ensure_ascii=False)}\n")
                f.write(f"failed_files={json.dumps(failed, ensure_ascii=False)}\n")
                f.write(f"manifest={manifest}\n")
        except Exception as e:
            print(f"WARN: Konnte GITHUB_OUTPUT nicht schreiben: {e}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description="Selective publisher für publish.yml")
    ap.add_argument("--manifest", help="Pfad zu publish.yml|yaml (Default: Root)")
    ap.add_argument(
        "--use-summary",
        action="store_true",
        help="Ordner über summary.md Reihenfolge bauen (falls vorhanden)",
    )
    ap.add_argument(
        "--no-apt", action="store_true", help="Keine apt-Installation versuchen"
    )
    ap.add_argument(
        "--only-prepare",
        action="store_true",
        help="Nur Umgebung vorbereiten und beenden",
    )
    ap.add_argument(
        "--reset-script",
        default=".github/tools/publishing/reset-publish-flag.py",
        help="Pfad zum Reset-Tool",
    )
    args = ap.parse_args()

    # B.1 + B
    prepare_publishing(no_apt=args.no_apt)
    if args.only - prepare:
        print("✔ Umgebung vorbereitet. (only-prepare)")
        return

    # A
    manifest = _find_manifest(args.manifest)
    targets = get_publish_list(manifest)

    if not targets:
        print("ℹ Keine zu publizierenden Einträge (build: true).")
        _write_github_outputs([], [], manifest)
        return

    built: List[str] = []
    failed: List[str] = []

    # C + Reset je nach Erfolg
    for entry in targets:
        path = entry["path"]
        out = entry["out"]
        typ = entry.get("type", "file")
        ok = build_pdf(path=path, out=out, typ=typ, use_summary=args.use_summary)
        if ok:
            built.append(out)
            # Reset publish-Flag (D) – nur bei Erfolg
            reset_tool = args.reset_script
            if os.path.exists(reset_tool):
                try:
                    _run(
                        [
                            sys.executable or "python",
                            reset_tool,
                            "--path",
                            path,
                            "--multi",
                        ],
                        check=True,
                    )
                except Exception as e:
                    print(
                        f"WARN: Konnte reset-publish-flag nicht aufrufen: {e}",
                        file=sys.stderr,
                    )
            else:
                # Fallback: direkt im Manifest auf false setzen
                try:
                    data = _load_yaml(manifest)
                    for e in data.get("publish", []):
                        if e.get("path") == path:
                            e["build"] = False
                    _save_yaml(manifest, data)
                except Exception as e:
                    print(
                        f"WARN: Konnte Manifest-Fallback-Reset nicht schreiben: {e}",
                        file=sys.stderr,
                    )
        else:
            failed.append(out)

    # Outputs
    print("::group::publisher.outputs")
    print(
        json.dumps(
            {
                "built_count": len(built),
                "built_files": built,
                "failed_files": failed,
                "manifest": manifest,
            },
            ensure_ascii=False,
        )
    )
    print("::endgroup::")

    _write_github_outputs(built, failed, manifest)

    # Exit-Code, wenn Builds fehlgeschlagen sind (aber nicht hart abbrechen, wenn ein Teil ok ist)
    if built and not failed:
        sys.exit(0)
    elif failed and not built:
        sys.exit(1)
    else:
        # Teilweise erfolgreich
        sys.exit(0)


if __name__ == "__main__":
    main()

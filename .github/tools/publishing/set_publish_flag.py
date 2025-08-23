#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setzt in publish.yaml/yml das build-Flag auf true, wenn der Commit relevante Pfade geändert hat.
Optional: setzt alle anderen Einträge auf false (--reset-others).
Nutzung:
  python .github/tools/publishing/set_publish_flag.py --commit <SHA> [--base <BASE_SHA>] [--branch <name>] [--reset-others] [--dry-run]

Typische Aufrufe in GitHub Actions:
  # Push: vergleiche "before" und "after"
  python .github/tools/publishing/set_publish_flag.py --commit "$GITHUB_SHA" --base "${{ github.event.before }}" --reset-others

  # PR: vergleiche Base- und Head-SHA
  python .github/tools/publishing/set_publish_flag.py --commit "${{ github.event.pull_request.head.sha }}" --base "${{ github.event.pull_request.base.sha }}" --reset-others
"""
import argparse
import json
import os
import posixpath
import subprocess
import sys
from typing import List, Dict, Any, Tuple

try:
    import yaml  # PyYAML
except ImportError:
    print(
        "ERROR: PyYAML nicht installiert. Bitte `pip install pyyaml` im Workflow ausführen.",
        file=sys.stderr,
    )
    sys.exit(2)


def run(cmd: List[str]) -> Tuple[int, str, str]:
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return p.returncode, out, err


def find_publish_file(explicit: str = None) -> str:
    if explicit and os.path.isfile(explicit):
        return explicit
    for name in ("publish.yaml", "publish.yml"):
        candidate = os.path.join(os.getcwd(), name)
        if os.path.isfile(candidate):
            return candidate
    print(
        "ERROR: publish.yaml oder publish.yml im Repo-Root nicht gefunden.",
        file=sys.stderr,
    )
    sys.exit(3)


def normalize_posix(path_str: str) -> str:
    # Git gibt immer forward slashes aus -> POSIX-Style beibehalten
    # Entferne führendes './' und normalisiere Mehrfach-Slashes.
    p = path_str.replace("\\", "/")
    p = p.lstrip("./")
    return posixpath.normpath(p)


def is_match(entry_path: str, entry_type: str, changed_file: str) -> bool:
    ep = normalize_posix(entry_path)
    cf = normalize_posix(changed_file)
    if entry_type == "folder":
        # Treffer, wenn Datei im Ordner (oder der Ordner selbst) liegt
        return cf == ep or cf.startswith(ep + "/")
    elif entry_type == "file":
        return cf == ep
    else:
        # "auto": heuristisch – Ordner wenn kein Punkt im letzten Segment und Pfad existiert/ist Dir,
        # sonst Datei. Fallback: Datei.
        last = posixpath.basename(ep)
        if os.path.isdir(ep) or (("." not in last) and not posixpath.splitext(last)[1]):
            return cf == ep or cf.startswith(ep + "/")
        return cf == ep


def git_changed_files(commit: str, base: str = None) -> List[str]:
    if base:
        code, out, err = run(["git", "diff", "--name-only", base, commit])
        ctx = f"{base}..{commit}"
    else:
        # Einzel-Commit
        code, out, err = run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit]
        )
        ctx = commit

    if code != 0:
        print(
            f"ERROR: Git-Aufruf fehlgeschlagen ({ctx}): {err.strip()}", file=sys.stderr
        )
        sys.exit(4)

    files = [normalize_posix(line) for line in out.splitlines() if line.strip()]
    return files


def load_publish(publish_path: str) -> Dict[str, Any]:
    with open(publish_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if "publish" not in data or not isinstance(data["publish"], list):
        print(
            "ERROR: Ungültiges publish.yaml-Format: Top-Level-Schlüssel 'publish' (Liste) fehlt.",
            file=sys.stderr,
        )
        sys.exit(5)
    return data


def save_publish(publish_path: str, data: Dict[str, Any]) -> None:
    # Hinweis: PyYAML formatiert neu; falls Format/Kommentare erhalten bleiben sollen -> ruamel.yaml verwenden.
    with open(publish_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def main():
    parser = argparse.ArgumentParser(
        description="Setzt build-Flags in publish.yaml basierend auf Git-Änderungen."
    )
    parser.add_argument(
        "--commit",
        default=os.getenv("GITHUB_SHA", "HEAD"),
        help="Ziel-Commit (default: GITHUB_SHA oder HEAD)",
    )
    parser.add_argument(
        "--base",
        help="Basis-Commit zum Vergleichen (z. B. github.event.before oder PR-Base-SHA)",
    )
    parser.add_argument("--branch", help="optionaler Branch-Name (nur Logging)")
    parser.add_argument(
        "--publish-file", help="Pfad zu publish.yaml/yml (default: Repo-Root)"
    )
    parser.add_argument(
        "--reset-others",
        action="store_true",
        help="Nicht betroffene Einträge explizit auf false setzen",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Nur anzeigen, keine Datei schreiben"
    )
    parser.add_argument("--debug", action="store_true", help="Debug-Ausgaben")
    args = parser.parse_args()

    publish_path = find_publish_file(args.publish_file)

    changed_files = git_changed_files(args.commit, args.base)
    if args.debug:
        print(f"[DEBUG] Changed files ({len(changed_files)}):")
        for c in changed_files:
            print(f"  - {c}")

    data = load_publish(publish_path)
    entries = data["publish"]

    touched_entries = []
    for idx, entry in enumerate(entries):
        ep = entry.get("path")
        etype = (entry.get("type") or "auto").lower()
        if not ep:
            print(
                f"WARNING: publish[{idx}] ohne 'path' – übersprungen.", file=sys.stderr
            )
            continue

        hit = any(is_match(ep, etype, cf) for cf in changed_files)

        # Baue altes/newes Flag
        old_build = bool(entry.get("build", False))
        new_build = True if hit else (False if args.reset_others else old_build)

        if old_build != new_build:
            entry["build"] = new_build
            touched_entries.append(
                {"path": ep, "type": etype, "from": old_build, "to": new_build}
            )
        else:
            # Stelle sicher, dass build-Schlüssel existiert
            entry["build"] = new_build

    # Outputs (für GitHub Actions)
    outputs = {
        "changed_files": changed_files,
        "modified_entries": touched_entries,
        "any_build_true": any(e.get("build", False) for e in entries),
    }

    # Schreiben
    if args.dry_run:
        print("[DRY-RUN] Änderungen würden geschrieben werden.")
    else:
        save_publish(publish_path, data)

    # Menschlich lesbares Log
    print(f"publish file: {publish_path}")
    print(
        f"commit: {args.commit}"
        + (f" | base: {args.base}" if args.base else "")
        + (f" | branch: {args.branch}" if args.branch else "")
    )
    if touched_entries:
        print("geänderte build-Flags:")
        for t in touched_entries:
            print(f"  - {t['path']} ({t['type']}): {t['from']} -> {t['to']}")
    else:
        print("keine build-Flag-Änderungen.")

    # Maschine-lesbar (JSON auf stdout ans Ende hängen, damit von anderen Steps geparst werden kann)
    print("::group::set_publish_flag.outputs")
    print(json.dumps(outputs, ensure_ascii=False))
    print("::endgroup::")

    # Zusätzlich GitHub-Outputs schreiben, falls verfügbar
    gh_out = os.getenv("GITHUB_OUTPUT")
    if gh_out:
        try:
            with open(gh_out, "a", encoding="utf-8") as f:
                f.write(
                    f"changed_files={json.dumps(changed_files, ensure_ascii=False)}\n"
                )
                f.write(
                    f"modified_entries={json.dumps(touched_entries, ensure_ascii=False)}\n"
                )
                f.write(
                    f"any_build_true={'true' if outputs['any_build_true'] else 'false'}\n"
                )
        except Exception as e:
            print(
                f"WARNING: Konnte GITHUB_OUTPUT nicht schreiben: {e}", file=sys.stderr
            )


if __name__ == "__main__":
    main()

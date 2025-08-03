"""Reporting utilities for :class:`SphereDeckCalculator`."""

from __future__ import annotations

from pathlib import Path

from ..geometry import deck as geom_deck


def to_string(
    calc: geom_deck.SphereDeckCalculator, file_path: str | None = None
) -> str:
    string_title = f"{calc.title}\n"
    string_table = calc.df_decks.to_string()
    string_total_volume = (
        f"Total Volume: {calc.calculate_total_volume_pressured()} m³\n"
    )
    string_doc = string_title + "\n" + string_table + "\n" + string_total_volume
    resolved = geom_deck._resolve_output_path(file_path)
    if resolved is not None:
        with open(resolved, "w") as f:
            f.write(string_doc)
        print(
            f"Deck dimensions have been successfully calculated and saved as text in {resolved}."
        )
    return string_doc


def to_html(calc: geom_deck.SphereDeckCalculator, file_path: str | None = None) -> str:
    html_title = f"<h1>{calc.title}</h1>"
    html_table = calc.df_decks.to_html()
    html_total_volume = (
        f"<h2>Total Volume: {calc.calculate_total_volume_pressured()} m³</h2>"
    )
    html_doc = html_title + html_table + html_total_volume
    resolved = geom_deck._resolve_output_path(file_path)
    if resolved is not None:
        with open(resolved, "w") as f:
            f.write(html_doc)
        print(
            f"Deck dimensions have been successfully calculated and saved as HTML in {resolved}."
        )
    return html_doc


def to_csv(calc: geom_deck.SphereDeckCalculator, file_path: str | None = None) -> str:
    csv_title = f"{calc.title}\n"
    csv_table = calc.df_decks.to_csv()
    csv_total_volume = f"Total Volume: {calc.calculate_total_volume_pressured()} m³\n"
    csv_doc = csv_title + csv_table + csv_total_volume
    resolved = geom_deck._resolve_output_path(file_path)
    if resolved is not None:
        with open(resolved, "w") as f:
            f.write(csv_doc)
        print(
            f"Deck dimensions have been successfully calculated and saved as CSV in {resolved}."
        )
    return csv_doc

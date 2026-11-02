import sys

from parsers import PressburgParser


def main() -> list[str]:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = PressburgParser()
    menu_lines: list[str] = parser.get_menu()

    for line in menu_lines:
        print(line)

    return menu_lines


if __name__ == "__main__":
    main()

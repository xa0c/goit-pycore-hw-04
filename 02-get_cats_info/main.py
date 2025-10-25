import pathlib, sys
import core

MSG_HELP = """\
DESCRIPTION:
    This script parses file with cat info records into Python list of dictionaries.
    If file argument isn't provided, then `test.csv` file which is shipped together with this \
repository is used.

USAGE:
    python main.py [ <file_path> | -h | --help ]

FLAGS:
    -h, --help: Show this message."""

MSG_FALLBACK_WARNING = """\
WARNING: Result values are based on the `test.csv` file which is shipped together with this \
repository.

Pass file path as the argument to get real data."""

def main():
    path = ""
    # If argument was passed to the script
    if len(sys.argv) == 2:
        if sys.argv[1] in ("-h", "--help"):
            print(MSG_HELP)
            return
        path = sys.argv[1]

    # Fallback to `test.csv` if file path wasn't provided
    if not path:
        print(MSG_FALLBACK_WARNING + "\n")
        path = str(pathlib.PurePath(__file__).parent / "test.csv")

    # Perform calculations
    try:
        cats = core.get_cats_info(path)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print("ERROR:", e)
        return -1
    print(f"Cats:\n{cats}")
    return

if __name__ == "__main__":
    main()

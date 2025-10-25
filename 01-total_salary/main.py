import pathlib, sys
import core

MSG_HELP = """\
DESCRIPTION:
    This script calculates total and average salary for the values from the provided file.
    If file argument isn't provided, then `test.csv` file which is shipped together with this \
repository is used.

USAGE:
    python main.py [ <file_path> | -h | --help ]

FLAGS:
    -h, --help: Show this message."""

MSG_FALLBACK_WARNING = """\
WARNING: Result values are based on the `test.csv` file which is shipped together with this \
repository.

To perform real calculations pass file path as the argument."""

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
        total_salary, average_salary = core.total_salary(path)
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print("ERROR:", e)
        return -1
    print(f"Total salary: {total_salary}\nAverage salary: {average_salary}")
    return

if __name__ == "__main__":
    main()

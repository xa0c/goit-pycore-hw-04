import sys
import core

MSG_HELP = """\
DESCRIPTION:
    This script prints tree-like structure of the specified directory.
    If path argument isn't provided, then current directory is used.
    Scan doesn't follow symbolic links.

USAGE:
    python main.py [ OPTIONS ] [ <path> ]

FLAGS:
    --draw-lines=<0|1>: Draw lines to visualize branches. Enabled by default.
            -h, --help: Show this message.
         --level=<int>: Maximum depth for recursive scan."""

MSG_BAD_FLAG_KEY = "ERROR: Unknown flag. Use -h flag to see the list of available options."
MSG_BAD_FLAG_VAL = "ERROR: Invalid flag format. Use -h flag to see the list of available options."

def main():
    path = ""
    level = None
    draw_lines = True
    # If argument was passed to the script
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print(MSG_HELP)
            return

        if arg.startswith("--draw-lines="):
            _, draw_lines = arg.split("=", 1)
            if not draw_lines.isascii() or not draw_lines.isdigit():
                print(MSG_BAD_FLAG_VAL)
                return -1
            draw_lines = int(draw_lines)
            if draw_lines > 1:
                print(MSG_BAD_FLAG_VAL)
                return -1
            draw_lines = bool(draw_lines)
        elif arg.startswith("--level="):
            _, level = arg.split("=", 1)
            if not level.isascii() or not level.isdigit():
                print(MSG_BAD_FLAG_VAL)
                return -1
            level = int(level)
        elif not arg.startswith("-"):
            path = arg
        else:
            print(MSG_BAD_FLAG_KEY)
            return -1

    # Fallback to current directory if path wasn't provided
    if not path:
        path = "."

    # Perform output
    try:
        core.print_tree(path, level, draw_lines)
    except OSError as e:
        print("ERROR:", e)
        return -1
    return

if __name__ == "__main__":
    main()

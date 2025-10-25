import errno, os, pathlib
from colorama import Back, Fore, Style

def print_tree(path: str, max_level: int | None = None, draw_lines: bool = True, prefix: str = ""):
    """Print tree-like structure of the specified directory.

    Scan doesn't follow symbolic links.

    Args:
        path (str): Path to the directory.
        max_level (int or None): Max depth level for nested directories.
        draw_lines (bool): Draw lines to visualize branches.
        prefix (str): Prefix used by recursion to add visual branches.

    Raises:
        OSError: If path can't be read.
    """
    if not prefix:
        print(Fore.BLUE + path + Style.RESET_ALL)

    try:
        path = pathlib.Path(path)
        # Get sorted list of directory nodes (directories first)
        nodes = sorted(path.iterdir(), key=lambda node: (not node.is_dir(), node.name))
        for node in nodes:
            # Add visual branches
            line = prefix
            if node != nodes[-1]:
                line += "├──" if draw_lines else "   "
            else:
                line += "└──" if draw_lines else "   "

            # Colorize nodes
            if node.is_block_device():
                line += Back.WHITE + Fore.YELLOW
            elif node.is_char_device():
                line += Back.WHITE + Fore.BLACK
            elif node.is_fifo():
                line += Back.WHITE + Fore.MAGENTA
            elif node.is_socket():
                line += Back.WHITE + Fore.BLUE
            elif node.is_mount():
                line += Back.BLUE + Fore.BLACK
            elif node.is_dir():
                line += Fore.BLUE
            elif node.is_symlink():
                line += Fore.CYAN if node.exists() else Fore.RED
            elif node.is_file():
                line += Fore.GREEN if os.access(node, os.X_OK) else Fore.RESET

            print(line + node.name + Style.RESET_ALL, end="")

            # Show "Permission denied" text for directories without read access
            if node.is_dir() and not node.is_symlink():
                if not os.access(node, os.R_OK):
                    print(" : Permission denied", end="")

            # Show destination for symbolic links
            if node.is_symlink():
                if node.exists():
                    print(" -> " + node.readlink().name, end="")
                else:
                    print(" -> " + Fore.RED + node.readlink().name, end="")

            print(Style.RESET_ALL)

            # Go to the next level if allowed
            if node.is_dir() and not node.is_symlink():
                new_prefix = prefix + ("│  " if draw_lines else "   ")
                if max_level == None:
                    print_tree(node.absolute(), None, draw_lines, new_prefix)
                elif max_level > 0:
                    print_tree(node.absolute(), max_level - 1, draw_lines, new_prefix)
    except OSError as e:
        match e.errno:
            case errno.ENOENT:
                raise OSError(f"Path `{path}`: Doesn't exist.") from e
            case errno.EACCES:
                raise OSError(f"Path `{path}`: Permission denied.") from e
            case errno.ENOTDIR:
                raise OSError(f"Path `{path}`: Not a directory.") from e
            case _:
                raise OSError(f"Path `{path}` can't be read.\n{e}") from e

def get_cats_info(path: str) -> list[dict]:
    """Parse cat info records.

    Args:
        path (str): Path to the source data.

    Returns:
        list[dict]: List of cats.

    Raises:
        OSError: If file can't be read.
        UnicodeDecodeError: If file has wrong UTF-8 encoding.
        ValueError: If record has invalid format.
    """
    LINE_MAX_SIZE = 100
    CURRENCY_SIZE = 100
    records_count = 0
    cats = {}
    try:
        with open(path, mode="r", encoding="utf-8", errors="strict") as fh:
            # Safe line-by-line read with line length limitation
            for line in iter(lambda: fh.readline(LINE_MAX_SIZE), ""):
                records_count += 1
                line = line.strip().split(",", 2)
                # Check if row has proper amount of columns
                if len(line) != 3:
                    raise ValueError(f"Row #{records_count} has wrong number of columns.")
                # Check if ID is present
                if not line[0]:
                    raise ValueError(f"Row #{records_count}: ID can't be empty.")
                # Check if name is present
                if not line[1]:
                    raise ValueError(f"Row #{records_count}: name can't be empty.")
                # Check if age is valid positive number
                if not line[2].isascii() or not line[2].isdigit():
                    raise ValueError(f"Row #{records_count}: age value must be a valid positive \
number.")
                # Check if record is unique
                if line[0] in cats:
                    raise ValueError(f"Record with id=`{line[0]}` is aleady present. Source data \
must contain only unique IDs.")

                cats[line[0]] = {"id": line[0], "name": line[1], "age": int(line[2])}
    except OSError as e:
        raise OSError(f"File `{path}` can't be read.") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"File `{path}` has wrong UTF-8 encoding.") from e

    return list(cats.values())

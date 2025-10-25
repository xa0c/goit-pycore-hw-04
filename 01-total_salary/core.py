import decimal, re

def total_salary(path: str) -> tuple[float, float]:
    """Calculate total and average salary.

    Args:
        path (str): Path to the source data.

    Returns:
        tuple[Decimal, Decimal]: Total & average salaries rounded to 2dp.

    Raises:
        OSError: If file can't be read.
        UnicodeDecodeError: If file has wrong UTF-8 encoding.
        ValueError: If record has invalid format.
    """
    LINE_MAX_SIZE = 100
    CURRENCY_SIZE = 100
    records_count = 0
    total_cents = 0
    number_re = re.compile(r"^\d+(\.\d+)?$")
    try:
        with open(path, mode="r", encoding="utf-8", errors="strict") as fh:
            # Safe line-by-line read with line length limit
            for line in iter(lambda: fh.readline(LINE_MAX_SIZE), ""):
                records_count += 1
                line = line.strip().split(",", 1)
                # Check if row has proper amount of columns
                if len(line) != 2:
                    raise ValueError(f"Row #{records_count} has wrong number of columns.")
                # Check if employee name is present
                if not line[0]:
                    raise ValueError(f"Row #{records_count}: name can't be empty.")
                # Check if salary is valid positive number
                if not re.match(number_re, line[1]):
                    raise ValueError(f"Row #{records_count}: salary value must be a valid positive \
number.")
                # Use Decimal and operate with cents for currency ops
                cents = decimal.Decimal(line[1]) * CURRENCY_SIZE
                # Convert cents back to int for faster ops
                cents = int(cents.to_integral_value(rounding=decimal.ROUND_HALF_UP))
                total_cents += cents
    except OSError as e:
        raise OSError(f"File `{path}` can't be read.") from e
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"File `{path}` has wrong UTF-8 encoding.") from e

    # Return (0, 0) if file is empty
    if not records_count:
        return decimal.Decimal(0), decimal.Decimal(0)

    average_cents = decimal.Decimal(total_cents) / records_count
    # Make sure that average salary cents are properly rounded
    average_cents = average_cents.to_integral_value(rounding=decimal.ROUND_HALF_UP)
    return decimal.Decimal(total_cents) / CURRENCY_SIZE, average_cents / CURRENCY_SIZE

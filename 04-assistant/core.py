E_UNKNOWN_FORMAT = "\
Unknown contact format. Phone number must contain only digits. Email must contain '@' character."

persons = {}

def add_contact(name: str, value: str) -> str:
    """Add new contact record to the specified person.

    Creates person key if it doesn't exist.

    Args:
        name (str): Person's name.
        value (str): Contact value for phone number or email address.

    Returns:
        string: Determined type of contact ("phone" or "email").

    Raises:
        ValueError: If contact already exists for the specified person.
    """
    if value.isascii and value.isdigit():
        persons.setdefault(name, {"phones": set(), "emails": set()})
        phone_number = int(value)
        if phone_number in persons[name]["phones"]:
            raise ValueError("Such phone number already exists for the specified person.")
        persons[name]["phones"].add(phone_number)
        return "phone"
    elif value.find("@") != -1:
        persons.setdefault(name, {"phones": set(), "emails": set()})
        if value in persons[name]["emails"]:
            raise ValueError("Such email address already exists for the specified person.")
        persons[name]["emails"].add(value)
        return "email"
    raise ValueError(E_UNKNOWN_FORMAT)

def change_contact(name: str, value: str) -> str:
    """Rewrite person's contacts of the determined type with new record.

    Args:
        name (str): Person's name.
        value (str): Contact value for phone number or email address.

    Returns:
        string: Determined type of contact ("phone" or "email").

    Raises:
        ValueError: If person doesn't exist.
    """
    if name not in persons:
        raise ValueError("Specified person doesn't exist.")
    if value.isascii and value.isdigit():
        persons[name]["phones"] = {int(value)}
        return "phone"
    elif value.find("@") != -1:
        persons[name]["emails"] = {value}
        return "email"
    raise ValueError(E_UNKNOWN_FORMAT)

def delete_contact(name: str, value: str) -> str:
    """Delete contact by value for the specified person.

    Args:
        name (str): Person's name.
        value (str): Contact value for phone number or email address.

    Returns:
        string: Determined type of contact ("phone" or "email").

    Raises:
        ValueError: If contact doesn't exists for the specified person.
    """
    if name not in persons:
        raise ValueError("Specified person doesn't exist.")
    if value.isascii and value.isdigit():
        try:
            persons[name]["phones"].remove(int(value))
        except KeyError as e:
            raise ValueError("Specified phone number doesn't exist.") from e
        return "phone"
    elif value.find("@") != -1:
        try:
            persons[name]["emails"].remove(value)
        except KeyError as e:
            raise ValueError("Specified email address doesn't exist.") from e
        return "email"
    raise ValueError(E_UNKNOWN_FORMAT)

def show_phone(name: str) -> list:
    """Return all phones for the specified person.

    Args:
        name (str): Person's name.

    Returns:
        list: Sorted list of unique person's phones.

    Raises:
        ValueError: If person doesn't exist.
    """
    if name not in persons:
        raise ValueError("Specified person doesn't exist.")
    return sorted(persons[name]["phones"])

def show_email(name: str) -> list:
    """Return all emails for the specified person.

    Args:
        name (str): Person's name.

    Returns:
        list: Sorted list of unique person's emails.

    Raises:
        ValueError: If person doesn't exist.
    """
    if name not in persons:
        raise ValueError("Specified person doesn't exist.")
    return sorted(persons[name]["emails"])

def render_person_table(name: str = None) -> str:
    """Render person's contacts as a 2-col table of phones and emails.

    Renders single person if name is provided. Otherwise renders all.

    Args:
        name (str): Person's name.

    Returns:
        str: Rendered person's table of contacts.

    Raises:
        ValueError: If person doesn't exist.
    """
    render_dict = persons
    if name:
        if name not in persons:
            raise ValueError("Specified person doesn't exist.")
        render_dict = {name: persons[name]}

    output = ""
    for name, contacts in render_dict.items():
        output += "/" + '═' * 80 + "\\\n"
        output += "│ " + f"Person: {name}".ljust(79) + "│\n"
        output += "├" + "─" * 80 + "┤\n"
        output += "│ " + "Phones".center(30) + "│ " + "Emails".center(47) + "│\n"
        output += "│" + "-" * 80 + "│\n"
        # Sort sets
        phones = sorted(contacts["phones"])
        emails = sorted(contacts["emails"])
        # Equalize lists for equal zip loop
        length_diff = len(phones) - len(emails)
        if length_diff > 0:
            emails.extend([""] * length_diff)
        elif length_diff < 0:
            phones.extend([""] * abs(length_diff))
        for phone, email in zip(phones, emails):
            output += "│ " + str(phone).ljust(30) + "│ " + email.ljust(47) + "│\n"
        output += "└" + "─" * 80 + "┘\n"
    return output

import readline
import core

MSG_HELP = """\
DESCRIPTION:
    This script provides CLI for contact management.

USAGE:
    - add <person> <value>
        Analyzes content of <value>, determines its type (phone/email) and adds contact record for\
 the specified person. Duplicates aren't allowed.
    - change <person> <value>
        Rewrites all contact records of the determined <value> type (phone/email) for the \
specified person.
    - delete <person> <value>
        Delete person's contact by its value.
    - phone <person>
        Prints all person's phone numbers.
    - email <person>
        Prints all person's email addresses.
    - all [ <person> ]
        If person is specified, prints all associated email addresses and phone numbers.
        Otherwise prints complete contacts database.
    - help
        Prints this message.
    - hello
        Prints "hello" message.
    - exit | close
        Quits application.

NOTES:
    Person name can contain spaces."""

MSG_BAD_ARG_COUNT = "Wrong number of arguments. Use -h flag to read about command usage."

def parse_input(user_input: str) -> tuple[str, dict[str, str]]:
    """Parse string into a tuple of command name and its arguments.

    Args:
        user_input (str): Input string.

    Returns:
        tuple[str, dict[str, str]]: Tuple of command name and a
            dictionary of it's arguments.

    Raises:
        ValueError: If user input has wrong number of arguments.
    """
    if not user_input:
        return "", {}

    cmd, *args = user_input.strip().split()
    match cmd:
        case "add" | "change" | "delete":
            if len(args) < 2:
                raise ValueError(MSG_BAD_ARG_COUNT)
            args = {"name": " ".join(args[:-1]), "value": args[-1]}
        case "phone" | "email":
            if len(args) < 1:
                raise ValueError(MSG_BAD_ARG_COUNT)
            args = {"name": " ".join(args)}
        case "all":
            args = {} if len(args) == 0 else {"name": " ".join(args)}

    return cmd.lower(), args

def print_person(name: str = None):
    """Print person's contacts as a 2-column table of phones and emails.

    Prints single person if name is provided. Otherwise prints all.

    Args:
        name (str): Person's name.

    Raises:
        ValueError: If person doesn't exist.
    """
    persons = core.persons
    if name:
        if name not in core.persons:
            raise ValueError("Specified person doesn't exist.")
        persons = {name: core.persons[name]}

    for name, contacts in persons.items():
        print('/' + '═' * 80 + '\\')
        print('│ ' + f"Person: {name}".ljust(79) + '│')
        print('├' + '─' * 80 + '┤')
        print('│ ' + "Phones".center(30) + '│ ' + "Emails".center(47) + '│')
        print('│' + '-' * 80 + '│')
        phones = sorted(contacts["phones"])
        emails = sorted(contacts["emails"])
        length_diff = len(phones) - len(emails)
        if length_diff > 0:
            emails.extend([""] * length_diff)
        elif length_diff < 0:
            phones.extend([""] * abs(length_diff))
        for phone, email in zip(phones, emails):
            print('│ ' + str(phone).ljust(30) + '│ ' + email.ljust(47) + '│' )
        print('└' + '─' * 80 + '┘')

def main():
    print(MSG_HELP)

    while True:
        # Handle empty input, interrupts and parse errors
        try:
            cmd = input("> ")
            if not cmd:
                continue
            cmd, args = parse_input(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user.")
            break
        except ValueError as e:
            print("ERROR:", e, "Try again.")
            continue

        # Handle commands
        try:
            match cmd:
                case "exit" | "close":
                    print("Exiting program. Good bye!")
                    break
                case "hello":
                    print("Hello! How can I help you?")
                case "help":
                    print(MSG_HELP)
                case "add":
                    result = core.add_contact(**args)
                    print(f"{result.title()} contact added.")
                case "change":
                    result = core.change_contact(**args)
                    print(f"Contact updated. All previous {result} contacts were rewritten.")
                case "delete":
                    result = core.delete_contact(**args)
                    print(f"{result.title()} contact deleted.")
                case "phone":
                    result = core.show_phone(**args)
                    if result:
                        print(f"List of phone numbers for {args["name"]}:")
                        for phone in result:
                            print(phone)
                    else:
                        print(f"{args["name"]} doesn't have any phone numbers.")
                case "email":
                    result = core.show_email(**args)
                    if result:
                        print(f"List of email addresses for {args["name"]}:")
                        for email in result:
                            print(email)
                    else:
                        print(f"{args["name"]} doesn't have any email addresses.")
                case "all":
                    print_person(**args)
                case _:
                    print("ERROR: Unknown command. Try again.")
        except ValueError as e:
            print("ERROR:", e, "Try again.")

if __name__ == "__main__":
    main()

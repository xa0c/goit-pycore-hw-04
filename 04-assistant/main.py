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

MSG_BAD_ARG_COUNT = "ERROR: Wrong number of arguments. Use -h flag to read about command usage."

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parse string into a tuple of command name and its arguments.

    Args:
        user_input (str): Input string.

    Returns:
        tuple[str, list]: Tuple of command name and it's arguments.
    """
    if not user_input:
        return "", []
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args

def print_person(name: str, contacts: dict[str, set]):
    """Print person's contacts as a 2-column table of phones and emails.

    Args:
        name (str): Person's name.
        contacts (dict[str, set]): Dictionary of sets for phones/emails.
    """
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
        try:
            cmd = input("> ")
            if not cmd:
                continue
            cmd, args = parse_input(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted by user.")
            break

        match cmd:
            case "exit" | "close":
                print("Exiting program. Good bye!")
                break
            case "hello":
                print("Hello! How can I help you?")
                continue
            case "help":
                print(MSG_HELP)
                continue
            case "add":
                if len(args) < 2:
                    print(MSG_BAD_ARG_COUNT)
                    continue
                try:
                    result = core.add_contact(" ".join(args[:-1]), args[-1])
                except ValueError as e:
                    print("ERROR:", e, "Try again.")
                    continue
                print(f"{result.title()} contact added.")
            case "change":
                if len(args) < 2:
                    print(MSG_BAD_ARG_COUNT)
                    continue
                try:
                    result = core.change_contact(" ".join(args[:-1]), args[-1])
                except ValueError as e:
                    print("ERROR:", e, "Try again.")
                    continue
                print(f"Contact updated. All previous {result} contacts were rewritten.")
            case "delete":
                if len(args) < 2:
                    print(MSG_BAD_ARG_COUNT)
                    continue
                try:
                    result = core.delete_contact(" ".join(args[:-1]), args[-1])
                except ValueError as e:
                    print("ERROR:", e, "Try again.")
                    continue
                print(f"{result.title()} contact deleted.")
            case "phone":
                if len(args) < 1:
                    print(MSG_BAD_ARG_COUNT)
                    continue
                name = " ".join(args)
                try:
                    result = core.show_phone(name)
                except ValueError as e:
                    print("ERROR:", e, "Try again.")
                    continue
                if result:
                    print(f"List of phone numbers for {name}:")
                    for phone in sorted(result): print(phone)
                else:
                    print(f"{name} doesn't have any phone numbers.")
            case "email":
                if len(args) < 1:
                    print(MSG_BAD_ARG_COUNT)
                    continue
                name = " ".join(args)
                try:
                    result = core.show_email(name)
                except ValueError as e:
                    print("ERROR:", e, "Try again.")
                    continue
                if result:
                    print(f"List of email addresses for {name}:")
                    for email in sorted(result): print(email)
                else:
                    print(f"{name} doesn't have any email addresses.")
            case "all":
                if len(args) == 0:
                    for name in core.persons:
                        print_person(name, core.persons[name])
                else:
                    name = " ".join(args)
                    if name not in core.persons:
                        print("ERROR: Specified person doesn't exist. Try again.")
                        continue
                    print_person(name, core.persons[name])
            case _:
                print("ERROR: Unknown command. Try again.")
                continue

if __name__ == "__main__":
    main()

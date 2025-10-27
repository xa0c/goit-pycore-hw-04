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

def print_contact_list(person_name: str, contact_type: str, contacts: list):
    """Prints user-friendly list of person's contacts by type.

    Args:
        person_name (str): Person's name.
        contact_type (str): Contact type ("phone" or "email")
        contacts (list): List of contacts to output.
    """
    if contacts:
        print(f"List of {contact_type} contacts for {person_name}:")
        for contact in contacts:
            print(contact)
    else:
        print(f"{person_name} doesn't have any {contact_type} contacts.")

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
                    print_contact_list(args["name"], cmd, result)
                case "email":
                    result = core.show_email(**args)
                    print_contact_list(args["name"], cmd, result)
                case "all":
                    print(core.render_person_table(**args))
                case _:
                    print("ERROR: Unknown command. Try again.")
        except ValueError as e:
            print("ERROR:", e, "Try again.")

if __name__ == "__main__":
    main()

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(HERE, "contacts.json")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9 \-]{5,18}[0-9]$")


class StorageError(Exception):
    pass


def check_loaded_data(data, path):
    if not isinstance(data, list):
        raise StorageError(path + " does not contain a list of contacts. The file was left untouched.")

    seen_ids = set()
    for item in data:
        valid = (isinstance(item, dict)
                 and isinstance(item.get("id"), int)
                 and all(isinstance(item.get(key), str) for key in ("name", "phone", "email")))
        if not valid:
            raise StorageError(path + " has an entry that is not a valid contact. The file was left untouched.")
        if item["id"] in seen_ids:
            raise StorageError(path + " has a repeated contact ID " + str(item["id"]) + ". The file was left untouched.")
        seen_ids.add(item["id"])


def load_contacts(path):
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as contact_file:
            text = contact_file.read()
    except OSError as error:
        raise StorageError("Could not read " + path + ": " + str(error))

    if text.strip() == "":
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise StorageError(path + " is not valid JSON (" + str(error) + "). The file was left untouched.")

    check_loaded_data(data, path)
    return data


def save_contacts(path, contacts):
    temp_path = path + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as contact_file:
        json.dump(contacts, contact_file, indent=2)
        contact_file.flush()
        os.fsync(contact_file.fileno())
    os.replace(temp_path, path)


def clean_name(name):
    name = name.strip()
    if name == "":
        raise ValueError("Name cannot be empty")
    return name


def clean_phone(phone):
    phone = phone.strip()
    if phone != "" and not PHONE_PATTERN.match(phone):
        raise ValueError("Phone number looks invalid: " + phone)
    return phone


def clean_email(email):
    email = email.strip()
    if email != "" and not EMAIL_PATTERN.match(email):
        raise ValueError("Email looks invalid: " + email)
    return email


def next_id(contacts):
    return max((contact["id"] for contact in contacts), default=0) + 1


def add_contact(contacts, name, phone="", email=""):
    contact = {
        "id": next_id(contacts),
        "name": clean_name(name),
        "phone": clean_phone(phone),
        "email": clean_email(email),
    }
    contacts.append(contact)
    return contact


def find_contact(contacts, contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    return None


def search_contacts(contacts, text):
    needle = text.strip().casefold()
    if needle == "":
        raise ValueError("Search text cannot be empty")
    matches = [contact for contact in contacts if needle in contact["name"].casefold()]
    return sorted(matches, key=lambda contact: contact["id"])


def update_contact(contacts, contact_id, name=None, phone=None, email=None):
    contact = find_contact(contacts, contact_id)
    if contact is None:
        raise ValueError("No contact with ID " + str(contact_id))

    new_name = contact["name"] if name is None else clean_name(name)
    new_phone = contact["phone"] if phone is None else clean_phone(phone)
    new_email = contact["email"] if email is None else clean_email(email)

    contact["name"] = new_name
    contact["phone"] = new_phone
    contact["email"] = new_email
    return contact


def delete_contact(contacts, contact_id):
    contact = find_contact(contacts, contact_id)
    if contact is None:
        raise ValueError("No contact with ID " + str(contact_id))
    contacts.remove(contact)
    return contact


def list_contacts(contacts):
    return sorted(contacts, key=lambda contact: contact["id"])


def show_contact(contact):
    phone = contact["phone"] or "-"
    email = contact["email"] or "-"
    print("  [" + str(contact["id"]) + "] " + contact["name"] + " | " + phone + " | " + email)


def ask_for_id(prompt):
    text = input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValueError("ID must be a whole number")


def try_to_save(path, contacts):
    try:
        save_contacts(path, contacts)
    except OSError as error:
        print("Could not save contacts:", error)


def run_menu(path):
    contacts = load_contacts(path)

    while True:
        print()
        print("1. Add contact")
        print("2. Search by name")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. List all contacts")
        print("6. Exit")

        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        try:
            if choice == "1":
                name = input("Name: ")
                phone = input("Phone (optional): ")
                email = input("Email (optional): ")
                contact = add_contact(contacts, name, phone, email)
                try_to_save(path, contacts)
                print("Added:")
                show_contact(contact)

            elif choice == "2":
                results = search_contacts(contacts, input("Search for: "))
                if results:
                    for contact in results:
                        show_contact(contact)
                else:
                    print("No contacts found.")

            elif choice == "3":
                contact_id = ask_for_id("ID to update: ")
                current = find_contact(contacts, contact_id)
                if current is None:
                    raise ValueError("No contact with ID " + str(contact_id))
                print("Press Enter to keep the current value.")
                name = input("Name [" + current["name"] + "]: ")
                phone = input("Phone [" + current["phone"] + "]: ")
                email = input("Email [" + current["email"] + "]: ")
                updated = update_contact(
                    contacts, contact_id,
                    name=name if name.strip() else None,
                    phone=phone if phone.strip() else None,
                    email=email if email.strip() else None,
                )
                try_to_save(path, contacts)
                print("Updated:")
                show_contact(updated)

            elif choice == "4":
                contact_id = ask_for_id("ID to delete: ")
                removed = delete_contact(contacts, contact_id)
                try_to_save(path, contacts)
                print("Deleted:")
                show_contact(removed)

            elif choice == "5":
                everyone = list_contacts(contacts)
                if everyone:
                    for contact in everyone:
                        show_contact(contact)
                else:
                    print("No contacts yet.")

            elif choice == "6":
                print("Goodbye.")
                break

            else:
                print("Please choose a number from 1 to 6.")

        except ValueError as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print()
            break


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
    try:
        run_menu(path)
    except StorageError as error:
        print("Storage problem:", error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

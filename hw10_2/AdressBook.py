import re
from datetime import datetime
from datetime import date

from mongoengine import NotUniqueError, Q

from models import Contacts


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class MailExists(Exception):
    pass


class AdressExists(Exception):
    pass


class IncorrectEmailFormat(Exception):
    pass


class IncorrectAdressFormat(Exception):
    pass


class PhoneNumberError(Exception):
    pass


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        codes_operators = ["067", "068", "096", "097", "098", "050",
                           "066", "095", "099", "063", "073", "093"]
        new_value = (value.strip().
                     removeprefix('+').
                     replace("(", '').
                     replace(")", '').
                     replace("-", ''))
        if new_value[:2] == '38' and len(new_value) == 12 and new_value[2:5] in codes_operators:
            self.__value = new_value
        else:
            raise PhoneNumberError

    def get_phone(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        if value:
            try:
                datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Incorrect data format, should be DD.MM.YYYY")
        self.__value = value


class Mail(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, value):
            self.__value = value
        else:
            raise IncorrectEmailFormat

    def get_email(self) -> str:
        return self.value


class Adress(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        regex = r'^([\w]([\.,]?)([\s]?)){1,60}$'
        if re.match(regex, value):
            self.__value = value
        else:
            raise IncorrectAdressFormat

    def get_adres(self) -> str:
        return self.value

def days_to_birthday(data_):
    if data_:
        start = date.today()
        birthday_date = data_
        end = date(day=birthday_date.day, month=birthday_date.month, year=start.year)
        count_days = (end - start).days
        if count_days < 0:
            count_days += 365
        return count_days
    else:
        return 'Unknown birthday'



class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Input formatting is not correct, make sure to check -help-!'
        except KeyError:
            return 'Sorry,user not found, try again!'
        except ValueError:
            return 'Sorry,incorrect argument,try again!'
        except MailExists:
            return "This e-mail already exists in the address book"
        except AdressExists:
            return 'This address already exists in the address book'
        except IncorrectEmailFormat:
            return "Email must contain latin letters, @ and domain after . (Example: 'email@.com)"
        except IncorrectAdressFormat:
            return 'Incorrect address! Example: Kyiv,Pr.Dnipro,12'
        except PhoneNumberError:
            return "Phone number must be 12 digits, and start with 380"
        except NotUniqueError:
            return "User name and phones must be unique."


def greeting(*args):
    return 'Hello! Can I help you?'


@InputError
def add(*args):
    phones = []
    user_name = (args[0])
    phone = str(Phone(args[1]))
    phones.append(phone)
    try:
        birthday = str(Birthday(args[2]))
    except IndexError:
        birthday = '-'
    contact = Contacts(
        user_name=user_name,
        phones=phones,
        birthday=birthday
        )
    contact.save()
    return f'Add user {user_name}, phone {phone}, birthday {birthday}'


@InputError
def add_mail(*args):
    user_name = str(args[0])
    mail = str(Mail(args[1]))
    contact = Contacts.objects(user_name=user_name)
    for c in contact:
        if c.email is None:
            contact.update(email=mail)
            return f'Email {mail} added successful to user {user_name}.'
        else:
            return f'User with id {user_name} already has email'


@InputError
def add_address(*args):
    user_name = str(args[0])
    address = str(Adress(args[1]))
    contact = Contacts.objects(user_name=user_name)
    for c in contact:
        if c.address is None:
            contact.update(address=address)
            return f'Address {address} added successful to user {user_name}.'
        else:
            return f'User with id {user_name} already has address'


@InputError
def change_phone(*args):
    user_name, old_phone, new_phone = str(args[0]), str(Phone(args[1])), str(Phone(args[2]))
    contact = Contacts.objects(user_name=user_name)
    if not contact:
        return f'User {user_name} does not exist'
    for c in contact:
        if old_phone in c.phones:
            phone_list = c.phones
            phone_list.remove(old_phone)
            phone_list.append(new_phone)
            contact.update(phones=phone_list)
            return f'Phone {old_phone} changed successful to {new_phone}.'
        else:
            return f'Phone {old_phone} not found.'


@InputError
def change_email(*args):
    user_name, mail, new_mail = str(args[0]), str(Mail(args[1])), str(Mail(args[2]))
    contact = Contacts.objects(user_name=user_name)
    if not contact:
        return f'User {user_name} does not exist'
    for c in contact:
        if c.email == mail:
            contact.update(email=new_mail)
            return f'Email {mail} changed successful to {new_mail}.'
        else:
            return f'Email {mail} not found.'


@InputError
def change_address(*args):
    user_name, address, new_address = str(args[0]), str(Mail(args[1])), str(Mail(args[2]))
    contact = Contacts.objects(user_name=user_name)
    if not contact:
        return f'User {user_name} does not exist'
    for c in contact:
        if c.address == address:
            contact.update(adress=new_address)
            return f'Address {address} changed successful to {new_address}.'
        else:
            return f'Address {address} not found.'


@InputError
def del_contact(*args):
    user_name = str(args[0])
    contact = Contacts.objects(user_name=user_name)
    contact.dalete()
    return f'Deleted user with name {user_name}'


@InputError
def show_all(*args):
    contacts = Contacts.objects.all()
    count = 1
    for contact in contacts:
        print('_' * 25, f'Sequence number {count}', '_' * 25)
        print(f"user_id___: {contact.id},\n"
                f"user_name_: {contact.user_name},\n"
                f"birthday__: {contact.birthday},\n"
                f"email_____: {contact.email},\n"
                f"address___: {contact.address},\n"
                f"phone(s)__: {contact.phones}")
        count += 1
    print('-' * 67)
    return 'END'


@InputError
def birthday(*args):
    user_name = str(args[0])
    contact = Contacts.objects(user_name=user_name)
    if not contact:
        return f'User {user_name} does not exist'
    for c in contact:
        if c.birthday == '-':
            return f'User with name {user_name} birthday is unknown '
        else:
            return f'User with name {user_name} birthday is at {c.birthday}'


def backing(*args):
    return 'Good bye CommandBot!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


@InputError
def find(*args):
    count = 1
    substring = str(args[0])
    contacts = Contacts.objects(Q(user_name__icontains=substring) |\
                                Q(birthday__icontains=substring) |\
                                Q(email__icontains=substring) |\
                                Q(address__icontains=substring)|\
                                Q(phones__icontains=substring))
    if contacts:
        for contact in contacts:
            print('_' * 25, f'Sequence number {count}', '_' * 25)
            print(f"user_id___: {contact.id},\n"
                    f"user_name_: {contact.user_name},\n"
                    f"birthday__: {contact.birthday},\n"
                    f"email_____: {contact.email},\n"
                    f"address___: {contact.address},\n"
                    f"phone(s)__: {contact.phones}")
            count += 1
        print('-' * 67)
        return 'The end'
    else:
        return "Nothing find"


@InputError
def show_birthday_x_days(*args):
    x = int(args[0])
    birth_list = []
    contacts = Contacts.objects.all()
    for contact in contacts:
        if contact.birthday != '-':
            birthday_date = datetime.strptime(contact.birthday, '%d.%m.%Y').date()
            if days_to_birthday(birthday_date) <= x:
                birth_list.append(contact.user_name)
    if len(birth_list) == 0:
        return f'There are no birthdays in the selected period'
    else:
        print('Users, who have birthday in the selected period:')
        print(*birth_list)
        return 'The end'


def help(*args):
    return """Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting
    Command: "hello" - returns a greeting
    Command: "add" Enter: name phone (birthday) - adds a phone to a contact, adds a birthday (optional)
    Command: "new phone" Enter: name phone new phone - changes a phone number to a new one
    Command: "show all" - displays all contacts
    Command: "birthday" Enter: name - finds a birthday for name
    Command: "soon birthday" Enter: {days} - gives a list of users who have birthday within the next {days}, where days = number of your choosing
    Command: "find" Enter: [any strings} - finds matches in the address book and returns the findings
    Command: "email" Enter: name email - adds an email for a user
    Command: "new email" Enter: name old email new email - changes old email to new email
    Command: "new address" Enter: name old address new address - changes old address to the new address
    Command: "address" Enter: name address - adds and address for a user, address format city,street,number
    Command: "remove contact" Enter:  name - deletes the user and all his data from the contact book
    Command: "back" - returns to the selection of work branches
    """


COMMANDS = {greeting: ['hello'], add: ['add '], change_phone: ['new phone'],
            show_all: ['show all'], backing: ['back'], birthday: ['birthday '],
            find: ['find', 'check'], add_mail: ['email'], add_address: ['address'],
            change_email: ["new email"], change_address: ['new address', 'new address'],
            show_birthday_x_days: ['soon birthday'], del_contact: ['remove contact'], help: ['help']}


def new_func():
    return str, list


def command_parser(user_command: str) -> new_func():
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []





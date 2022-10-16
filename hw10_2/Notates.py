from mongoengine import Q

from models import Notates


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Sorry,such a note does not exist'
        except KeyError:
            return 'Sorry,user not found, try again!'
        except ValueError:
            return 'Sorry,value is incorrect,try again!'


@InputError
def add(*args):
    notate = ''
    for _ in args:
        notate += _ + ' '
    notate_ = Notates(
        notate=notate,
        tag=[]
        )
    notate_.save(())
    return f'Notate added successful'


@InputError
def add_tag(*args):
    _id = args[0]
    # for i in range(1, len(args)):
    #     tag += args[i] + ' '
    notate = Notates.objects(_id=_id)
    for n in notate:
        tags = n.tag
        tags.extend(args[1:])
        notate.update(tag=tags)
        return f'Tag(s) added successful to notate id {_id}'


@InputError
def del_notate(*args):
    _id = args[0]
    notate = Notates.objects(_id=_id)
    notate.delete()
    return f'Deleted notate with id {_id}'


@InputError
def del_tag(*args):
    _id = args[0]
    notate = Notates.objects(_id=_id)
    notate.update(tag=[])
    return f'Tags deleted'


@InputError
def change_notate(*args):
    _id = args[0]
    notate_ = ''
    for i in range(1, (len(args))):
        notate_ += args[i] + ' '
    notate = Notates.objects(_id=_id)
    notate.update(notate=notate_)
    return f'Notate changed successful'


@InputError
def find_symb(*args):
    count = 1
    substring = str(args[0])
    notates = Notates.objects(Q(notate__icontains=substring) | Q(tag__icontains=substring))
    if notates:
        for notate in notates:
            print('_' * 25, f'Sequence number {count}', '_' * 25)
            print(f"_id____: {notate.id},\n"
                  f"notate_: {notate.notate},\n"
                  f"tags___: {notate.tag}")
            count += 1
        print('-' * 67)
        return 'The end'
    else:
        return "Nothing find"


@InputError
def find_tags(*args):
    substring = str(args[0])
    count = 1
    substring = str(args[0])
    notates = Notates.objects(tag__icontains=substring)
    if notates:
        for notate in notates:
            print('_' * 25, f'Sequence number {count}', '_' * 25)
            print(f"_id____: {notate.id},\n"
                  f"notate_: {notate.notate},\n"
                  f"tags___: {notate.tag}")
            count += 1
        print('-' * 67)
        return 'The end'
    else:
        return "Nothing find"



@InputError
def clear(*args):
    notate = Notates.objects.all()
    notate.delete()
    return 'All notates deleted'


def show_notates(*args):
    count =1
    notates = Notates.objects.all()
    if notates:
        for notate in notates:
            print('_' * 25, f'Sequence number {count}', '_' * 25)
            print(f"_id____: {notate.id},\n"
                  f"notate_: {notate.notate},\n"
                  f"tags___: {notate.tag}")
            count += 1
        print('-' * 67)
        return 'The end'


def backing_notates(*args):
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


def greeting(*args):
    return 'Hello! Can I help you?'


def help(*args):
    return """Commands format - Command meaning
    Command: "help" - returns a list of available commands with formatting
    Command: "hello" - returns a greeting
    Command: "add" Enter: note - adds a note to a NotateBook
    Command: "tag" Enter: number of note and tags in format 'tag1, tag2, ...'
    Command: "del notate" Enter: the number of the note you want to delete
    Command: "del tag" Enter: the number of the note whose tags you want to delete
    Command: "change" Enter: the number of the note you want to change and new note
    Command: "find notate" Enter: the text that the notes should contain
    Command: "find tag" Enter: the tag(s) that the note's tags should contain
    Command: "show"  print a book of notes
    Command: "clear"  delete a book of notes
    Command: "back" returns to the selection of work branches
    """


COMMANDS = {greeting: ['hello'], add: ['add'], backing_notates: ['back'],
            show_notates: ['show'], add_tag: ['tag'], del_notate : ['del notate'],
            del_tag : ['del tag'], change_notate: ['change'],  help: ['help'],
            find_symb: ['find notate'], clear: ['clear'], find_tags: ['find tag']}


def new_func():
    return str, list


def command_parser_not(user_command: str) -> new_func():
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                data = user_command[len(value)+1:].split(' ')
                return key, data
    else:
        return unknown_command, []





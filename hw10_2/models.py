
from mongoengine import *
#
# connect(host='mongodb://localhost:27017/cli_assistant')


class Contacts(Document):
    user_name = StringField(required=True, unique=True)
    birthday = StringField(max_length=50)
    email = StringField(max_length=100)
    address = StringField(max_length=100)
    phones = ListField(StringField(max_length=200, unique=True))


class Notates(Document):
    _id = SequenceField(required=True)
    notate = StringField(max_length=50, nullable=False)
    tag = ListField(StringField(max_length=50))




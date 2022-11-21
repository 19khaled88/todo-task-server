from mongoengine import Document, IntField, StringField


class Employee(Document):
    emp_id = IntField()
    Name = StringField(max_length=100)
    age = IntField()

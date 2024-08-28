import csv
from models import db, Group, Contact, Call

def import_groups():
    with open('groups.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group = Group(
                id=row['group_id'],
                name=row['name'],
                memberCount=row['member_count'],
                dayCallCount=row['day_call_count']
            )
            db.session.add(group)
        db.session.commit()

def import_contacts():
    with open('contacts.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contact = Contact(
                id=row['contact_id'],
                name=row['name'],
                phone_number=row['phone_number'],
                group_id=row['group_id']
            )
            db.session.add(contact)
        db.session.commit()

def import_calls():
    with open('calls.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            call = Call(
                id=row['call_id'],
                day_of_week=row['day_of_week'],
                caller_id=row['caller_id'],
                receiver_id=row['receiver_id'],
                group_id=row['group_id']
            )
            db.session.add(call)
        db.session.commit()

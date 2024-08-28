import csv
from models import db, Group, Contact, Call

def export_groups():
    groups = Group.query.all()
    with open('groups.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['group_id', 'name', 'member_count', 'day_call_count'])
        for group in groups:
            writer.writerow([group.id, group.name, group.memberCount, group.dayCallCount])

def export_contacts():
    contacts = Contact.query.all()
    with open('contacts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['contact_id', 'name', 'phone_number', 'group_id'])
        for contact in contacts:
            writer.writerow([contact.id, contact.name, contact.phone_number, contact.group_id])

def export_calls():
    calls = Call.query.all()
    with open('calls.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['call_id', 'day_of_week', 'caller_id', 'receiver_id', 'group_id'])
        for call in calls:
            writer.writerow([call.id, call.day_of_week, call.caller_id, call.receiver_id, call.group_id])

if __name__ == "__main__":
    export_groups()
    export_contacts()
    export_calls()
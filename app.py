from flask import Flask, request, jsonify, render_template
from models import db, Group, Contact, Call
from __init__ import create_app
import os

app = create_app()

# Check if the database file exists
if not os.path.exists('app.db'):
    with app.app_context():
        db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    new_group = Group(name=data['name'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'id': new_group.id, 'name': new_group.name})

@app.route('/create_contact', methods=['POST'])
def create_contact():
    data = request.json
    new_contact = Contact(
        name=data['name'],
        phone_number=data['phone_number'],
        group_id=data['group_id']
    )
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'id': new_contact.id, 'name': new_contact.name, 'phone_number': new_contact.phone_number})

@app.route('/create_call', methods=['POST'])
def create_call():
    data = request.json
    new_call = Call(
        day_of_week=data['day_of_week'],
        caller_id=data['caller_id'],
        receiver_id=data['receiver_id'],
        group_id=data['group_id']
    )
    db.session.add(new_call)
    db.session.commit()
    return jsonify({'id': new_call.id, 'day_of_week': new_call.day_of_week, 'group_id': new_call.group_id})

@app.route('/get_contacts_by_group', methods=['GET'])
def get_contacts_by_group():
    group_name = request.args.get('group_name')
    group = Group.query.filter_by(name=group_name).first()
    if group:
        contacts = Contact.query.filter_by(group_id=group.id).all()
        return jsonify([{'id': contact.id, 'name': contact.name, 'phone_number': contact.phone_number} for contact in contacts])
    return jsonify({'message': 'Group not found'}), 404

@app.route('/get_calls_by_group', methods=['GET'])
def get_calls_by_group():
    group_name = request.args.get('group_name')
    group = Group.query.filter_by(name=group_name).first()
    if group:
        calls = Call.query.filter_by(group_id=group.id).all()
        return jsonify([
            {
                'id': call.id,
                'day_of_week': call.day_of_week,
                'caller_id': call.caller_id,
                'receiver_id': call.receiver_id
            } for call in calls
        ])
    return jsonify({'message': 'Group not found'}), 404

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)



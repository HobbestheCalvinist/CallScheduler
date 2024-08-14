-- Run this command to populate data:
-- sqlite3 instance/app.db < create_test_data.sql


-- Delete records from the 'group' table if they exist
DELETE FROM "group" WHERE id IN (1, 2);

-- Insert test data into the 'group' table
INSERT INTO "group" (id, name) VALUES (1, 'Group A');
INSERT INTO "group" (id, name) VALUES (2, 'Group B');

-- Delete records from the 'contact' table if they exist
DELETE FROM "contact" WHERE id IN (1, 2, 3, 4);

-- Insert test data into the 'contact' table
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (1, 'Alice', '123-456-7890', 1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (2, 'Bob', '234-567-8901', 1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (3, 'Charlie', '345-678-9012', 2);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (4, 'Diana', '456-789-0123', 2);

-- Delete records from the 'call' table if they exist
DELETE FROM "call" WHERE id IN (1, 2, 3, 4, 5);

-- Insert test data into the 'call' table
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (1, 'Monday', 1, 2, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (2, 'Tuesday', 2, 1, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (3, 'Wednesday', 1, 3, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (4, 'Thursday', 3, 4, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (5, 'Friday', 4, 3, 2);

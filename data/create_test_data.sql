-- Clean up existing groups and contacts
DELETE FROM "call"; 
DELETE FROM "contact";
DELETE FROM "group";

---- Insert test data for Group A
INSERT INTO "group" (id, name, memberCount, dayCallCount) VALUES (1, 'Group A', 5, 6);

INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (1, 'Alice', '123-456-7890',   1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (2, 'Bob', '234-567-8901',     1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (3, 'Eve', '345-678-9012',     1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (4, 'Mallory', '456-789-0123', 1);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (5, 'Trent', '567-890-1234',   1);
--                                                                                    call,rec,group
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (1, 'Day1',1, 2, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (2, 'Day2',2, 1, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (3, 'Day3',1, 3, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (4, 'Day4',3, 4, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (5, 'Day5',4, 5, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (6, 'Day6',5, 1, 1);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (7, 'Day6',2, 4, 1);

---- Insert test data for Group B
INSERT INTO "group" (id, name, memberCount, dayCallCount) VALUES (2, 'Group B', 4, 5);

INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (6, 'Charlie', '678-901-2345', 2);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (7, 'Diana', '789-012-3456',   2);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (8, 'Oscar', '890-123-4567',   2);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (9, 'Peggy', '901-234-5678',   2);
--                                                                                     call,rec,group
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (8, 'Day1', 6, 7, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (9, 'Day2', 7, 6, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (10, 'Day3',8, 9, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (11, 'Day3',9, 8, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (12, 'Day4',6, 8, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (13, 'Day4',7, 9, 2);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (14, 'Day5',8, 6, 2);

---- Insert test data for Group C
INSERT INTO "group" (id, name, memberCount, dayCallCount) VALUES (3, 'Group C', 6, 7);

INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (10, 'Victor', '012-345-6789', 3);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (11, 'Wendy', '123-456-7890',  3);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (12, 'Xander', '234-567-8901', 3);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (13, 'Yvonne', '345-678-9012', 3);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (14, 'Zara', '456-789-0123',   3);
INSERT INTO "contact" (id, name, phone_number, group_id) VALUES (15, 'Ursula', '567-890-1234', 3);
--                                                                                     call,rec,group
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (15, 'Day1',10, 11, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (16, 'Day2',11, 10, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (17, 'Day3',12, 13, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (18, 'Day4',13, 12, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (19, 'Day5',14, 15, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (20, 'Day6',15, 14, 3);
INSERT INTO "call" (id, day_of_week, caller_id, receiver_id, group_id) VALUES (21, 'Day7',10, 12, 3);

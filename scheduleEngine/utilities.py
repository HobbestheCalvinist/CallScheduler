import csv,os
import logging

def create_directory_for_file(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")

def output_schedule_to_csv(schedule, filename,days_of_week,peoples_names):
    create_directory_for_file(filename)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Caller/Receiver'] + days_of_week
        writer.writerow(header)

        for person in peoples_names:
            row = [person]
            for day in days_of_week:
                row.append(schedule[day].get(person, ''))
            writer.writerow(row)

def output_schedule_to_LoggingConsole(schedule,days_of_week):
    for day in days_of_week:
        logging.debug(f"\n{day}:")
        for caller, receiver in schedule[day].items():
            logging.debug(f"{caller} calls {receiver}")


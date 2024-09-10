import csv,os
import logging

def create_directory_for_file(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
        return False
    
    elif os.path.exists(file_path):
        return True
    
    else:
        return False

def output_schedule_to_csv(schedule, fullFilePath):
    alreadyExists=create_directory_for_file(fullFilePath)

    if not alreadyExists:
        with open(fullFilePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ['Caller/Receiver'] + schedule.days_of_period
            writer.writerow(header)

            for person in schedule.peoples_names:
                row = [person]
                
                for day in schedule.days_of_period:
                    row.append(schedule.DayDictCallsofNames[day].get(person, ''))
                writer.writerow(row)
    else:
        logging.debug(f"{fullFilePath} already existed")
    

def output_schedule_to_LoggingConsole(schedule,days_of_period):
    for day in days_of_period:
        logging.debug(f"\n{day}:")
        for caller, receiver in schedule.DayDictCallsofNames[day].items():
            logging.debug(f"{caller} calls {receiver}")


import ScheduleGeneratorSieve

DAYS_OF_WEEK = ["Day1", "Day2", "Day3"]
PEOPLES_NAMES = ["Name1","Name2","Name3"]

for i in range(4,10):
    PEOPLES_NAMES.append(f"Name{i}")
    DAYS_OF_WEEK = ["Day1", "Day2", "Day3"]
    for d in range(4,8):
        DAYS_OF_WEEK.append(f"Day{i}")    
        ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_WEEK)
        print(f"people{len(PEOPLES_NAMES)} - days{len(DAYS_OF_WEEK)}")
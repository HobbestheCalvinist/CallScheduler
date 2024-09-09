import ScheduleGeneratorSieve
from config import RunConfig
import cProfile


DAYS_OF_PERIOD = []
PEOPLES_NAMES = []

def populateList(Prefix,endNum):
    myList = []
    for l in range(1,endNum+1):
        myList.append(Prefix+str(l))
    return myList


for i in range(4,10+1):
    #PEOPLES_NAMES.append(f"Name{i}")
    PEOPLES_NAMES = populateList("Name",i)
    for d in range(5,7+1):
        #DAYS_OF_PERIOD.append(f"Day{i}")
        rc = RunConfig()
        DAYS_OF_PERIOD = populateList("Day",d)
        
        rc.max_made_calls_per_period = len(DAYS_OF_PERIOD)-1
        rc.max_received_calls_per_period = len(DAYS_OF_PERIOD)-1
        #rc.max_made_calls_per_period = 3
        #rc.max_received_calls_per_period=5 
        with cProfile.Profile() as pr:
            ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_PERIOD,rc)
            pr.print_stats()
        #ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_PERIOD,rc)
        print(f"people{len(PEOPLES_NAMES)} - days{len(DAYS_OF_PERIOD)}")
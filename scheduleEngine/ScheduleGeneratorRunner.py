import ScheduleGeneratorSieve
from config import RunConfig



DAYS_OF_WEEK = []
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
        #DAYS_OF_WEEK.append(f"Day{i}")
        rc = RunConfig()
        DAYS_OF_WEEK = populateList("Day",d)
        
        rc.max_made_calls_per_week = len(DAYS_OF_WEEK)-1
        rc.max_received_calls_per_week = len(DAYS_OF_WEEK)-1
        
        ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_WEEK,rc)
        print(f"people{len(PEOPLES_NAMES)} - days{len(DAYS_OF_WEEK)}")
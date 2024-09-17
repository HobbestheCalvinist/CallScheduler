import ScheduleGeneratorSieve
from config import RunConfig
import cProfile

from Schedule_Contraints import *



def populateList(Prefix,endNum):
    myList = []
    for l in range(1,endNum+1):
        myList.append(Prefix+str(l))
    return myList

def populateNames(Prefix,endNum):
    myList = []
    for l in range(1,endNum+1):
        myList.append(Prefix + "_" + chr(97+l))
    return myList

def buildConstraintsSet1(rc):
    constraints = [
            NoRepeatedCallsConstraint(),
            NoReverseCallSameDayConstraint(),
            MaxCallsPerDayConstraint(rc.max_made_calls_per_day),
            MaxReceiverPerDayConstraint(rc.max_received_calls_per_day)
            
        ]
    
    return constraints

def buildConstraintSet2(rc):
    constraints = [
            NoRepeatedCallsConstraint(),
            NoReverseCallSameDayConstraint(),
            MaxCallsPerDayConstraint(rc.max_made_calls_per_day),
            MaxReceiverPerDayConstraint(rc.max_received_calls_per_day),
            MaxCallsPerPeriodConstraint(rc.max_made_calls_per_period),
            MaxReceiverPerPeriodConstraint(rc.max_received_calls_per_period),
            FullInteractionDayConstraint()
        ]
    
    return constraints


def runScheduleWithProfiler(DAYS_OF_PERIOD,PEOPLES_NAMES):
    rc = RunConfig()
    
    #rc.max_made_calls_per_period = len(DAYS_OF_PERIOD)-1
    #rc.max_received_calls_per_period = len(DAYS_OF_PERIOD)-1
    rc.max_made_calls_per_period = 3
    rc.max_received_calls_per_period=5 
    
    with cProfile.Profile() as pr:
        ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_PERIOD,rc)
        pr.print_stats()
    #ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_PERIOD,rc)
    print(f"people{len(PEOPLES_NAMES)} - days{len(DAYS_OF_PERIOD)}")

def runSchedule(DAYS_OF_PERIOD,PEOPLES_NAMES):
    rc = RunConfig()
    
    rc.max_made_calls_per_period = len(DAYS_OF_PERIOD)-1
    rc.max_received_calls_per_period = len(DAYS_OF_PERIOD)-1
    #rc.max_made_calls_per_period = 3
    #rc.max_received_calls_per_period=5 
    ScheduleGeneratorSieve.run(PEOPLES_NAMES,DAYS_OF_PERIOD,rc,buildConstraintSet2(rc))
        
    print(f"people{len(PEOPLES_NAMES)} - days{len(DAYS_OF_PERIOD)}")



def largeRun():
    for i in range(4,10+1):
        #PEOPLES_NAMES.append(f"Name{i}")
        nameList = populateList("Name",i)
        for d in range(5,7+1):
            #DAYS_OF_PERIOD.append(f"Day{i}")
            dayPeriodList = populateList("Day",d)
            runSchedule(dayPeriodList,nameList)

#largeRun()
#runScheduleWithProfiler(populateList("Day",6),populateList("Name",4))
runSchedule(populateList("Day",6),populateNames("Name",10))
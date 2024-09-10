import os
import random, logging, time
from Schedule_Run_Rules import StatTrack
import utilities 
from config import RunConfig
from Schedule_Person import SchedulePerson
from  Schedule_Contraints import *
from Schedule import Schedule

#when initialized, every day gets a fully built out call list 
def createCombinationCallsDict(names,days):
    callDict = {}
    combination_list = [(person1, person2) for idx1, person1 in enumerate(names) for idx2, person2 in enumerate(names) if idx1 != idx2]
    for day in days:
        callDict[day] = combination_list.copy()
    return callDict
  
def check_EveryOneHasACall_Today(schedule,day):
    a = list(schedule[day].keys())
    b = list(schedule[day].values())
    unique = list(set(a + b))
    if len(unique) != len(schedule.peoples_names):
        return False
    else:
        return True

def check_EveryOneHasACall_ThisPeriod(schedule):
    finishedDays = 0
    for day in schedule.days_of_period:
        goodDayInt = int(check_EveryOneHasACall_Today(schedule,day))
        finishedDays=finishedDays+goodDayInt
    return finishedDays


def buildSchedule(sched, c_list):

    assignments = 1
    while assignments > 0:
        assignments = 0
        # walk through the period looking for new assigned calls to make
        for day in sched.days_of_period:
            
            #check sieved list of calls to see if we have more options
            availableOptions = c_list[day]
            if availableOptions:
                                
                call = random.choice(availableOptions)
                sched.makeCall(day,call[0],call[1])
                assignments += 1
                
                # Apply each constraint to filter the call list options
                for constraint in sched.constraints:
                    constraint.apply(sched,c_list, call, day)
        
        
        #metgoals = bool(sched.getFinishedDays() == len(sched.days_of_period))           
        #metGoals = bool(check_EveryOneHasACall_ThisPeriod(schedule) == len(days_of_period))
        logging.debug("Made {} assignments this round".format(assignments))

    logging.debug("Finished Building Schedule")

def run(pNames, daysofperiod, rc):
    logging.basicConfig(level=rc.LogLevel)
    
    s_track = StatTrack(rc)
    folderName =F"People{len(pNames)}-Days{len(daysofperiod)}"
    
    while(s_track.loopCount<rc.MAX_ITERATIONS):
            
        #fully populated list, combinations of all calls resets every loop
        combinations_names_list = createCombinationCallsDict(pNames,daysofperiod) 
        constraints = [
            NoRepeatedCallsConstraint(),
            NoReverseCallSameDayConstraint(),
            MaxCallsPerDayConstraint(rc.max_made_calls_per_day),
            MaxReceiverPerDayConstraint(rc.max_received_calls_per_day)
            
        ]

        sched = Schedule(pNames,daysofperiod,constraints)
        buildSchedule(sched,combinations_names_list)
        
        outputResults=True
        if rc.doesEveryoneNeedCall:
            outputResults= bool(len(sched.days_of_period) == check_EveryOneHasACall_ThisPeriod(sched))  

        #TODO -> check that other larger rules to be applied here?
        if outputResults:
    
            s_track.currentTotalCalls = sched.calculateTotalCallsThisPeriod()
            s_track.currentDelta = sched.calculateDeltaCallsThisPeriod()
            s_track.currentNoCall = sched.calculateNoInteractionDaysThisPeriod()
            
            #there is a new lowest stat, we can output the schedule
            if s_track.checkAnyStatChangeForLower():

                filename = os.path.join(folderName,f"Missing-{s_track.currentNoCall}-calls-{s_track.currentTotalCalls}-delta-{s_track.currentDelta}.csv")
                fullPath = os.path.join(rc.OutputDirectory,filename)
                utilities.output_schedule_to_csv(sched, fullPath)
                logging.info(f"schedule_output{s_track.loopCount} has output csv -- {filename}")
                s_track.updateLowestValues()
              
        s_track.loopCount+=1
        if s_track.loopCount % 10000 ==0:
            print(s_track.getCurrentElapsedTime())

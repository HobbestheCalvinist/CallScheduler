import random, logging, time
import utilities 
from config import RunConfig
from Schedule_Person import SchedulePerson
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

def check_EveryOneHasACall_Week(schedule):
    finishedDays = 0
    for day in schedule.days_of_week:
        goodDayInt = int(check_EveryOneHasACall_Today(schedule,day))
        finishedDays=finishedDays+goodDayInt
    return finishedDays


def buildSchedule(sched, c_list):

    assignments = 1
    while assignments > 0:
        assignments = 0
        # walk through the week looking for new assigned calls to make
        for day in sched.days_of_week:
            
            #check sieved list of calls to see if we have more options
            availableOptions = c_list[day]
            if availableOptions:
                                
                call = random.choice(availableOptions)
                sched.makeCall(day,call[0],call[1])
                assignments += 1
                
                # sieve out the possibility of this exact call
                c_list[day].remove(call)
                
                # Apply each constraint to filter the call list
                for constraint in sched.constraints:
                    availableOptions = constraint.apply(sched,c_list, call, day)
        
        #TODO, everyone made a call add as a constraint                
        #metGoals = bool(check_EveryOneHasACall_Week(schedule) == len(days_of_week))
        logging.debug("Made {} assignments this round".format(assignments))

    logging.debug("Finished Building Schedule")


def filterExtraCalls(schedule):
    assignments = 9999
    while (assignments>0):
        assignments=0
        for day in schedule.days_of_week:
            tempSchedule = schedule.copy()
            highestCount = -9999
            callNumbers = []
            for person in schedule.people:
                p = schedule.getPersonByName[person]
                interactions = p.getMakingCallsCountDay(day) + p.getReceivingCallsCountDay(day)
                callNumbers.append(interactions)

            #TODO -> This code isn't updated to the new data structure!
            list(tempSchedule[day].keys())
            mostInteractionsPerson = list(schedule.people.keys())[callNumbers.index(max(callNumbers))]
            if mostInteractionsPerson in tempSchedule[day]:
                del tempSchedule[day][mostInteractionsPerson]

                if(check_EveryOneHasACall_Today(tempSchedule,day) and len(schedule.days_of_week)==check_EveryOneHasACall_Week(schedule)):
                    schedule = tempSchedule
                    schedule.people[mostInteractionsPerson].makingCallsDict[day]-=1
                    assignments+=1

def run(pNames, daysofweek, rc):
    logging.basicConfig(level=rc.LogLevel)
    run_Config = rc
    
    # Generate the schedule
    loopCount = 0
    fewestCalls = 9999
    smallestDelta = 9999 
    start = time.time()
    
    folderName =F"People{len(pNames)}-Days{len(daysofweek)}"
    
    while(loopCount<run_Config.MAX_ITERATIONS):
            
        combinations_names_list = createCombinationCallsDict(pNames,daysofweek) #fully populated list, combinations of all calls
        sched = Schedule(pNames,daysofweek)
        
        buildSchedule(sched,combinations_names_list)
        
        filterExtraCalls(sched,combinations_names_list)
        if run_Config.doesEveryoneNeedCall:
            outputResults=False
            finishedDays = check_EveryOneHasACall_Week(sched)
            if finishedDays==len(sched.days_of_week):
                outputResults=True
        else:
            outputResults=True
        
        if outputResults:
            sumTotalCalls = getTotalCallsThisWeek(people)
            currentDelta = getDeltaCallsThisWeek(people)
            
            if (sumTotalCalls<=fewestCalls or currentDelta<=smallestDelta ):
                filename = f"{folderName}\calls-{sumTotalCalls}-delta-{currentDelta}.csv"
                utilities.output_schedule_to_csv(sched, filename ,sched.days_of_week,sched.peoples_names)

                if (sumTotalCalls<fewestCalls):
                    fewestCalls = sumTotalCalls
                    logging.info(f"schedule_output{loopCount} has {sumTotalCalls} total calls")
                if (currentDelta<smallestDelta):
                    smallestDelta = currentDelta
                    logging.info(f"schedule_output{loopCount} has {smallestDelta} delta size")
        
        loopCount+=1
        if loopCount % 10000 ==0:
            end = time.time()
            duration = round(end - start,2)
            # time left = how many loop "chunks" multiplied by how long each "chunk" takes
            timeLeft = ((run_Config.MAX_ITERATIONS-loopCount)/loopCount)*duration/60
            print(str(loopCount) + " -- minutes left:" + str(timeLeft))

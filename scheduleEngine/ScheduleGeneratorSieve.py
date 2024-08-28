import random, logging, time
import utilities 
from config import RunConfig
from schedulePerson import schedulePerson


peoples_names = []
days_of_week = []

#when initialized, every day gets a fully built out call list 
def createCombinationCallsDict(names,days):
    callDict = {}
    combination_list = [(person1, person2) for idx1, person1 in enumerate(names) for idx2, person2 in enumerate(names) if idx1 != idx2]
    for day in days:
        callDict[day] = combination_list.copy()
    return callDict

def getTotalCallsThisWeek(people):
    total = 0
    for p in people.values():
                total+=p.getMakingCallsCount()
    return total

def getDeltaCallsThisWeek(people):
    delta=0
    for p in people.values():
                delta= delta+ abs(p.getMakingCallsCount()-p.getReceivingCallsCount())
    return delta

def filter_Caller_Week(c_list,caller):
    for day in days_of_week:
        callList = c_list[day].copy()
        for call in c_list[day]:
            if call[0] == caller.Name:
                callList.remove(call)
        c_list[day] = callList

    logging.debug(f"filter_Caller_Week {caller.Name} for all week")
    return c_list
    
def filter_Receiver_Week(c_list,receiver):
    for day in days_of_week:
        callList = c_list[day].copy()
        for call in c_list[day]:
            if call[1] == receiver.Name:
                callList.remove(call)
        c_list[day] = callList
        
    logging.debug(f"filter_Caller_Week {receiver.Name} for all week")
    return c_list

def filter_CallPair_Week(c_list,call):
    for day in days_of_week:
        callList = c_list[day].copy()
        if call in c_list[day]:
            callList.remove(call)
        c_list[day] = callList

    logging.debug("filter_CallPair_Week {0} from all week".format(call))
   
def filter_ReverseCallOption_Today(callListDay,day,caller,receiver):
    newlist= callListDay.copy()
    for call in callListDay:
        if call[0] == receiver.Name and call[1] == caller.Name:
            newlist.remove(call)
            logging.debug("filter_ReverseCallOptionForToday {0} from {1}".format(call,day))
    return newlist

def filter_AlreadyGotCalled_Today(callListDay,day,receiver):
    newlist= callListDay.copy()
    for call in callListDay:
        if  call[1] == receiver.Name:
            newlist.remove(call)
            logging.debug("filter_AlreadyGotCalled_Today {0} from {1}".format(call,day))
    
    return newlist

def filter_Caller_Today(callListDay,day,caller): 
    newlist= callListDay.copy()
    for call in callListDay:
            if  call[0] == caller.Name:
                newlist.remove(call)
    return newlist
    logging.debug("filter_Caller_Today {0} from {1}".format(caller.Name,day))

def check_EveryOneHasACall_Today(schedule,day):
    a = list(schedule[day].keys())
    b = list(schedule[day].values())
    unique = list(set(a + b))
    if len(unique) != len(peoples_names):
        return False
    else:
        return True

def check_EveryOneHasACall_Week(schedule):
    finishedDays = 0
    for day in days_of_week:
        goodDayInt = int(check_EveryOneHasACall_Today(schedule,day))
        finishedDays=finishedDays+goodDayInt
    return finishedDays


def buildSchedule(schedule,people,c_list):

    metGoals = False
    assignments=1
    #try assign one call per day until everyone has a call OR we run out of assignments to make
    while (not metGoals and assignments>0):
         
        assignments =0
        for day in days_of_week:
            availableOptions = c_list[day]
            if len(availableOptions)!=0:
                
                call = random.choice(availableOptions)
                caller = people[call[0]]
                caller.makeCall(day)
                receiver = people[call[1]]
                receiver.receiveCall(day)
                #makes the call
                assignments +=1
                schedule[day][caller.Name] = receiver.Name

                #no one has the exact same call twice in a week
                filter_CallPair_Week(c_list,call)

                #if you are getting called from someone, you don't call them back in the same day
                c_list[day] = filter_ReverseCallOption_Today(c_list[day],day,caller,receiver)

                if (caller.getMakingCallsCountDay(day) >= run_Config.max_made_calls_per_day):
                    c_list[day] = filter_Caller_Today(c_list[day],day,caller)

                #if you've already recieved 2 calls today, you are no longer an option
                if receiver.getReceivingCallsCountDay(day) >= run_Config.max_received_calls_per_day:
                    c_list[day] = filter_AlreadyGotCalled_Today(c_list[day],day,receiver)

                if (receiver.getReceivingCallsCount() >= run_Config.max_received_calls_per_week):
                    c_list = filter_Receiver_Week(c_list,receiver)
                    
                if (caller.getMakingCallsCount() >= run_Config.max_made_calls_per_week ):
                    c_list = filter_Caller_Week(c_list,caller)
            
        metGoals = bool(check_EveryOneHasACall_Week(schedule)==len(days_of_week))
        logging.debug("Made {} assignments this round".format(assignments))

    logging.debug("Finished Building Schedule")

def filterExtraCalls(schedule,people,day):
    assignments = 9999
    while (assignments>0):
        assignments=0
        for day in days_of_week:
            tempSchedule = schedule.copy()
            highestCount = -9999
            callNumbers = []
            for person in people:
                p = people[person]
                interactions = p.getMakingCallsCountDay(day) + p.getReceivingCallsCountDay(day)
                callNumbers.append(interactions)

            list(tempSchedule[day].keys())
            mostInteractionsPerson = list(people.keys())[callNumbers.index(max(callNumbers))]
            if mostInteractionsPerson in tempSchedule[day]:
                del tempSchedule[day][mostInteractionsPerson]

                if(check_EveryOneHasACall_Today(tempSchedule,day) and len(days_of_week)==check_EveryOneHasACall_Week(schedule)):
                    schedule = tempSchedule
                    people[mostInteractionsPerson].makingCallsDict[day]-=1
                    assignments+=1

def run(peepNames, daysofweek, rc):
    logging.basicConfig(level=rc.LogLevel)
    global peoples_names,days_of_week,run_Config
    peoples_names = peepNames
    days_of_week = daysofweek
    run_Config = rc
    
    # Generate the schedule
    loopCount = 0
    fewestCalls = 9999
    smallestDelta = 9999 
    start = time.time()
    folderName =F"People{len(peoples_names)}-Days{len(days_of_week)}"
    while(loopCount<run_Config.MAX_ITERATIONS):
            
        c_list = createCombinationCallsDict(peoples_names,days_of_week) #fully populated list, combinations of all calls
        people = {pname: schedulePerson(pname,days_of_week) for pname in peoples_names} # populated list of "People" object with names
        schedule = {day: {} for day in days_of_week} #empty schedule

        buildSchedule(schedule,people,c_list)
        filterExtraCalls(schedule,people,c_list)
        if run_Config.doesEveryoneNeedCall:
            outputResults=False
            finishedDays = check_EveryOneHasACall_Week(schedule)
            if finishedDays==len(days_of_week):
                outputResults=True
        else:
            outputResults=True
        
        if outputResults:
            sumTotalCalls = getTotalCallsThisWeek(people)
            currentDelta = getDeltaCallsThisWeek(people)
            
            if (sumTotalCalls<=fewestCalls or currentDelta<=smallestDelta ):
                filename = f"{folderName}\calls-{sumTotalCalls}-delta-{currentDelta}.csv"
                utilities.output_schedule_to_csv(schedule, filename ,days_of_week,peoples_names)

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

import random
import csv
import logging
import time
import os 

logging.basicConfig(level=logging.INFO)

peoples_names = []
days_of_week = []

max_made_calls_per_day = 1
max_received_calls_per_day = 2
max_made_calls_per_week = 0
max_received_calls_per_week = 0


MAX_ITERATIONS = 1000000



class Person:

    def __init__(self, name):
        self.Name = name
        self.makingCallsDict = {}
        self.receivingCallsDict = {}
        for day in days_of_week:
            self.makingCallsDict[day] = 0
            self.receivingCallsDict[day] = 0
    
    def makeCall(self,day):
        value = self.makingCallsDict[day]
        value+=1
        self.makingCallsDict[day]=value

    def receiveCall(self,day):
        self.receivingCallsDict[day]+=1
    
    def getMakingCallsCount(self):
        total = sum(self.makingCallsDict.values())
        return total

    def getReceivingCallsCount(self):
        total = sum(self.receivingCallsDict.values())
        return total
    
    def getMakingCallsCountDay(self,day):
        return self.makingCallsDict[day]

    def getReceivingCallsCountDay(self,day):
        return self.receivingCallsDict[day]

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

def createBlankSchedule():
    sdule={}
    for day in days_of_week:
        sdule[day] = {}
    return sdule

def createPeopleList():
    pList = {}
    for p in peoples_names:
        pList[p]=Person(p)
    return pList

def create_directory_for_file(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")

def output_schedule_to_csv(schedule, filename):
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

def writeOutSchedule(schedule):
    for day in days_of_week:
        logging.debug(f"\n{day}:")
        for caller, receiver in schedule[day].items():
            logging.debug(f"{caller} calls {receiver}")

def filter_CallerFromWeek(c_list,caller):
    for day in days_of_week:
        callList = c_list[day].copy()
        for call in c_list[day]:
            if call[0] == caller.Name:
                callList.remove(call)
        c_list[day] = callList

    logging.debug(f"filter_callerFromWeek {caller.Name} for all week")
    return c_list
    
def filter_ReceiverFromWeek(c_list,receiver):
    for day in days_of_week:
        callList = c_list[day].copy()
        for call in c_list[day]:
            if call[1] == receiver.Name:
                callList.remove(call)
        c_list[day] = callList
        
    logging.debug(f"filter_callerFromWeek {receiver.Name} for all week")
    return c_list

def filter_CallPairFromWeek(c_list,call):
    for day in days_of_week:
        callList = c_list[day].copy()
        if call in c_list[day]:
            callList.remove(call)
        c_list[day] = callList

    logging.debug("filter_CallPairFromWeek {0} from all week".format(call))
   
def filter_ReverseCallOptionForToday(callListDay,day,caller,receiver):
    newlist= callListDay.copy()
    for call in callListDay:
        if call[0] == receiver.Name and call[1] == caller.Name:
            newlist.remove(call)
            logging.debug("filter_ReverseCallOptionForToday {0} from {1}".format(call,day))
    return newlist

def filter_alreadyGotCalledToday(callListDay,day,receiver):
    newlist= callListDay.copy()
    for call in callListDay:
        if  call[1] == receiver.Name:
            newlist.remove(call)
            logging.debug("filter_alreadyGotCalledToday {0} from {1}".format(call,day))
    
    return newlist

def filter_CallerFromToday(callListDay,day,caller): 
    newlist= callListDay.copy()
    for call in callListDay:
            if  call[0] == caller.Name:
                newlist.remove(call)
    return newlist
    logging.debug("filter_CallerFromToday {0} from {1}".format(caller.Name,day))

def checkEveryOneHasACallToday(schedule,day):
    a = list(schedule[day].keys())
    b = list(schedule[day].values())
    unique = list(set(a + b))
    if len(unique) != len(peoples_names):
        return False
    else:
        return True

def checkEveryOneHasACall(schedule):
    finishedDays = 0
    for day in days_of_week:
        goodDayInt = int(checkEveryOneHasACallToday(schedule,day))
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
                filter_CallPairFromWeek(c_list,call)

                #if you are getting called from someone, you don't call them back in the same day
                c_list[day] = filter_ReverseCallOptionForToday(c_list[day],day,caller,receiver)

                if (caller.getMakingCallsCountDay(day) >= max_made_calls_per_day):
                    c_list[day] = filter_CallerFromToday(c_list[day],day,caller)

                #if you've already recieved 2 calls today, you are no longer an option
                if receiver.getReceivingCallsCountDay(day) >= max_received_calls_per_day:
                    c_list[day] = filter_alreadyGotCalledToday(c_list[day],day,receiver)

                if (receiver.getReceivingCallsCount() >= max_received_calls_per_week):
                    c_list = filter_ReceiverFromWeek(c_list,receiver)
                    
                if (caller.getMakingCallsCount() >= max_made_calls_per_week ):
                    c_list = filter_CallerFromWeek(c_list,caller)
            
        metGoals = bool(checkEveryOneHasACall(schedule)==len(days_of_week))
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

                if(checkEveryOneHasACallToday(tempSchedule,day) and len(days_of_week)==checkEveryOneHasACall(schedule)):
                    schedule = tempSchedule
                    people[mostInteractionsPerson].makingCallsDict[day]-=1
                    assignments+=1

def run(peepNames, daysofweek ):

    global peoples_names,days_of_week ,max_made_calls_per_week,max_received_calls_per_week
    peoples_names = peepNames
    days_of_week = daysofweek
    max_made_calls_per_week = len(days_of_week)-1
    max_received_calls_per_week = len(days_of_week)-1
    
    # Generate the schedule
    loopCount = 0
    fewestCalls = 9999
    smallestDelta = 9999 
    start = time.time()
    folderName =F"People{len(peoples_names)}-Days{len(days_of_week)}"
    while(loopCount<MAX_ITERATIONS):
            
        c_list = createCombinationCallsDict(peoples_names,days_of_week)
        people = createPeopleList()
        schedule = createBlankSchedule()
        buildSchedule(schedule,people,c_list)
        filterExtraCalls(schedule,people,c_list)
        finishedDays = checkEveryOneHasACall(schedule)
        if finishedDays==len(days_of_week):
            
            sumTotalCalls = getTotalCallsThisWeek(people)
            currentDelta = getDeltaCallsThisWeek(people)
            #output_schedule_to_csv(schedule, f"{folderName}\calls-{sumTotalCalls}-delta-{currentDelta}.csv")

            if (sumTotalCalls<=fewestCalls or currentDelta<=smallestDelta ):
                            
                output_schedule_to_csv(schedule, f"{folderName}\calls-{sumTotalCalls}-delta-{currentDelta}.csv")

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
            timeLeft = ((MAX_ITERATIONS-loopCount)/loopCount)*duration/60
            print(str(loopCount) + " -- minutes left:" + str(timeLeft))

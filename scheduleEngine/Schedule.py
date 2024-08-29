from Schedule_Person import Schedule_Person
import Schedule_Contraints

class Schedule:

    
    def __init__(self, peoples_names, days_of_week,constraints):
        self.days_of_week = days_of_week
        self.peoples_names = peoples_names
        self.people = {pname: Schedule_Person(pname,days_of_week) for pname in peoples_names}
        self.constraints = constraints
        self.DayDictCallsofNames = {day: {} for day in days_of_week}
        ###  dictionary DAY (Key: String Day Name, Value: Dictionary Names )
        ###------- dictionary NAMES (Key: String Caller, Value: String Receiver Name)
        ### i.e. DayDictCallsofNames[Monday][Name] = Name2


    def getTotalCallsThisWeek(self):
        total = 0
        for p in self.people.values():
                    total+=p.getMakingCallsCount()
        return total

    def getDeltaCallsThisWeek(self):
        delta=0
        for p in self.people.values():
                    delta= delta+ abs(p.getMakingCallsCount()-p.getReceivingCallsCount())
        return delta
    
    def getPersonByName(self,name):
        p = self.people[name]
        return p
    
    def makeCall(self,day,callerName,receiverName):
        callerPerson = self.getPersonByName(callerName)
        receiverPerson = self.getPersonByName(receiverName)
        
        callerPerson.makeCall(day)
        receiverPerson.receiveCall(day)
        
        self.DayDictCallsofNames[day][callerName] = receiverName
        
    def getFinishedDays():
        #TODO, need to run this through a contraint check
        #for day in days_of_week:
        #    goodDayInt = int(check_EveryOneHasACall_Today(schedule,day))
        #    
        #finishedDays=finishedDays+goodDayInt
        return 0
    
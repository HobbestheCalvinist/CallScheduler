from Schedule_Person import SchedulePerson
import Schedule_Contraints

class Schedule:

    
    def __init__(self, peoples_names, days_of_period,constraints):
        self.days_of_period = days_of_period
        self.peoples_names = peoples_names
        self.people = {pname: SchedulePerson(pname,days_of_period) for pname in peoples_names}
        self.constraints = constraints
        self.DayDictCallsofNames = {day: {} for day in days_of_period}
        ###  dictionary DAY (Key: String Day Name, Value: Dictionary Names )
        ###------- dictionary NAMES (Key: String Caller, Value: String Receiver Name)
        ### i.e. DayDictCallsofNames[Monday][Name] = Name2


    def getTotalCallsThisperiod(self):
        total = 0
        for p in self.people.values():
                    total+=p.getMakingCallsCount()
        return total

    def getDeltaCallsThisperiod(self):
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


    def check_EveryOneHasACall_Today (self,day):
          dayOfCalls = self.DayDictCallsofNames[day]
          return 0
    

    def getFinishedDays(self):
        finishedDays=0
        for day in self.days_of_period:
            goodDayInt = int(self.check_EveryOneHasACall_Today(day))
            
            finishedDays=finishedDays+goodDayInt
        return finishedDays
    

    
class schedulePerson:
    
    def __init__(self, name,days_of_week):
        self.Name = name
        self.makingCallsDict = {}
        self.receivingCallsDict = {}
        self.madeCalls = 0
        self.receivedCalls = 0
        for day in days_of_week:
            self.makingCallsDict[day] = 0
            self.receivingCallsDict[day] = 0
    
    def makeCall(self,day):
        value = self.makingCallsDict[day]
        value+=1
        self.makingCallsDict[day]=value
        self.madeCalls +=1

    def receiveCall(self,day):
        self.receivingCallsDict[day]+=1
        self.receivedCalls +=1
        
    def getMakingCallsCount(self):
        return self.madeCalls

    def getReceivingCallsCount(self):
        return self.receivedCalls
    
    def getMakingCallsCountDay(self,day):
        return self.makingCallsDict[day]

    def getReceivingCallsCountDay(self,day):
        return self.receivingCallsDict[day]
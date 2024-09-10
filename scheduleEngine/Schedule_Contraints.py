
''' Contraints are ways to narrow down the 
'''
class Constraint:
    def apply(self, schedule, call_list , call, day):
        """
        Applies the constraint and returns the modified call list.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class NoRepeatedCallsConstraint(Constraint):
    def apply(self, schedule,call_list , call, day):
        """
        Removes the call pair from the list if they have already interacted this period.
        """
        for day in call_list.keys():
            modList=None
            modified = False
            
            if call in call_list[day]:
                if modList is None: #copying memory objects is expensive, so optimize when we copy
                    modList = call_list[day].copy()
                
                modList.remove(call)
                modified =True

            #assign the modified call list back into the object
            if modified == True:
                call_list[day] = modList

class NoReverseCallSameDayConstraint(Constraint):
    def apply(self, schedule, call_list , call, day):
     
        caller, receiver = call
        if (receiver, caller) in call_list[day]:       
            dayListCalls = call_list[day]
            dayListCalls.remove((receiver, caller))


class MaxCallsPerDayConstraint(Constraint):
    def __init__(self, max_made_calls_per_day):
        self.max_made_calls_per_day = max_made_calls_per_day

    def apply(self, schedule, call_list , call, day):
        modList = None
        modified = False

        caller = schedule.getPersonByName(call[0])
        if caller.getMakingCallsCountDay(day) >= self.max_made_calls_per_day:
            for currCall in call_list[day]:
                #remove any interaction where this person is the caller
                if currCall[0] == call[0]:
                    if modList is None: #copying memory objects is expensive, so optimize when we copy
                        modList=call_list[day].copy()
                    modList.remove(currCall)
                    modified = True
            
        if modified == True:
            call_list[day] = modList

class MaxReceiverPerDayConstraint(Constraint):
    def __init__(self, max_received_calls_per_day):
        self.max_received_calls_per_day = max_received_calls_per_day

    def apply(self, schedule, call_list , call, day):
        modList = None
        modified = False

        reciever = schedule.getPersonByName(call[1])
        if reciever.getReceivingCallsCountDay(day) >= self.max_received_calls_per_day:
            for currCall in call_list[day]:
                #remove any interaction where this person is the caller
                if currCall[1] == call[1]:
                    if modList is None: #copying memory objects is expensive, so optimize when we copy
                        modList=call_list[day].copy()
                    modList.remove(currCall)
                    modified = True
            
        if modified == True:
            call_list[day] = modList


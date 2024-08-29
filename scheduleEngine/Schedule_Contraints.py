
class Constraint:
    def apply(self, schedule, call_list , call, day):
        """
        Applies the constraint and returns the modified call list.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class NoRepeatedCallsConstraint(Constraint):
    def apply(self, schedule,call_list , call, day):
        """
        Removes the call pair from the list if they have already interacted this week.
        """
        for day in call_list.keys():
            callList = call_list[day].copy()
            if call in call_list[day]:
                callList.remove(call)
            call_list[day] = callList

class NoReverseCallSameDayConstraint(Constraint):
    def apply(self, schedule, call_list , call, day):
        new_list = call_list.copy()
        for call in call_list[day]:
            caller, receiver = call
            if (receiver.Name, caller.Name) in new_list:
                new_list.remove((receiver.Name, caller.Name))
        return new_list

class MaxCallsPerDayConstraint(Constraint):
    def __init__(self, max_made_calls_per_day):
        self.max_made_calls_per_day = max_made_calls_per_day

    def apply(self, schedule, call_list , call, day):
        new_list = call_list.copy()
        for call in call_list[day]:
            caller = call[0] #TODO, this used to call out to the "People" object. Might need to fix
            if caller.getMakingCallsCountDay(day) >= self.max_made_calls_per_day:
                new_list.remove(call)
        return new_list

class MaxReceiverPerDayConstraint(Constraint):
    def __init__(self, max_received_calls_per_day):
        self.max_received_calls_per_day = max_received_calls_per_day

    def apply(self, schedule, call_list , call, day):
        newlist = call_list.copy()
        caller = call[0]
        receiver = call[1]
        for currCall in call_list[day]:
            if currCall[0] == receiver.Name and currCall[1] == caller.Name:
                newlist.remove(call)
                
        return newlist


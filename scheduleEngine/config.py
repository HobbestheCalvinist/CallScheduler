import logging

class RunConfig:
    MAX_ITERATIONS = 1000000
    max_made_calls_per_day = 1
    max_received_calls_per_day = 2
    max_made_calls_per_week = 0
    max_received_calls_per_week = 0
    doesEveryoneNeedCall = False
    LogLevel = logging.INFO
    
    @property
    def max_iterations(self):
        return self.MAX_ITERATIONS

    @max_iterations.setter
    def max_iterations(self, value):
        self.MAX_ITERATIONS = value

    @property
    def everyone_needs_call(self):
        return self.doesEveryoneNeedCall

    @everyone_needs_call.setter
    def everyone_needs_call(self, value):
        self.doesEveryoneNeedCall = value
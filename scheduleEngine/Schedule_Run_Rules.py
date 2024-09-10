import time

class StatTrack:

    def __init__(self,rc):

        self.runConfig = rc
        self.startTime = time.time()
        self.loopCount = 0

        self.lowestTotalCalls = 9999
        self.lowestDelta = 9999
        self.lowestNoCall = 9999

        self.currentTotalCalls = 0
        self.currentDelta = 0
        self.currentNoCall = 0

    def resetCurrentRun(self):
        self.currentTotalCalls = 0
        self.currentDelta = 0
        self.currentNoCall = 0

    def getCurrentElapsedTime(self):
        end = time.time()
        duration = round(end - self.startTime,2)
        # time left = how many loop "chunks" multiplied by how long each "chunk" takes
        timeLeft = ((self.runConfig.MAX_ITERATIONS-self.loopCount)/self.loopCount)*duration/60
        returnValue = (str(self.loopCount) + " -- minutes left:" + str(timeLeft))
        return returnValue
    
    def checkAnyStatChangeForLower(self):
        pairs=[]
        pairs.append((self.lowestTotalCalls,self.currentTotalCalls))
        pairs.append((self.lowestDelta,self.currentDelta))
        pairs.append((self.lowestNoCall,self.currentNoCall))

        # use different operators for comparison, like any difference, or greater than, etc...
        #any(a != b for a, b in pairs) 

        returnValue= any(b < a for a, b in pairs)

        return returnValue

    def updateLowestValues(self):
        if (self.currentTotalCalls<self.lowestTotalCalls):
                    self.lowestTotalCalls = self.currentTotalCalls

        if (self.currentDelta<self.lowestDelta):
                    self.lowestDelta = self.currentDelta
        
        if (self.currentNoCall<self.lowestNoCall):
                    self.lowestNoCall = self.currentNoCall
# CS4365 HW2 Project Part 2
# Ben Rust bjr170630

# py main.py ex1.var ex1.con none
# py main.py ex2.var ex2.con fc
# py main.py ex3.var ex3.con none

import sys
import copy

# Main function which takes 3 commandline arguments and tries to find
# a valid solution to the problems described in the files
def main():
    # ---------------------------
    # read in command prompt & files
    # populate cspProblem1
    # run cspProblem.getSolution()
    # ---------------------------

    print("\n")
    # create cspProblem variable
    csp = cspProblem()

    # fill csp with the data from the command line & files
    csp.fill(sys.argv[1], sys.argv[2], sys.argv[3])

    # get the solution
    csp.getSolution()



# class of the entire CSP problem
class cspProblem:
    varList = []
    varDomains = [] * 1
    conList = []
    forChecking = None

    # Fill the varList and varDomains variables
    def fillVar(self, varFilename):
        varFile = open(varFilename, "r")

        i = 0
        # Fill varList
        for line in varFile:
            # Fill varList
            self.varList.append(line[0])

            # Fill varDomains
            j = 0
            l = []
            values = line.split()
            values.pop(0)
            for x in values:
                l.append(x)
            self.varDomains.append(l)
            i = i + 1

        # Unnecessary printing as proof
        #print(self.varList, "\n")
        #print(self.varDomains, "\n")

        varFile.close()

    # Fill the conList variable
    def fillCon(self, conFilename):
        conFile = open(conFilename, "r")

        for line in conFile:
            self.conList.append(line.rstrip())

        #print(self.conList)
        conFile.close()

    # Fill the forChecking variable
    def fillForCheck(self, forCheck):
        if (forCheck == "fc"):
            #print("\nYes FC\n")
            forChecking = True
        elif (forCheck == "none"):
            #print("\nNo FC\n")
            forChecking = False
        else:
            #print("\nUnsure if FC, defaulting to yes \n")
            forChecking = True

    # Fill the cspProblem with the values/files from the commandLine
    def fill(self, varFilename, conFilename, forCheck):
        self.fillVar(varFilename)
        self.fillCon(conFilename)
        self.fillForCheck(forCheck)
        return None;

    # Returns either a failure or
    def getSolution(self):
        # creates root node
        # create a stack of nodes
        # while (queue not empty)
        #   figure out if the current node violates any constraints
        #   if so
        #       print out the values of the node & "failure"
        #   if not
        #       if it has all values filled
        #           print values and print success
        #           end function here
        #       if it doesn't have all values filled
        #           get successors & add them to the queue
        # ----------------------------------------------------

        # creates root node
        varV = [None] * len(self.varList)
        ordV = [None] * len(self.varList)
        cspRoot = cspNode(None, self.varList, self.varDomains, self.conList, self.forChecking, varV, ordV)

        # create a stack of nodes (insert lowest priority values first)
        stack = []
        stack.append(cspRoot)

        while stack: #while stack has values
            temp = stack.pop()

            #print("\n\nNew node popped off the stack, values are", temp.varValues)
            #for x in range(0, len(stack)):
            #    print("\n\tRemaining stacc values: ", stack[x].varValues)

        #   figure out if the current node violates any constraints
            #   if so
            if(not temp.isCorrect()):
                # Print out values
                temp.printValues()
                print ("\tFailure")
                #TODO      replace "return None" with "continue"
                # once a non-hardcoded getSuccessor() is working
                #return None
                continue

            #   if the current values don't violate constraints
            # if all the values are filled, it's a success
            # if not, get the successors
            else:
                hasAllValues = True
                # Set flag to false is any variable is missing a value
                for x in range(0, len(temp.varList)):
                    if (temp.varValues[x] is None):
                        hasAllValues = False

                #if it has all values filled
                if hasAllValues:
                    # print values and print success
                    temp.printValues()
                    print("\tSolution")
                    return None
                    # end function here
                # if it doesn't have all values filled
                else:
                    # get successors & add them to the queue
                    # Note: this will return the worst successors first so they're
                    # last to be popped
                    #print("Getting successors\n")
                    l = temp.getSuccessors()
                    if l is None:
                        continue
                    else:
                        for y in l:
                            #print("Adding y to stack, y values = ", y.varValues)
                            stack.append(y)

        print ("\n\nStack empty without finding a solution, complete failure\n")
        return None

# Class of an individual CSP node
class cspNode:
    parent = None #parent node
    varList = []
    varDomains = []
    varValues = []
    conList = []
    forChecking = None
    orderVars = []

    # Initialize all variables
    def __init__(self, par, varL, varD, conL, fCheck, varV, ordV):
        #print("Making new CSP node, values are:", varV, "\n\n")
        self.parent = par
        self.varList = varL
        self.varDomains = varD
        self.conList = conL
        self.forChecking = fCheck
        self.varValues = varV
        self.orderVars = ordV

    # Returns true if the current values for the
    # variables do not violate any constraint
    # NOTE: unassigned variables do NOT violate constraints
    def isCorrect(self):
        # For all constraints
        for x in self.conList:
            # Check if the constraint is correct, and return false immediately if one is broken
            if(self.isConCorrect(x) is False):
                return False
        return True


    # Returns true/false if the constraint passed in is followed/broken
    def isConCorrect(self, con):
        l = con.split()

        # if one of the variables in the constraint has
        # no value, skip
        if ((self.varValues[self.varList.index(l[0])] is None) or \
                (self.varValues[self.varList.index(l[2])] is None)):
            #print("At least one of the 2 values in constraint ", con, " is unassigned")
            return True

        if (l[1] == ">"):
            if (self.varValues[self.varList.index(l[0])] > self.varValues[self.varList.index(l[2])]):
                #print("constraint: ", con, " is not broken")
                return True
            else:
                #print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "="):
            if (self.varValues[self.varList.index(l[0])] == self.varValues[self.varList.index(l[2])]):
                #print("constraint: ", con, " is not broken")
                return True
            else:
                #print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "<"):
            if (self.varValues[self.varList.index(l[0])] < self.varValues[self.varList.index(l[2])]):
                #print("constraint: ", con, " is not broken")
                return True
            else:
                #print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "!"):
            if (self.varValues[self.varList.index(l[0])] is not self.varValues[self.varList.index(l[2])]):
                #print("constraint: ", con, " is not broken")
                return True
            else:
                #print("constraint: ", con, " is broken")
                return False;

        else:
            print("Middle value (should be >, =, <, or !) is not recognized")
            return False
        return True

    # TODO code this
    # returns a list of nodes that are successors to this node
    # a successor all the next possible values for
    def getSuccessors(self):
        list = []

        # returns & stores the position of the next variable in the varL list
        nextVar = self.nextVar()
        self.orderVars.append(nextVar)

        # TODO
        # For that variable, return all possible values,
        nextVals = self.nextVals(nextVar)

            # TODO  Forward Checking
            # For each variable domain in the nodes you're about to create,
            # use forward checking here to delete constraint-violating values from domains
            # after doing so, if any domain is empty, return failure?
                # Figure out how to return failure from this function

        # and create cspNodes with each of these values, amd store them in the list
        # from worst to last
        for x in nextVals:
            self.varValues[self.varList.index(nextVar)] = x
            # TODO - set the new domains according to constraints and value

            tempCSPnode = cspNode(self, self.varList, self.varDomains, self.conList, self.forChecking, self.varValues, self.orderVars)
            #print("Appending CSP node w/ values:", tempCSPnode.varValues)
            list.append(copy.deepcopy(tempCSPnode))
            #print("Current list, list = ")
            #for y in list:
            #    print("\n\t", y.varValues)


# Hardcoded success case ----------------------------
#        print("\n   ----Hardcoded success setup for var1 con1:---- \n\n")
#        self.varValues = [5, 2, 2, 1, 1, 1]
#        next = cspNode(self, self.varList, self.varDomains, self.conList, self.forChecking, self.varValues)
# Hardcoded failure case
        #        print("\n   ----Hardcoded failure setup for var1 con1:---- \n\n")
        #        self.varValues = [5, 2, 1, 1, 1, 1]
        #        next = cspNode(self, self.varList, self.varDomains, self.conList, self.forChecking, self.varValues)
# ------------------------

        #print("Returning successors\n")
        # IMPORTANT: for list, store the worst states first and the
        # best states last
        #list.append(next)      For the hardcoded solutions
        #print("Right before returning list, list = ")
        #for y in list:
        #    print("\n\t", y.varValues)

        return list

    # Prints out the current values
    def printValues(self):
        #print("Ought to print values rn")
        # Must find a way to print out values
        # in the order that they were assigned
        for x in range(0, len(self.orderVars)):
            if(self.orderVars[x] is None):
                continue
            if (x < (len(self.orderVars)-1)):
                print(self.orderVars[x] + "=" + self.varValues[self.varList.index(self.orderVars[x])] + ",", end=" ")
            else:
                print(self.orderVars[x] + "=" + self.varValues[self.varList.index(self.orderVars[x])], end=" ")
        return None

    # Returns the next unassigned variable
    def nextVar(self):
        # something to hold the results of the functions
        nextVar = None

        # make a list of unassigned variables to pass into each function
        # do it once now instead of once in each function
        blankVars = []
        for x in self.varList:
            if(self.varValues[self.varList.index(x)] is None):
                blankVars.append(x)

        if (len(blankVars) is 0):
            print("Major problem, somehow searching for another variable with no blank variables left")
            exit -1

        if (len(blankVars) is 1):
            return blankVars[0]

        nextVar = self.getMCedVar(blankVars)
        #print("Most constrained var is :", nextVar)
        if nextVar is False:
            nextVar = self.getMCingVar(blankVars)
            #print("Most constraining var is :", nextVar)

        if nextVar is False:
            nextVar = self.getABVar(blankVars)
            #print("Most alphabetical var is :", nextVar)

        return nextVar

    # Returns the most constrained unassigned variable
    # If two variables are equally constrained, returns false
    def getMCedVar(self, blankVars):
        #print("Getting the most constrained variable:")
        nextVar = False
        nextVarLenDomain = 100000 # should be max num but whatever

        # for all unassigned variables
        for x in blankVars:
            # if the number of values is equal to the current nextVar's
            if (len(self.varDomains[self.varList.index(x)]) == nextVarLenDomain):
                # replace it with False
                nextVar = False

            # if the number of values is less than the current nextVar's
            if (len(self.varDomains[self.varList.index(x)]) < nextVarLenDomain):
                # replace it with this variable
                nextVar = x
                #print(nextVar, ": ", len(self.varDomains[self.varList.index(x)]), "\n")
                nextVarLenDomain = len(self.varDomains[self.varList.index(x)])

        return nextVar

    # Returns the most constraining unassigned variable
    # If two variables are equally constraining, returns false
    # Note: returns unassigned variable with most constraints on other variables
    #   Does NOT return the UV that eliminates the most other values from other
    #   variable's domains
    def getMCingVar(self, blankVars):
        #print("Getting the most constraining variable")
        varNumCons = []

        # For each blank variable
        for x in blankVars:
            # Count the number of constraints that it is in
            # where the other variable's value is also none
            numCons = 0
            for y in self.conList:
                # if the constraint where one thing is x,
                # and the other is a blank variable numCons++
                if((y[0] in blankVars) and (y[2] in blankVars) and \
                        ((y[0] is x) or (y[2] is x))):
                    numCons = numCons + 1
            varNumCons.append(numCons)

        maxCons = max(varNumCons)
        numMaxes = varNumCons.count(maxCons)
        if (numMaxes == 1):
            return blankVars[varNumCons.index(maxCons)]

        return False

    # Returns the next unassigned variable alphabetically
    def getABVar(self, blankVars):
        #print("Getting the alphabetically next value")
        blankVars.sort()

        return blankVars[0]

    # TODO
    # Returns a list of all possible values for the selected variable
    # Specifically in the order of least-constricting and then alphabetical
    def nextVals(self, var):
        #print("Creates a list of the next values")

        # make a list of all the unassigned values
        unassignedVals = copy.deepcopy(self.varDomains[self.varList.index(var)])
        # make a list to hold all the values
        # valList is in the order least restricting -> most restricting
        #   or A -> Z       append A first
        valList = []
        # make a variable to temporarily hold the next best value
        tempVal = None
        tempList = None

        # for the number of possible values
            # append the most desired value to the list
            # ideally the last-constraining, but in a tie, numberically
        for x in range(0, len(unassignedVals)):
            #print("yo")
            # return a list of all unassigned values tied for least constraining value(s)
            tempList = self.getLCVal(var, unassignedVals)
            # if that list has only 1 value
            if (len(tempList) is 1):
                # tempVal = that value, and delete that value from unassignedVals
                tempVal = tempList[0]

            else:
                # return the numerically lowest of those values
                tempVal = self.getNumVal(tempList)
                #print("tempVal, should be numerically lowest, = ", tempVal)
                # tempVal = that value, and delete that value from unassignedVals

            # delete the tempVal from unassignedVals
            unassignedVals.remove(tempVal)
            # add tempVal to the valList
            valList.append(tempVal)

        # Since valList is in the order least->most restricting, or A->Z
        # Flip it before returning it
        valList.reverse()

        #print("returning valList, it is:", valList)
        return valList

    # TODO
    # Returns a list of the least constraining unassigned value
    def getLCVal(self, var, unassignedVals):
        #print("Getting the least constraining value(s)")
        tempList = [0] * len(self.varDomains[self.varList.index(var)])
        locList = []
        blankVars = []

        for x in self.varList:
            if(self.varValues[self.varList.index(x)] is None):
                blankVars.append(x)

        # For every value of the next variable
        for x in range(0, len(unassignedVals)):
            # for each unassigned variable
            for y in blankVars:
                #print(blankVars)
                # calculate the size of the remaining domain after assigning x to var
                #print("here's the total # of remaining domains after assigning ", unassignedVals[x], "to var ", var)
                if (var is not y):
                    tempList[x] = tempList[x] + self.remainingDomain(var, y, unassignedVals[x])
                    #print("for ", var, " = ", unassignedVals[x], "; blankVar is ", y, "; remDom = ", tempList[x])

        # find max value in the list
        maxVal = max(tempList)
        # for the location of the max values, add uV[loc] to tempList
        for x in range(0, len(unassignedVals)):
            if tempList[x] is maxVal:
                locList.append(unassignedVals[x])

        #print("List of least constraining values: ", locList)
        return locList

    # Takes the next varible, an unassigned variable, and a value for the next
    # variable and returns the
    def remainingDomain(self, currVar, otherVar, currVal):
        # Calculate the remaining domain of otherVar after currVar is assigned a a value
        # for every constraint

        # This flag will turn to false if there's a constraint involving both
        # the current variable and the other variable
        # If not, we can simply return the original domain of otherVar
        noConsFlag = True

        remDom = 0
        for z in self.conList:
            x = z.split()
            #print("x = ", x, "; x[0] = ", x[0], "x[1] = ", x[1], "x[2] = ", x[2])
            for y in self.varDomains[self.varList.index(otherVar)]:
#                print("currVar = ", currVar, "; x[0] = ", x[0], "; otherVar = ", otherVar, "; x[2] = ", x[2])
                # if that constraint contains currVar
                if((currVar is x[0]) and (otherVar is x[2])):
                    noConsFlag = False;
                    if(x[1] == "<"):
                        if(currVal < y):
                            remDom = remDom + 1

                    elif(x[1] == ">"):
                        if(currVal > y):
                            remDom = remDom + 1

                    elif(x[1] == "="):
                        if(currVal is y):
                            remDom = remDom + 1

                    elif(x[1] == "!"):
                        if(currVal is not y):
                            remDom = remDom + 1

                elif((currVar is x[2]) and (otherVar is x[0])):
                    noConsFlag = False;
                    if(x[1] == "<"):
                        if(y < currVal):
                            remDom = remDom + 1

                    elif(x[1] == ">"):
                        if(y > currVal):
                            remDom = remDom + 1

                    elif(x[1] == "="):
                        if(currVal is y):
                            remDom = remDom + 1

                    elif(x[1] == "!"):
                        if(currVal is not y):
                            remDom = remDom + 1

                #print("After y = ", y, ", remDom = ", remDom)
            #print("After x = ", x, ", remDom = ", remDom)

        if (noConsFlag is True):
            remDom = remDom + len(self.varDomains[self.varList.index(otherVar)])

        #print("\t remdom = ", remDom)
        return remDom

    # Returns the next unassigned values numerically
    def getNumVal(self, unassignedVals):
        #print("Getting the numerically next value of the tied for LCVs")
        unassignedVals.sort()
        return unassignedVals[0]

# main
if __name__ == '__main__':
    main()


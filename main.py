# CS4365 HW2 Project Part 2
# Ben Rust bjr170630

# py main.py ex1.var ex1.con none
# py main.py ex2.var ex2.con fc
# py main.py ex3.var ex3.con none

import sys

# Main function which takes 3 commandline arguments and tries to find
# a valid solution to the problems described in the files
def main():
    # ---------------------------
    # read in command prompt & files
    # populate cspProblem1
    # run cspProblem.getSolution()
    # ---------------------------

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
        print(self.varList, "\n")
        print(self.varDomains, "\n")

        varFile.close()

    # Fill the conList variable
    def fillCon(self, conFilename):
        conFile = open(conFilename, "r")

        for line in conFile:
            self.conList.append(line.rstrip())

        print(self.conList)
        conFile.close()

    # Fill the forChecking variable
    def fillForCheck(self, forCheck):
        if (forCheck == "fc"):
            print("\nYes FC\n")
            forChecking = True
        elif (forCheck == "none"):
            print("\nNo FC\n")
            forChecking = False
        else:
            print("\nUnsure if FC, defaulting to yes \n")
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
        cspRoot = cspNode(None, self.varList, self.varDomains, self.conList, self.forChecking, varV)

        # create a stack of nodes (insert lowest priority values first)
        stack = []
        stack.append(cspRoot)

        while stack: #while stack has values
            temp = stack.pop()

        #   figure out if the current node violates any constraints
            #   if so
            if(not temp.isCorrect()):
                # Print out values
                temp.printValues()
                print ("\tFailure")
                #TODO      replace "return None" with "continue"
                # once a non-hardcoded getSuccessor() is working
                return None

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
                    print("Getting successors\n")
                    l = temp.getSuccessors()
                    if l is None:
                        continue
                    else:
                        for y in l:
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

    # Initialize all variables
    def __init__(self, par, varL, varD, conL, fCheck, varV):
        print("Initializing\n\n")
        self.parent = par
        self.varList = varL
        self.varDomains = varD
        self.conList = conL
        self.forChecking = fCheck
        self.varValues = varV


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
                (self.varValues[self.varList.index(l[0])] is None)):
            print("At least one of the 2 values in constraint ", con, " is unassigned")
            return True

        if (l[1] == ">"):
            if (self.varValues[self.varList.index(l[0])] > self.varValues[self.varList.index(l[2])]):
                print("constraint: ", con, " is not broken")
                return True
            else:
                print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "="):
            if (self.varValues[self.varList.index(l[0])] == self.varValues[self.varList.index(l[2])]):
                print("constraint: ", con, " is not broken")
            else:
                print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "<"):
            if (self.varValues[self.varList.index(l[0])] < self.varValues[self.varList.index(l[2])]):
                print("constraint: ", con, " is not broken")
            else:
                print("constraint: ", con, " is broken")
                return False;

        elif (l[1] == "!"):
            if (self.varValues[self.varList.index(l[0])] is not self.varValues[self.varList.index(l[2])]):
                print("constraint: ", con, " is not broken")
            else:
                print("constraint: ", con, " is broken")
                return False;

        else:
            print("Middle value (should be >, =, <) is not recognized")
            return False
        return True

    # TODO code this
    # returns a list of nodes that are successors to this node
    # a successor all the next possible values for
    def getSuccessors(self):
        list = []

# Hardcoded success case ----------------------------
        print("\n   ----Hardcoded success setup for var1 con1:---- \n\n")
        self.varValues = [5, 2, 2, 1, 1, 1]
        next = cspNode(self, self.varList, self.varDomains, self.conList, self.forChecking, self.varValues)
# Hardcoded failure case
#        print("\n   ----Hardcoded failure setup for var1 con1:---- \n\n")
#        self.varValues = [5, 2, 1, 1, 1, 1]
#        next = cspNode(self, self.varList, self.varDomains, self.conList, self.forChecking, self.varValues)
#------------------------

        # returns & stores the position of the next variable in the varL list
        nextVar = self.nextVar()


        # TODO
        # For that variable, return all possible values,
        nextVals = self.nextVals()

            # TODO  Forward Checking
            # For each variable domain in the nodes you're about to create,
            # use forward checking here to delete constraint-violating values from domains
            # after doing so, if any domain is empty, return failure?
                # Figure out how to return failure from this function

        # and create cspNodes with each of these values, amd store them in the list
        # from worst to last




        print("Returned successor\n")
        # IMPORTANT: for list, store the worst states first and the
        # best states last
        list.append(next)
        return list

    # Prints out the current values
    def printValues(self):
        print("Ought to print values rn")
        # Must find a way to print out values
        # in the order that they were assigned

            # might just have to make an attribute of cspNode that's
            # "orderOfVars" and keeps track of the order they were added

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

        nextVar = self.getMCedVar(blankVars)
        if nextVar is False:
            nextVar = self.getMCingVar(blankVars)
        if nextVar is False:
            nextVar = self.getABVar(blankVars)

        return nextVar

    # TODO
    # Returns the most constrained unassigned variable
    # If two variables are equally constrained, returns false
    def getMCedVar(self, blankVars):
        print("Getting the most constrained variable")
        nextVar = False
        nextVarLenDomain = 100000 # should be max num but whatever

        # for all unassigned variables
        for x in blankVars:
            # if the number of values is less than the current nextVar's
            if (len(self.varDomains[self.varList.index(x)]) < nextVarLenDomain):
                # replace it with this variable
                nextVar = x
                nextVarLenDomain = len(self.varDomains[self.varList.index(x)])

            # if the number of values is equal to the current nextVar's
            if (len(self.varDomains[self.varList.index(x)]) == nextVarLenDomain):
                # replace it with False
                nextVar = False

        return nextVar

    # TODO
    # Returns the most constraining unassigned variable
    # If two variables are equally constraining, returns false
    def getMCingVar(self, blankVars):
        print("Getting the most constraining variable")
        numConstraints = [None] * len(blankVars)
        nextVar = False
        numConstraints = -1

        # For each blank variable
        for x in blankVars:
            # Count the number of constraints that it is in
            # where the other variable's value is also none


            print("yo")



        return False

    # TODO
    # Returns the next unassigned variable alphabetically
    def getABVar(self, blankVars):
        print("Getting the alphabetically next variable")

        # Use these to determine the more preferred values
        self.getLCVal()
        self.getNumVal()


        return False

    # TODO
    # Returns a list of all possible values for the selected variable
    # Specifically in the order of least-constricting and then alphabetical
    def nextVals(self, var):
        print("Returns a list of the next values")


        return False

    # TODO
    # Returns the most constraining unassigned value
    def getLCVal(self):
        print ("Getting the most constraining value")

        return False

    # TODO
    # Returns the next unassigned value numerically
    def getNumVal(self):
        print("Getting the alphabetically next variable")

        return False


# main
if __name__ == '__main__':
    main()


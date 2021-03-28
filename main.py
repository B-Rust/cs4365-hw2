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

    # TODO - fill out this function
    def getSolution(self):
        # creates root node
        # create a queue of nodes
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

        return None

# Class of an individual CSP node
class cspNode:
    parent = None #parent node
    varList = None
    varValues = None

	#has checkCorrect() function
	#has getSuccessors() function

    def __init__(self, par, varL, varV):
        parent = par
        varList = varL

    # TODO code this
    def checkCorrect(self):
        # If constraints are violated
        #       print out current values & failure
        # If constraints are not violated
            # If all the variables are filled
                # Print out variables & success
            # getSuccessors & add them to the cspProblem.getSolution queue
        return None

    def getSuccessors(self):
        # Stuff
        return None

# Most ConstrainED VARiable
def mCedVar():
    print("TODO")
    return 0

# Most ConstrainING VARiable
def mCingVar():
    print("TODO")

    # if there's still a tie, break it alphabetically
    return 0

# Least Constraining Value
def lCV():
    print("TODO")
    #if there's a tie, go with the smaller  number
    return 0


# main
if __name__ == '__main__':
    main()


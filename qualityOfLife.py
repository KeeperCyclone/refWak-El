# QUALITY OF LIFE FUNCTIONS

import interpolate as ipl
import rowNeighSearch as rns 

# Transpose abitrarily-large 2D list such that [[1,2],[3,4]] becomes [[1,3],[2,4]]
# Independent
# TESTED SUCCESSFULLY
def transpose(table):
    temp_table = []
    for j in range(len(table[0])):
        newcol = []
        for i in table:
            newcol.append(i[j])
        temp_table.append(newcol)        
    return temp_table

# Columnar interpolation: Given a large 2D matrix, interpolate between columns, not rows
# Uses ipl
# TESTED SUCCESSFULLY
def colListerpolate(table,col1,col2,x):
    """
    Inputs:
        table : large 2D list
        col1 : integer index of target column 1
        col2 : integer index of target column 2
        x : interpolation factor (approaches col2 as x approaches 1)
    Output: 1D list of interpolated values
    """
    temp_table = transpose(table)
    # the larger value is usually on the right
    return ipl.listerpolate(temp_table[col1], temp_table[col2], x)

# uses rns
def listIsInRange(list,query):
    # list = [a,b]
    a,b = list[0],list[1]
    return rns.isInRange(a,b,query)
    # returns TRUE or FALSE

""" probably won't use this but I'll leave it in anyway """
def allNeighborsCoordsFromRef(idxref):
    # Uses 2-element 1D idxref (upper left corner of a 2x2 neighborhood) to find coords of all other neighbors.
    return idxref , [idxref[0],idxref[1]+1] , [idxref[0]+1,idxref[1]] , [idxref[0]+1,idxref[1]+1]

# independent
# TESTED SUCCESSFULLY
def getIdxFirstAndLast(listq,query):
    # Gets first and last indices of a chunk of repeating members in a list (e.g. -1 in [1,4,2,-1,-1,-1,-1,9,8])
    first = listq.index(query)
    listq.reverse()
    last = (len(listq)-1) - listq.index(query)
    return first, last

# independent
# TESTED SUCCESSFULLY
def reverseDict(dicti):
    # generates a dict with reversed key-value pairs
    dict_rev = {value:key for (key,value) in dicti.items()}
    return dict_rev


# generates an object that functions as a dictionary that can work both ways
# uses the function above
# TESTED SUCCESSFULLY
class insensitiveDict:
    def __init__(self,base_dict):
        self.base_dict = base_dict
        self.rev_dict = reverseDict(base_dict)
    def insensitivelookup(self,key):
        try:
            return self.base_dict[key]
        except:
            try:
                return self.rev_dict[key]
            except:
                raise Exception('Cannot find value anywhere!')


# Turns a list into an integer-keyed dictionary
# Independent
# TESTED AND WORKING!
def listToDict(l,reverse=0):
    if not isinstance(l, list):
        raise Exception('listToDict function input should be a list!')
    dictionary = {}
    n = 0
    if reverse == 0:
        for eachElement in l:
            dictionary.update({n:eachElement})
            n += 1
        return dictionary
    elif reverse == 1:
        for eachElement in l:
            dictionary.update({eachElement:n})
            n += 1
        return dictionary

# TESTED AND WORKING!
# apparently it breaks when you use a list as input
def merge1DListsByElement(*l):
    # process: [a,b] + [x,y] + ... = [ [a,x,...] , [b,y,...] ]
    listOfLists = [each for each in l]
    masterList = []
    for eachElement in range(len(listOfLists[0])):
        newCell = [eachList[eachElement] for eachList in listOfLists]
        masterList.append(newCell)
    return masterList


# TESTED AND WORKING!
# takes a list as input
def merge1DListsByElement2(l):
    # process: [a,b] + [x,y] + ... = [ [a,x,...] , [b,y,...] ]
    masterList = []
    for eachElement in range(len(l[0])):
        newCell = [eachList[eachElement] for eachList in l]
        masterList.append(newCell)
    return masterList

# TESTED AND WORKING!
def merge2DListsByCell(*inputmatrices):
    # process: [[a,b],[c,d]] + [[w,x],[y,z] = [  [[a,w] , [b,x]] ,  [[c,y],[d,z]]  ]
    matrixList = [m for m in inputmatrices]
    masterList = []
    for eachRow in range(len(matrixList[0])):
        targetRow = [eachMatrix[eachRow] for eachMatrix in matrixList]
        newRow = merge1DListsByElement2(targetRow)
        masterList.append(newRow)
    return masterList

# TESTED AND WORKING!
def isTableRectangular(m):
    firstRowlen = len(m[0])
    for rows in m:
        if len(rows) != firstRowlen:
            return False
        else:
            pass
    return True

# TESTED AND WORKING!
# intended for rectangular matrices
def areTablesSameDimension(*m):
    for tables in m:
        if not isTableRectangular(tables):
            raise Exception("Input tables aren't even rectangular!")
    getRows = lambda a : len(a)
    getCols = lambda a : len(a[0])
    refRows = getRows(m[0])
    refCols = getCols(m[0])
    for each in m:
        currentRows = getRows(each)
        currentCols = getCols(each)
        if currentRows != refRows or currentCols != refCols:
            return False
        else:
            pass
    return True

# TESTED AND WORKING!
def strInputValidation(input,tupleOfValidInputs):
    if input in tupleOfValidInputs:
        return input
    else:
        raise Exception('Input not in list of valid inputs!')

def inputLoopTrap(checkFor,condition,prompt_str='',error_str=''):
    # Asks the user for input and keeps them there until they enter a valid input
    # Returns input if valid
    # Can be set to check either type validity or membership in a tuple/other such iterable
    def isValid(checkFor,user_input,condition):
        # can either check for type validity and/or membership
        try:
            if checkFor == 'member':
                if user_input in condition:
                    return True, user_input
                else:
                    return False, None
            elif checkFor == 'int':
                try:
                    user_input = int(user_input)
                    return True, user_input
                except:
                    return False, None
            elif checkFor == 'float':
                try:
                    user_input = float(user_input)
                    return True, user_input
                except:
                    return False, None
        except:
            raise ValueError("checkFor is only 'member', 'float', or 'int'!")

    while True:
        user_input = input(prompt_str)
        valid, user_input = isValid(checkFor,user_input,condition)
        if valid:
            return user_input
        else:
            print(error_str)



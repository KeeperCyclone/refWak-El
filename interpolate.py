# TESTED AND WORKING
def listerpolate(ulist, llist, x=0.5):
    """
    Linearly interpolates values element-wise between two lists
        Gets midpoint value by default
    Inputs:
        ulist: Upper list; appears towards the top of the table
        llist: Lower list; appears downwards of the table
            Must be same length as ulist
        x: value from 0 to 1, with 1 being towards llist; used multiplicatively to find output
    Output: 1-D list
    """
    x = float(x) # just to make sure a float value is passed into here

    if len(ulist) != len(llist):
        raise Exception('Both input lists must be the same length!')
    if x <= 0 or x >= 1:
        raise Exception('x must be between 0 and 1!')

    inter = [] # list of interpolated values
    for element in range(len(ulist)):
        inter.append(x*(llist[element] - ulist[element])+ulist[element])
    
    return inter

# TESTED AND WORKING
def listerpolate2(ulist,llist,targetCol,targetQuery):
    x = reversefast(ulist[targetCol],targetQuery,llist[targetCol])
    return listerpolate(ulist,llist,x)

# TESTED AND WORKING
def fast(a,b,x=0.5):
    # Fast interpolation between only two float values
    # Function approaches b as x approaches 1
    a, b, x = float(a), float(b), float(x) # just to make sure a float value is passed here
    if x < 0 or x > 1:
        raise Exception('x must be between 0 and 1!')
    return a+x*(b-a)

# TESTED AND WORKING
def reversefast(a,c,b):
    # If c is between a and b, returns the interpolation factor x
    a, b, c = float(a), float(b), float(c) # just to make sure a float value is passed here
    if c < a or c > b:
        raise Exception('c must be between a and b!')
    return (c-a)/(b-a)

# TESTED AND WORKING
def cellterpolateByRow(row1,row2,x=0.5):
    # interpolates between [[a,b],[c,d]] and [[1,2],[3,4]] as [ [listerpolate([a,b],[1,2])] , [listerpolate([c,d],[3,4])] ]
    interpolatedRow = [listerpolate(row1[eachCellIdx],row2[eachCellIdx],x) # listerpolate raises its own exception, apparently
        for eachCellIdx in range(len(row1))]
    
    return interpolatedRow

# TESTED AND WORKING!
def cellterpolateBetwCells(cell1,cell2,iplFactor=0.5):
    # process: [a,b] , [c,d] -> [ipl(a,c) , ipl(b,d)]
    newCell = [fast(cell1[i],cell2[i],iplFactor) for i in range(len(cell1))]
    return newCell 


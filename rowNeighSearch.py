import csv

# TESTED AND WORKING
def onBounds(a,b,c):
    # Check if c is equal to a or b
    return c == a or c == b 

# TESTED AND WORKING
def isInRange(a, b, c):
    # Check if c is between a and b
    # Not sensitive to order of a and b
    if b < a:
        a, b = b, a 
    return c > a and c < b 

# TESTED AND WORKING
def prepCSV(filename):
    # Input: filename in single quotes
    # Output: 2D list with header stripped
    with open(filename) as csvfile:
        csv_iter = csv.reader(csvfile, delimiter=",") # csv as an iterable object
        temp_table = []
        next(csv_iter) # skips the header
        
        # create a table of float values with the header stripped off and place it in temp_table
        for row in csv_iter: 
            floatedRow = [float(element) for element in row]
            temp_table.append(floatedRow)
        return temp_table

# TESTED AND WORKING
def filterByRow(table,col,input):
    # Finds and returns neighboring rows which bound the input value
    # Input: list (table), col (int), and search query (float)
    # Output: list (table) of boundary rows

    # Create a 1D list from a target column of the table
    targetList = [row[col] for row in table]

    # Make pairwise comparisons with isInRage() and onBounds() and note the indices
    # in which the comparison returns true.
    idx = []
    raiseError = True
    for n in range(len(targetList)-1):
        if input == targetList[n] :
            idx.append(n)
            raiseError = False
            break
        elif input == targetList[n+1] :
            idx.append(n+1)
            raiseError = False
            break
        elif isInRange(targetList[n],targetList[n+1],input):
            idx.extend([n, n+1])
            raiseError = False
    if raiseError == True:
        raise Exception('No indices found!')
    # Return the lists those indices correspond to and string together a 2D list with them.
    i_iter = iter(idx)
    output = []
    for eachIdx in i_iter:
        output.append(table[eachIdx])
    return output

# TESTED AND WORKING
def filterByCol(table,col1,col2,query):
    # Finds and returns table's rows whose two targeted columns bound the query value
    # Inputs:
        # table : 2D list
        # col1 : integer value; index of nested list in table
        # col2 : int; index of nested list in table
    # Output:
        # 2D list of filtered rows

    table_iter = iter(table)

    # Find all passable row indices
    idx = []
    idxPos = 0
    for eachRow in table_iter:
        row = eachRow
        if onBounds(row[col1],row[col2],query) or isInRange(row[col1],row[col2],query):
            idx.append(idxPos)
        idxPos += 1
    
    # Use idx list to call all pertinent table rows into an output 2D list
    i_iter = iter(idx)
    output = []
    for eachIdx in i_iter:
        output.append(table[eachIdx])
    return output





"""
def rowNeighSearch(csv, pbar=-1, psia=-1, t=-1, h=-1, s=-1, v=-1, x=-1):
    # csv is the csv file object
    
    # pbar : pressure (bar)
    # psia : pressure (psia)
    # t : temperature
    # h : enthalpy
    # s : entropy
    # v : specific volume
    # x : quality
    # defaults are -1; used to signal the fact that there was no input
    
    csv_iter = csv.reader(csv, delimiter=",") # csv as an iterable object
    temp_table = []
    next(csv_iter) # skips the header
    
    # create a table of float values with the header stripped off and place it in temp_table
    for row in csv_iter: 
        floatedRow = [float(element) for element in row]
        temp_table.append(floatedRow) 
    # make pair-wise comparisons and see if given inputs exist in ranges
    # record comparisons into temp_candidates
    iter_table = iter(temp_table)
    temp_candidates = []
    for start in iter_table:
        first = start
        second = next(iter_table)
"""
    

import rowNeighSearch as rns 
import csv
import interpolate as ipl
from qualityOfLife import areTablesSameDimension
from qualityOfLife import merge2DListsByCell

# WORKING
def cleanTable(table2d):
        for i in range(len(table2d)):
            table2d[i] = [float(element) for element in table2d[i]]
        return table2d

# TESTED AND WORKING
def prepCSV(csvfilename):
    """
    reorders CSV data; specific to the way superheat tables are arranged
    inputs:
        csvfilename : string of the csv filename
    outputs:
        tList : 1D list of temperature data
        pList : 1D list of pressure data
        hsvList : 2D list of h/s/v (enthalpy/entropy/specific volume) data
    """
    with open(csvfilename) as csvfile:
        csv_iter = csv.reader(csvfile, delimiter=",")
        temp_table = [row for row in csv_iter]

        # separate out the temperature, pressure, and h/s/v values in 1D, 1D, and 2D lists, respectively
        tList = temp_table.pop(0)
        del tList[0] # removes the tiny corner label
        tList = [float(tElement) for tElement in tList]
        pList = [float(eachPRow.pop(0)) for eachPRow in temp_table]
        temp_table = cleanTable(temp_table)
        return tList, pList, temp_table

def prepCSVBoundary(csvfilenames):
    """
    reorders CSV data; specific to the way boundary tables are arranged
    input: tuple of csv filenames
    output: 4 temporary tables and a plist
    """
    listOfTables = []
    for eachFile in csvfilenames:
        with open(eachFile) as csvfile:
            csv_iter = csv.reader(csvfile, delimiter=",")
            temp_table = [row for row in csv_iter]

            del temp_table[0] # these are just headers
            plist = [float(row.pop(0)) for row in temp_table]
            temp_table = cleanTable(temp_table)
            listOfTables.append(temp_table)
    ttable, htable, stable, vtable = listOfTables[0],listOfTables[1],listOfTables[2],listOfTables[3]
    return plist, ttable, htable, stable, vtable

# TESTED AND WORKING!
def prepWorkingTable(tlist,plist,htable,stable,vtable):
    # dimensional assumptions check:
    if (len(plist) == len(htable) and len(tlist) == len(htable[0]) and 
    areTablesSameDimension(htable,stable,vtable)):
        pass
    else:
        raise Exception("Cannot prepare WorkingTable; input table dimensions not equal!")
    ttable = [tlist for length in plist] # generate a columnarly-repeated 2D table from tlist
    megatable = merge2DListsByCell(ttable,htable,stable,vtable) # combine t with h,s,v
    
    return megatable

# TESTED AND WORKING!
def getExactPRow(pList,pquery,workingtable):
    try:
        exactPRowIdx = pList.index(pquery)
    except:
        return False
    return workingtable[exactPRowIdx]

# TESTED AND WORKING!
def getBoundingPRows(pList,pquery,workingtable):
    def getBoundingPRowIndices():
        # returns indices or flags False
        try:
            find = [x for x in range(len(pList)) 
                if 
                (pquery > pList[x] and pquery < pList[x+1])
                or
                (pquery < pList[x] and pquery > pList[x-1])
            ]
            return find
        except:
            return False
    
    get = getBoundingPRowIndices()
    if get == False:
        return False
    else:
        m, n = get[0], get[1]
        a, b = pList[m], pList[n]
        x = (pquery - a)/(b - a)
        return workingtable[m], a, workingtable[n], b, x
    

# TESTED AND WORKING!
def stripColswithEmptyCells(listOfRows,flag=-1): # expected data structure: [ [[a,b],[c,d]] , [[1,2],[3,4]]  ]
    def findEmptyCellIndices(row):
        emptyCellIndices = [i for i in range(len(row)) if flag in row]
        emptyCellIndices.sort()
        return emptyCellIndices
    def deleteIndicatedCells(listOfIndices,row):
        for idx in reversed(listOfIndices):
            del row[idx]
        return row

    emptyCellIndices = findEmptyCellIndices(listOfRows[-1]) # assuming the last row has the most number of empty cells
    #[deleteIndicatedCells(emptyCellIndices,row) for row in listOfRows]
    return [deleteIndicatedCells(emptyCellIndices,row) for row in listOfRows]

def stripColswithEmptyCells2(listOfRows,flag=-1): #expected data structure: [ [a,b,c] , ... , [x,y,z] ]
    def findCellIndicesWithFlag():
        emptyCellIndices = [i for i in range(len(listOfRows)) if flag in listOfRows[i]]
        return emptyCellIndices
    def deleteIndicatedCells(listOfRows,listOfIndices):
        for idx in reversed(listOfIndices):
            del listOfRows[idx]
        return listOfRows

    emptyCellIndices = findCellIndicesWithFlag()
    return deleteIndicatedCells(listOfRows,emptyCellIndices)

# TESTED AND WORKING!
def getparam(param_type,cell):
    return cell[{'t':0,'h':1,'s':2,'v':3}[param_type]]

# TESTED AND WORKING!
def getExactCell(row,paramType,paramVal):
    # paramType valid inputs: 't', 'h', 's' and 'v'
    for cell in row:
        if getparam(paramType,cell) == paramVal:
            return cell
    return False

# TESTED AND WORKING!
def getBoundingCells(row,paramType,paramVal):
    # row is of the form [[a,b],[c,d],[...]]
    # paramType valid inputs: 't', 'h', 's' and 'v'
    def getCellPair():
        a,b=0,1
        while True: # will stop via missing list index exception when it calls a non-existent row[b]
            yield row[a],row[b]
            b,a = a+2,a+1
    def paramIsBetwCells(cell1,cell2): # expected data structure: [a,b,c]
        paramCell1, paramCell2 = getparam(paramType,cell1), getparam(paramType,cell2)
        return rns.isInRange(paramCell1, paramCell2, paramVal)
    
    cellPair = getCellPair()
    while True:
        try:
            cell1,cell2 = next(cellPair)
            if paramIsBetwCells(cell1,cell2):
                param1 = getparam(paramType,cell1)
                param2 = getparam(paramType,cell2)
                x = (paramVal - param1)/(param2 - param1)
                return cell1,cell2, x, param1, param2
        except:
            return False

import csv 
import rowNeighSearch as rns
import interpolate as ipl
import qualityOfLife as qol
import tableMetadata as tmd
import threeDSearch as tds
from pprint import pprint

class metadataDict:
    queryToVartype = {'px':'p','tx':'t'}
    unitTypeToUnits = {
        'eng': {
            'p':'psia',
            't':'degF',
            'h':'Btu/lbm',
            's':'Btu/lbm-F',
            'v':'ft^3/lbm'
        },
        'si': {
            'p':'bar',
            't':'degC',
            'h':'kJ/kg',
            's':'kJ/kg-K',
            'v':'m^3/kg'
        }
    }
    superheatCellVarDict = {'t':0,'h':1,'s':2,'v':3}

class sattable:
    filenameDict = {
        'eng': {
            'px':('A-1 Saturated Steam (p)(English).csv','A-2 Saturated Steam (t)(English).csv'),
            'tx':('A-2 Saturated Steam (t)(English).csv','A-1 Saturated Steam (p)(English).csv')
        },
        'si': {
            'px':('A-4b Saturated Steam (p)(SI).csv','A-4a Saturated Steam (t)(SI).csv'),
            'tx':('A-4a Saturated Steam (t)(SI).csv','A-4b Saturated Steam (p)(SI).csv')
        }
    } # [unit][query]
    
    def __init__(self,unitType,queryType):
        if unitType == 'eng' or 'si':
            self.unitType = unitType
        else:
            raise Exception("Only allowable unitType inputs are 'eng' or 'si'!")
        if queryType == 'px' or 'tx':
            self.queryType = queryType
        else:
            raise Exception("Only allowable unitType inputs are 'px' or 'tx'!")
        self.filenames = sattable.filenameDict[unitType][queryType]

    def reportState(self,pt,x=-1,s=-1):
        if x > 0 and s > 0:
            raise Exception('User may only input EITHER x OR s, not both at the same time!')
        queryVar = metadataDict.queryToVartype[self.queryType]
        colDict = tmd.tableColDict[self.unitType][self.queryType]
        targetCol = colDict[queryVar]

        fileidx = 0
        workingTable = rns.prepCSV(self.filenames[fileidx])
        
        def getRowFilterResult():
            try: 
                print('***\nSearching.......')
                rowFilterResult = (rns.filterByRow(workingTable, targetCol, pt))
                return rowFilterResult
            except:
                print('==================')
                print('SEARCH FAILED! Query may be out of data bounds.')
                print('==================')
                failstate = False
                return failstate

        rowFilterResult = getRowFilterResult()
        if rowFilterResult == False:
            print('Retrying.......')
            fileidx = 1 # check next file in 2-tuple
            rowFilterResult = getRowFilterResult()
            if rowFilterResult == False:
                print('==================')
                print('SEARCH FAILED! Query absolutely out of data bounds.')
                print('==================')
                print('\n==================')
                print('Report failed! :(')
                print('==================\n')
                failstate = False
                return failstate
            else:
                pass
        else:
            pass

        def getRefRow():
            if len(rowFilterResult) == 1:
                return rowFilterResult[0]
            if len(rowFilterResult) == 2:
                return ipl.listerpolate2(rowFilterResult[0],rowFilterResult[1],targetCol,pt)

        def interpolateFromX(finalRefRow,x):
            # find h, s, v; tack on P or T (whichever's the alternate of the query) and return as dictionary
            solutions = {}
            for eachPair in [['hf','hg','h'],['sf','sg','s'],['vf','vg','v']]:
                idx_colf , idx_colg = colDict[eachPair[0]] , colDict[eachPair[1]]
                solvedVal = ipl.fast(finalRefRow[idx_colf], finalRefRow[idx_colg], x)
                solutions.update({eachPair[2]:solvedVal})
            # add corresponding T if query is px; P if tx
            PorT = {'px':'t','tx':'p'}[self.queryType]
            idx_PorT = colDict[PorT]
            solutions.update({PorT:finalRefRow[idx_PorT]})

            return solutions

        def getXFromS(finalRefRow,s):
            if s == -1:
                pass
            else:
                sf_colid = tmd.tableColDict[self.unitType][self.queryType]['sf']
                sg_colid = tmd.tableColDict[self.unitType][self.queryType]['sg']
                sf, sg = finalRefRow[sf_colid], finalRefRow[sg_colid]
                interpolationFactor = (s-sf)/(sg-sf)
                return interpolationFactor

        def printReport(sol,refrow):
            workingFilename = self.filenames[fileidx]
            colHeaderDict = {
                'A-1 Saturated Steam (p)(English).csv':tmd.a1_vars,
                'A-2 Saturated Steam (t)(English).csv':tmd.a2_vars,
                'A-4b Saturated Steam (p)(SI).csv':tmd.a4b_vars,
                'A-4a Saturated Steam (t)(SI).csv':tmd.a4a_vars,
            }
            varHeaderList = colHeaderDict[workingFilename]
            unitDict = metadataDict.unitTypeToUnits[self.unitType]
            rawDataUnitList = tmd.tableUnitDict[self.unitType][self.queryType]

            print('==========================================')
            print("With a query of:")
            print("{a} = {b} {c}".format(
                a = self.queryType,
                b = pt,
                c = unitDict[queryVar]
            ))
            print("x = {}".format(x))
            print('==========================================')
            print('Using data from {},'.format(self.filenames[fileidx]))
            print('the following rows were obtained:')
            print('==========================================')
            print(varHeaderList)
            print(rawDataUnitList)
            print(rowFilterResult[0])
            if len(rowFilterResult) == 2:
                print(rowFilterResult[1])
            print('==========================================')
            print('Interpolating...')
            print('==========================================')
            print(refrow)
            print('==========================================')
            print('...and the following values were calculated:')
            print('==========================================')
            if self.queryType == 'px':
                t = sol['t']
                print('T = {a} {b}'.format(a=t,b=unitDict['t']))
            elif self.queryType == 'tx':
                p = sol['p']
                print('P = {a} {b}'.format(a=p,b=unitDict['p']))
            print('h = {a} {x}\ns = {b} {y}\nv = {c} {z}'.format(
                    a = sol['h'],
                    x = unitDict['h'],
                    b = sol['s'],
                    y = unitDict['s'],
                    c = sol['v'],
                    z = unitDict['v']
                    )
                )
            print('==========================================')
        
        refRow = getRefRow()
        if s != -1:
            x = getXFromS(refRow,s)
            solution = interpolateFromX(refRow,x)
            printReport(solution,refRow)
        else:
            solution = interpolateFromX(refRow,x)
            printReport(solution,refRow)

class superheat:
    filenameDict = {
        'eng': (
            'A-3 Superheated Steam (h)(English).csv',
            'A-3 Superheated Steam (s)(English).csv',
            'A-3 Superheated Steam (v)(English).csv'
        ),
        'si': (
            'A-5 Superheated Steam (h)(SI).csv',
            'A-5 Superheated Steam (s)(SI).csv',
            'A-5 Superheated Steam (v)(SI).csv'
        )
    }
    
    def __init__(self,unitType,queryType):
        self.unitType = qol.strInputValidation(unitType,('eng','si'))
        self.queryType = qol.strInputValidation(queryType,('pt','ps'))
        self.filenames = superheat.filenameDict[unitType]
    
    def reportState(self,p,ts):
        pquery = p
        tsquery = ts
        tsType = {'pt':'t','ps':'s'}[self.queryType]
        tlist,plist,htable = tds.prepCSV(self.filenames[0])
        stable, vtable = tds.prepCSV(self.filenames[1])[2], tds.prepCSV(self.filenames[2])[2]
        workingTable = tds.prepWorkingTable(tlist,plist,htable,stable,vtable)

        def getRow():
            row = tds.getExactPRow(plist,pquery,workingTable)
            if row == False:
                getBoundingPRows = tds.getBoundingPRows(plist,pquery,workingTable)
                if getBoundingPRows == False:
                    noneFound = False
                    return noneFound
                else:
                    row1, p1 = getBoundingPRows[0],getBoundingPRows[1]
                    row2, p2 = getBoundingPRows[2], getBoundingPRows[3]
                    iplFactor = getBoundingPRows[4]
                    print('===================')
                    print('Pressure query has to be interpolated between the ff. data:')
                    print('+++')
                    print('From pressure {}:'.format(p1))
                    pprint(row1)
                    print('+++ and +++')
                    print('From pressure {}:'.format(p2))
                    pprint(row2)
                    print('===================')
                    rows = tds.stripColswithEmptyCells([row1,row2])
                    row1, row2 = rows[0], rows[1]
                    interpolatedRow = ipl.cellterpolateByRow(row1,row2,iplFactor)
                    print('===================')
                    print('Interpolating for {a} {b}:'.format(a=pquery, b=metadataDict.unitTypeToUnits[self.unitType]['p']))
                    pprint(interpolatedRow)
                    print('===================')
                    return interpolatedRow
            else:
                finalExactRow = tds.stripColswithEmptyCells([row])[0]
                finalExactRow = tds.stripColswithEmptyCells2(finalExactRow)
                print('===================')
                print("Pressure query is exact, resulting in the ff. data row:")
                print('+++')
                pprint(finalExactRow)
                print('+++')
                print('===================')
                return finalExactRow

        def getCell(finalRow):
            tsTypeDict = {'t':'temperature','s':"entropy"}

            getExactCell_result = tds.getExactCell(finalRow,tsType,tsquery)
            if getExactCell_result == False:
                getBoundingCells_result = tds.getBoundingCells(finalRow,tsType,tsquery)
                if getBoundingCells_result == False:
                    noneFound = False
                    return noneFound
                else:
                    cell1, cell2 = getBoundingCells_result[0],getBoundingCells_result[1]
                    print('===================')
                    print("The {a} query {b} {c} was found between cells:".format(a=tsTypeDict[tsType],b=tsquery,
                        c=metadataDict.unitTypeToUnits[self.unitType][tsType]))
                    print('+++')
                    print('Cell 1: ',cell1)
                    print('Cell 2: ',cell2)
                    print('+++')
                    iplFactor2 = getBoundingCells_result[2]
                    param1, param2 = getBoundingCells_result[3],getBoundingCells_result[4]
                    print("Calculating an interpolation factor of f = {} by".format(iplFactor2))
                    print("finding {a} = {d} between {b} and {c},".format(a=tsType,b=param1,c=param2,d=tsquery))
                    print("resulting in the cell:")
                    ans = ipl.cellterpolateBetwCells(cell1,cell2,iplFactor2)
                    print('\n')
                    print(ans)
                    print('\n')
                    print('===================')
                    return ans
            else:
                exactResult = getExactCell_result
                print('===================')
                print("One of the cells exactly match the {} query; cell data:".format(tsTypeDict[tsType]))
                print('+++')
                print(exactResult)
                print('+++')
                print('===================')
                return exactResult

        def printReportHeader():
            appendixDict = {'eng':'A-3, Superheated Steam (English)','si':'A-5, Superheated Steam (SI)'}
            print('=================== REPORT START ===================')
            print('Referring to Appendix {},'.format(appendixDict[self.unitType]))
            print('using data from {a}, {b},\nand {c},'.format(a=self.filenames[0],b=self.filenames[1],c=self.filenames[2]))
            print('the following steps were taken:')
            print('================== NOTES =================')
            print('***All cells follow [T,h,s,v] structure!***')
            print("***All cell with -1's are empty cells!***")
            print('================== UNITS ==================')
            print(metadataDict.unitTypeToUnits[self.unitType])
            print('==========================================')

        def printAnswer(ans):
            varTypeToUnits = metadataDict.unitTypeToUnits[self.unitType]
            print('=============== STATE FOUND =============')
            print("p = {a} {b}".format(a=pquery,b=varTypeToUnits['p']))
            for eachVar in 'thsv':
                colid = metadataDict.superheatCellVarDict[eachVar]
                print("{a} = {b} {c}".format(a=eachVar,b=ans[colid],c=varTypeToUnits[eachVar]))
            print('==========================================')
        def reportFail():
            print('***************** !!! *****************')
            print('SUPERHEAT DATA INSUFFICIENT.')
            print('RAISING FAILSTATE FLAG.')
            print('***************** !!! *****************')

        printReportHeader()
        workingRow = getRow()
        if workingRow == False:
            reportFail()
            print('Failure info: Failed at getRow()')
            answered = False
            return answered
        else:
            workingCell = getCell(workingRow)
            if workingCell == False:
                reportFail()
                print('Failure info: Failed at getCell()')
                answered = False
                return answered
            else:
                printAnswer(workingCell)

class boundary: 
    filenameDict = {
        'eng':(
            'Saturated-Superheated Boundary (t)(English).csv',
            'Saturated-Superheated Boundary (h)(English).csv',
            'Saturated-Superheated Boundary (s)(English).csv',
            'Saturated-Superheated Boundary (v)(English).csv'
        ),
        'si':(
            'Saturated-Superheated Boundary (t)(SI).csv',
            'Saturated-Superheated Boundary (h)(SI).csv',
            'Saturated-Superheated Boundary (s)(SI).csv',
            'Saturated-Superheated Boundary (v)(SI).csv'
        )
    }
    
    def __init__(self,unitType,queryType):
        checkInput = ['eng','si','pt','ps']
        if unitType in checkInput and queryType in checkInput:
            self.unitType = unitType
            self.queryType = queryType
        else:
            raise Exception('Bad unit/queryType input!')
        
        self.filenames = boundary.filenameDict[unitType]

    def reportState(self,pquery,tsquery):
        filenames = self.filenames
        tsType = {'pt':'t','ps':'s'}[self.queryType]
        failstate = False

        def prepWorkingTable():
            plist, ttable, htable, stable, vtable = tds.prepCSVBoundary(filenames)
            megatable = qol.merge2DListsByCell(ttable, htable, stable, vtable)
            return plist, megatable

        def getRows(plist, workingtable):
            # use getBoundingProws and getExactPRow
            # get exactRow, if exactRow == False, execute getBoundingProw, else return exactRow result
            print ('.....\nSearching for exact row...\n.....')
            exactRow = tds.getExactPRow(plist, pquery, workingtable)
            if exactRow == False:
                # resort to bounding prow
                boundingRows = tds.getBoundingPRows(plist, pquery, workingtable)
                if boundingRows == False:
                    print('NO BOUNDING ROWS FOUND!')
                    return False
                else:
                    pa, pb = boundingRows[1],boundingRows[3]
                    rowa,rowb = boundingRows[0],boundingRows[2]
                    iplF = boundingRows[4]
                    print('=======================')
                    print('At pressure {}, row data is: '.format(pa), rowa)
                    print('At pressure {}, row data is: '.format(pb), rowb)
                    print('At queried pressure ',pquery,', the interpolation factor is f = ', iplF)
                    finalRow = ipl.cellterpolateByRow(rowa,rowb,iplF)
                    print('=======================')
                    print('Using the interplation factor, the interpolated cells are:')
                    print('At pressure P = ',pquery, ', ',finalRow)
                    print('=======================')
                    return finalRow
            else:
                print('=======================')
                print('EXACT ROW FOUND!:')
                print(exactRow)
                print('=======================')
                return exactRow
        def getCells(finalRow):
            print('=======================')
            print('Finding a cell with exact matching query......')
            print('=======================')
            exactCell = tds.getExactCell(finalRow, tsType, tsquery)
            if exactCell == False:
                print('CANNOT FIND EXACT CELL!')
                print('=======================')
                print('Finding cells that bound the query.......')
                print('=======================')
                boundingCells = tds.getBoundingCells(finalRow, tsType, tsquery)
                if boundingCells == False:
                    print('CANNOT FIND CELLS THAT BOUND THE QUERY!')
                    print('=======================')
                    return False
                else:
                    print('BOUNDING CELLS FOUND!')
                    cell1, cell2 = boundingCells[0], boundingCells[1]
                    print('=======================')
                    print('The cells are {a} and {b}'.format(a=cell1,b=cell2))
                    print('=======================')
                    iplF2 = boundingCells[2]
                    print('Between the bounding cells, the queried parameter {a} = {b} yields'.format(a=tsType,b=tsquery))
                    print('an interpolationfactor of f = {}'.format(iplF2))
                    print('=======================')
                    finalCell = ipl.cellterpolateBetwCells(cell1, cell2, iplF2)
                    print('The final cell is thus: {}'.format(finalCell))
                    print('=======================')
                    return finalCell
            else:
                print('=======================')
                print('EXACT CELL FOUND!:')
                print(exactCell)
                print('=======================')
                return exactCell

        def printReportHeader():
            appendixDict = {
                'eng':(
                    'A-3, Superheated Steam (English)',
                    'A-1, Saturated Steam (Pressure) (English)'
                ),
                'si':(
                    'A-5, Superheated Steam (SI)',
                    'A-4b, Saturated Steam (Pressure) (SI)'
                )
            }
            print('=============== * * * * * * ============')
            print('Referring to Appendices {a} and ,'.format(a=appendixDict[self.unitType][0],
                b=appendixDict[self.unitType][1]))
            print('using data from {a},{b}, {c} \n and {d},'.format(a=self.filenames[0],
                b=self.filenames[1], c=self.filenames[2], d=self.filenames[3]))
            print('the following steps were taken:')
            print('================== NOTES =================')
            print('***All cells follow [T,h,s,v] structure!***')
            print('================== UNITS ==================')
            print(metadataDict.unitTypeToUnits[self.unitType])
            print('==========================================')

        def printSolution(answerCell):
            unitDict = metadataDict.unitTypeToUnits[self.unitType]
            varDict = metadataDict.superheatCellVarDict
            print('=========================')
            print('p = {a} {b}'.format(a=pquery,b=unitDict['p']))
            for eachLetter in 'thsv':
                eachAnswer = answerCell[varDict[eachLetter]]
                print('{a} = {b} {c}'.format(a=eachLetter,b=eachAnswer,c=unitDict[eachLetter]))
            print('=========================')

        def reportFail():
            print('************ !!! ************')
            print("CANNOT FIND A REPORTABLE STATE :(")
            print('************ !!! ************')

        plist,self.megatable = prepWorkingTable()
        printReportHeader()
        workingRow = getRows(plist, self.megatable)
        if workingRow == False:
            reportFail()
            failstate = True
            return failstate
        else:
            self.answerCell = getCells(workingRow)
            if self.answerCell == False:
                reportFail()
                failstate = True
                return failstate
            else:
                printSolution(self.answerCell)
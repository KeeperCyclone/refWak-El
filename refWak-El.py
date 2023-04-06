import mainEngine as engine
import qualityOfLife as qol


unitDict = engine.metadataDict.unitTypeToUnits
validateUnitTypeInput = lambda str : qol.strInputValidation(str,('eng','si'))

def printUltraHeader():
    print('*******************!!!********************')
    print('*********!!! SEARCH STARTING !!!*********')
    print('*******************!!!********************')

def pxSearch(p,x,unit):
    # saturated region search only
    printUltraHeader()
    try:
        unit = validateUnitTypeInput(unit)
        px_search = engine.sattable(unit,'px')
        px_search.reportState(p,x)
    except:
        print('// Probably not in the saturated region?')
def txSearch(t,x,unit):
    # saturated region search only
    printUltraHeader()
    try:
        unit = validateUnitTypeInput(unit)
        tx_search = engine.sattable(unit,'tx')
        tx_search.reportState(t,x)
    except:
        print('// Probably not in the saturated region?')
def ptSearch(p,t,unit):
    # superheated region, then boundary search
    unit = validateUnitTypeInput(unit)
    printUltraHeader()
    pt_search = engine.superheat(unit,'pt')
    checkIfFailed = pt_search.reportState(p,t)
    if checkIfFailed == True:
        print('!!!\nRESORTING TO BOUNDARY TABLES\n!!!')
        pt_search = engine.boundary(unit,'pt')
        pt_search.reportState(p,t)
    else:
        pass
def psSearch(p,s,unit):
    # search saturated region first, then superheated, then boundary
    unit = validateUnitTypeInput(unit)
    printUltraHeader()
    ps_satSearch = engine.sattable(unit,'px')
    print('\n===============\nAttempting saturated table search........\n===============\n')
    try:
        ps_satSearch.reportState(p,s=s)
    except:
        print('No results from saturated region search.')
        print('\n===============\nAttempting superheat table search........\n===============\n')
        ps_superSearch = engine.superheat(unit,'ps')
        supersearch = ps_superSearch.reportState(p,s)
        if supersearch == False:
            print('No results from superheated region search.')
            print('\n===============\nAttempting Saturated-Superheat Boundary Table Search........\n===============\n')
            ps_boundarySearch = engine.boundary(unit,'ps')
            ps_boundarySearch.reportState(p,s)
        else:
            pass

""" 
def turbineEff(hstart,hideal,eta,unit):
def compEff(hstart,hideal,eta,unit):
""" # previously-planned, but never really bothered with it until now

print('\n========================================')
print('============ RefWak-El a1b3 ============')
print('========================================\n')

keepWindowOn = True
nextState = 0
attachedData = None
while keepWindowOn:
    defaultReturn = 0, None  

    def chooseSearchQuery():
        # asks user for search query and passes the appropriate variables
        # or exits, why not
        queries = ['pxSearch','txSearch','ptSearch','psSearch']

        print('***')
        print('Query Types:')
        for i in range(len(queries)):
            print("'{a}' for '{b}'".format(a=i,b=queries[i]))
        print("Type 'exit' to exit the script!")
        print('***')

        userInput_membership = ('0','1','2','3','exit')
        user_query = qol.inputLoopTrap('member',userInput_membership,'Enter query: ','Invalid input!')
        try:
            user_query = int(user_query)
            nextState = 2
            searchType = user_query
            print()
            confirmInput = qol.inputLoopTrap('member',('y','n'),
                'You have chosen {}. Are you sure? [y/n]: '.format(queries[user_query]),'Invalid input: Lower case only!')
            if confirmInput == 'y':
                return nextState, searchType
            else:
                return defaultReturn
        except:
            return user_query, None

    def enterVars(searchType):
        searchDict = {
            0:('p','x'),
            1:('t','x'),
            2:('p','t'),
            3:('p','s')
        }
        searchVars = searchDict[searchType]
    
        firstVar = qol.inputLoopTrap('float',float,'First variable: {} = '.format(searchVars[0]),'Invalid input type!')
        secondVar = qol.inputLoopTrap('float',float,'Second variable: {} = '.format(searchVars[1]),'Invalid input type!')
        unit = qol.inputLoopTrap('member',('eng','si'),"'eng' or 'si': ", 'Invalid input!')
        
        nextState, searchQuery = 3, (searchType, firstVar, secondVar, unit)
        return nextState, searchQuery

    def searchData(searchQuery):
        try:
            searchType, firstVar, secondVar, unit = searchQuery
            searchDispatch = {
                0:pxSearch,
                1:txSearch,
                2:ptSearch,
                3:psSearch
            }
            searchDispatch[searchType](firstVar, secondVar, unit)
            input('\n-- Report concluded --\nPress ENTER to continue...')
        except:
            pass
        return defaultReturn

    # ****** main execution below ******

    
    stateDispatch = {
        0:chooseSearchQuery,
        1:'exit',
        2:enterVars,
        3:searchData
    }
    try:
        nextState, attachedData = stateDispatch[nextState](attachedData) # allow it to error out
    except:
        nextState, attachedData = stateDispatch[nextState]()

    if nextState == 'exit':
        break

""" stateHasAttachedData = {
        0:0,
        1:0,
        2:1,
        3:1
    }""" # previously used as a manual check
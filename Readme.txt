       =================================
      ===================================
	THANK YOU FOR USING refWak-El!!
      ===================================
       =================================

current version: a1b3
Tables from El-Wakil (2nd Edition, (c) 1985), Appendix A

	NOW WITH CONSOLE-BASED UIX!!!

The only script you have to touch is refWak-El.py.

To run on Windows, double-click the file or use command prompt and do
`py refWak-El.py`.

To run on Linux, use `python3 refWak-El.py` from terminal.

There are four (4) available functions:

pxSearch()
txSearch()
ptSearch()
psSearch()

These are the four most common searches for doing Rankine cycle calculations from El-Wakil problems.
If you need other search types, feel free to try to understand my code and write your own lol (anyway,
the .csv files are just there)

Each function takes three inputs: parameter1, parameter2, and unit.

	parameter1 : numerical value of the first parameter
		(e.g. in pxSearch, parameter1 is pressure and param2 is quality-- because p and x) 
	parameter2 : numerical val of 2nd param
	unit : 'eng' or 'si' (this is CASE SENSITIVE because i was too LAZY to add a single line of code)

The console UIX will ask these from you when prompted. Please note that all units follow whatever the El-Wakil tables'
units are. In the special case of SI tables, where bars and psia are both in the same table, the script will select bars.

*************

CHANGELOG (Reverse chronological order)

19:40 10-Feb-21 (a1b3)
- Discovered a bug where superheat table search fails to ignore empty cells. The function "stripColsWithEmptyCells"
	wasn't doing its job.
	
	FIX: Created new function stripColsWithEmptyCells2 to operate alongside the existing stripColsWithEmptyCells; only
		God knows what will break if I switched out every instance of the original function for the new one.

- Discovered a bug where psSearch fails to do a boundary table search after failing a superheat table search.

	FIX: Apparently the failure flag was raising the opposite of what it was supposed to. Never touching that again.

18:13 08-Jan-21
+ Finally finished the console UIX. Running the script via double-click and non-instantly-vanishing
	CMD prompt should be feasible now.

16:59 08-Jan-21
- Discovered that interpolate.py is importing threeDSearch.py, but none of the functions there even use threeDSearch.

	FIX: Went ahead and removed the import.

16:48 08-Jan-21
- Discovered that module "qualityOfLife.py" imports itself. qualityOfLife.py imports interpolate.py,
	which imports threeDSearch.py, which -- yes -- imports qualityOfLife.py. This does not impede
	major functions, but it does mean that infinite loops CANNOT be implemented from inside
	qualityOfLife.py, as it would call the infinite loop twice.
	
	FIX: threeDSearch.py only uses two functions from qualityOfLife, so I went ahead and just directly imported
		the functions only instead of the whole module.






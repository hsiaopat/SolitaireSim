autosolver.exe: autosolver.cpp
	cl /EHsc autosolver.cpp user32.lib kernel32.lib

c-solver.exe: c-solver.cpp
	cl /EHsc c-solver.cpp user32.lib kernel32.lib /std:c++17
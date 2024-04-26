main.exe: main.cpp
	cl /EHsc main.cpp user32.lib kernel32.lib

c-solver.exe: c-solver.cpp
	cl /EHsc c-solver.cpp user32.lib kernel32.lib /std:c++17
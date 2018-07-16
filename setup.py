import cx_Freeze
import os

executables = [cx_Freeze.Executable("program.py")]

os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'

cx_Freeze.setup(
	name= "Mac Gyver",
	options= {"build_exe": {"packages":["pygame"],
							"include_files":["lib/labygen.py",
							"Assets/guard.png",
							"Assets/lootmodif.png",
							"Assets/macgyver.png",
							"Assets/path.png",
							"Assets/wall.png"]}},
	executables = executables


	)

# sets up exe file for main controller
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter"],
    "includes": ["syllogism_controller", "interface_controller", "image_controller", "venn_diagram", "region_manager", "region_struct"],
    "excludes": [],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SyllogismEvaluator",
    version="0.1",
    description="Syllogism Evaluator Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main_controller.py", base=base)],
)



# run using - python setup.py build
# check build folder for exe
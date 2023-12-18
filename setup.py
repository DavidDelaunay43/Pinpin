from cx_Freeze import setup, Executable

executables = [Executable("pinpin.py", icon = "ProjectFiles/Icons/pinpin_icon.ico")]

setup(
    name="pinpin",
    version="1.0.8",
    description="",
    executables=executables,
    options={
        "build_exe": {
            "includes": ["PySide2", "PIL"]
        }
    }
)

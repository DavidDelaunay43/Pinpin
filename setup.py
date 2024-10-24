from cx_Freeze import setup, Executable

executables: list[Executable] = [Executable("pinpin.py", icon = "ProjectFiles/Icons/pinpin_icon.ico")]

setup(
    name="pinpin",
    version="1.2.0b9",
    description="",
    executables=executables,
    options={
        "build_exe": {
            "includes": ["PySide2", "requests", "colorama"]
        }
    }
)

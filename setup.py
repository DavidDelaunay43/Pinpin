from cx_Freeze import setup, Executable

executables: list[Executable] = [
    Executable("pinpin.py", icon = "ProjectFiles/Icons/pinpin_icon.ico"),
    Executable("post_install.py", icon = "ProjectFiles/Icons/pinpin_dev_icon.ico"),
]

setup(
    name="pinpin",
    version="v1.2.0-beta.13",
    description="",
    executables=executables,
    options={
        "build_exe": {
            "includes": ["PySide2", "requests", "colorama"]
        }
    }
)

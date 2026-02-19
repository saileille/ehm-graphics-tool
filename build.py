"""Build the script to an exe."""
import sys
import traceback
from types import TracebackType


def show_exception_and_exit(exc_type: type[BaseException], exc_value: BaseException, tb: TracebackType):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press key to exit.")
    sys.exit(-1)


sys.excepthook = show_exception_and_exit


import PyInstaller.__main__


def main():
    """Build."""
    PyInstaller.__main__.run([
        "main.py",
        "--optimize=2",
        "--clean",
        "--onefile",
        "--name=ehm-graphics-tool",
        "--icon=favicon.ico",
        "--version-file=version.txt",
    ])


if __name__ == "__main__":
    main()
    input("Done")
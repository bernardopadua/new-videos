from argparse import ArgumentParser
from pathlib import Path
import os

parser = ArgumentParser(description="Simple tool for migration")
parser.add_argument("-i", "--init", action="store_true", help="Init folder to create migration")
parser.add_argument("-a", "--addversion", type=str, help="add the name of the file to be generated")

def checkVersionPath() -> tuple[bool, Path]:

    versionPath = (Path('./') / "versions")

    return (versionPath.exists(), versionPath)
        

def initFolder():
    fdExists, path = checkVersionPath()

    if not fdExists:
        path.mkdir()
    
def addVersion():
    fdExists, versionPath = checkVersionPath()
    maxVersion = 0

    if not fdExists:
        raise RuntimeError("No folder version")
    
    for file in os.listdir(versionPath):
        fileVersion = int(file.split("_")[0][1:])
        maxVersion = fileVersion if fileVersion > maxVersion else maxVersion


def main():
    args = parser.parse_args()

    if args.init:
        initFolder()
        return

    if args.addversion:
        addVersion()

if __name__=="__main__":
    main()
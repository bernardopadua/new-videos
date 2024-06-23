from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser(description="Simple tool for migration")
parser.add_argument("-i", "--init", action="store_true", help="Init folder to create migration")
parser.add_argument("-a", "--addversion", 
    type=str, 
    help="Add a new version. Need to inform the filename without '.sql'"
)
parser.add_argument("-r", "--run", action="store_true", help="Init folder to create migration")

def checkVersionPath() -> tuple[bool, Path]:

    versionPath = (Path(__file__).parent / "versions")

    return (versionPath.exists(), versionPath)
        
def initFolder():
    fdExists, path = checkVersionPath()

    if not fdExists:
        path.mkdir()
    
def addVersion(fileName: str) -> None:
    import os

    fdExists, versionPath = checkVersionPath()
    maxVersion = 0

    if not fdExists:
        raise RuntimeError("No folder version")
    
    for file in os.listdir(versionPath):
        fileVersion = int(file.split("_")[0][1:])
        maxVersion = fileVersion if fileVersion > maxVersion else maxVersion
    
    maxVersion += 1
    newFileName = fileName if ".sql" in fileName else f"{fileName}.sql"
    newFileName = f"V{maxVersion}_{newFileName}"
    open((versionPath / newFileName), "w").write("")

def main():
    args = parser.parse_args()

    if args.init:
        initFolder()
        return

    if args.addversion:
        addVersion(args.addversion)

if __name__=="__main__":
    main()
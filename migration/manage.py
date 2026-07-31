from os import environ, listdir
from pathlib import Path

# is running from virtualenv ?
import sys
avoidENVCheck = environ.get("AVOID_VIRTUALENV_CHECK", "False").lower()=="true"
if sys.prefix != sys.base_prefix and not avoidENVCheck:
    #avoiding problems with no migration module
    sys.path.append(Path(__file__).parent.parent.__str__())

from argparse import ArgumentParser
from migration.db.pgdbcontext import PgDBContext, UndefinedTable

parser = ArgumentParser(description="Simple tool for migration")
parser.add_argument("-i", "--init", action="store_true", help="Init folder to create migration")
parser.add_argument("-a", "--addversion", 
    type=str, 
    help="Add a new version. Need to inform the filename without '.sql'"
)
parser.add_argument("-r", "--run", action="store_true", help="Run migrations and init")

TABLE_MIGRATION_NAME="nvideo_migration_control_version"
COLUMN_MIGRATION_CONTROL="version_control"

def checkVersionPath() -> tuple[bool, Path]:
    versionPath = (Path(__file__).parent / "versions")
    return (versionPath.exists(), versionPath)

def migrationTableVersionControlExists() -> bool:
    conn = PgDBContext.getConn() 
    cur = conn.cursor()
    try:
        cur.execute(f"select 1 from {TABLE_MIGRATION_NAME};")
    except UndefinedTable:
        conn.rollback()
        return False
    return True

def createTableMigrationVersionControl() -> None: 
    conn = PgDBContext.getConn()
    cur = conn.cursor()
    cur.execute(f"create table {TABLE_MIGRATION_NAME} ( {COLUMN_MIGRATION_CONTROL} varchar(50) not null );")
    conn.commit()


def initMigration():
    PgDBContext.initDB()
    fdExists, path = checkVersionPath()
    migrationTableExists = migrationTableVersionControlExists()

    if not fdExists:
        path.mkdir()
    
    if not migrationTableExists:
        createTableMigrationVersionControl()
    
    PgDBContext.closeConn()

def addVersion(fileName: str) -> None:
    from datetime import datetime

    fdExists, versionPath = checkVersionPath()
    if not fdExists:
        raise RuntimeError("No folder version")

    timeNow = datetime.now().__format__("%Y%m%d-%H%M%S")
    newFileName = fileName if ".sql" in fileName else f"{fileName}.sql"
    newFileName = f"{timeNow}_{newFileName}"
    open((versionPath / newFileName), "w").write("")

def runMigrations() -> None:
    # If not init, just init
    initMigrrootation()

    #After initMigration the connection is closed
    PgDBContext.initDB()

    conn = PgDBContext.getConn()
    cur = conn.cursor()
    cur.execute(f"select {COLUMN_MIGRATION_CONTROL} from {TABLE_MIGRATION_NAME};")
    if cur.fetchone() == None:
        cur.execute(f"""
            insert into {TABLE_MIGRATION_NAME}
            ( {COLUMN_MIGRATION_CONTROL} )
            values
            (%s)
        """, ("0",))
        conn.commit()

    cur.execute(
        f"select {COLUMN_MIGRATION_CONTROL} from {TABLE_MIGRATION_NAME};"
    )
    versionControl = cur.fetchone()[0]
    folderVersions = (Path(__file__).parent / "versions")
    sortedFiles = sorted(
        listdir(folderVersions)
    )
    hasUpdate = False
    for file  in sortedFiles:
        version = file.split("_")[0]
        if version > versionControl:
            fileVersionApply = open(folderVersions / file).read()
            cur.execute(fileVersionApply)
            versionControl = version
            hasUpdate = True
    
    if hasUpdate:
        cur.execute(f"""
            update {TABLE_MIGRATION_NAME} set 
            {COLUMN_MIGRATION_CONTROL} = %s
        """, (versionControl,))
        conn.commit()
    
    PgDBContext.closeConn()

def main():
    args = parser.parse_args()

    if args.init:
        initMigration()
        return

    if args.addversion:
        addVersion(args.addversion)

    if args.run:
        runMigrations()

if __name__=="__main__":
    main()
# Typing ?
from io import TextIOWrapper

def load_dotenv(filename: TextIOWrapper):
    configRet = {}
    line = filename.readline()
    while line:
        k, v = line.strip().split("=")
        configRet[k] = v

        line = filename.readline()

    return configRet
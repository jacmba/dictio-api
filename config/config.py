import os


def getEnv(key: str, default: str) -> str:
    value = os.getenv(key)
    if value == None:
        return default
    return value


class Config:
    mongo_url = getEnv("MONGO_URL", "mongodb://localhost")
    mongo_db = getEnv("MONGO_DB", "dictio")
    debug = getEnv("DEBUG", "false") == "true"

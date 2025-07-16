import json
import hashlib
import os

def getHash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def loadCache(cachePath):
    if os.path.exists(cachePath):
        with open(cachePath, 'r') as f:
            return json.load(f)
    return {}

def saveCache(cachePath, data):
    with open(cachePath, 'w') as f:
        json.dump(data, f, indent=2)


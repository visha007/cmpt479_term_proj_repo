import os
from .tracker import runUsingCoverage
from .storage import loadCache, saveCache, getHash
from .utils import discoverTests

CACHE_FILE = 'jsonData/deps.json'

def runTests():
    import importlib

    os.makedirs('jsonData', exist_ok=True)
    cache = loadCache(CACHE_FILE)
    new_cache = {}

    for testID, testFunc in discoverTests():
        deps = cache.get(testID, {}).get("deps", [])
        changed = any(
            not os.path.exists(dep) or getHash(dep) != cache[testID]["hashes"].get(dep)
            for dep in deps
        )

        if testID not in cache or changed:
            print(f"Running test: {testID}")
            used = runUsingCoverage(testFunc)
            print("Used files:", used)
            new_cache[testID] = {
                "deps": list(used),
                "hashes": {f: getHash(f) for f in used if os.path.exists(f)}
            }
        else:
            print(f"Skipping unchanged test: {testID}")
            new_cache[testID] = cache[testID]

    saveCache(CACHE_FILE, new_cache)

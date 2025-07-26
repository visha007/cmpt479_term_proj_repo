import os
import shutil
import pytest

import coverage
from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item

from .storage import loadCache, saveCache, getHash

CACHE_FILE = "jsonData/deps.json"

new_cache = None
cache = None
ekstazi_enabled = False
cov = None


def pytest_addoption(parser):
    parser.addoption(
        "--ekstazi",
        action="store_true",
        help="select tests using ekstazi test selection",
    )
    parser.addoption(
        "--ekstazi-clean",
        action="store_true",
        help="clear ekstazi cache and run with ekstazi",
    )


# hook called when configuring pytest
def pytest_configure(config: Config):
    global ekstazi_enabled
    if config.getoption("--ekstazi") or config.getoption("--ekstazi-clean"):
        ekstazi_enabled = True
    if config.getoption("--ekstazi-clean"):
        shutil.rmtree("jsonData", ignore_errors=True)
        terminal = config.pluginmanager.get_plugin("terminalreporter")
        if terminal:
            terminal.write_line("[ekstazi] Cleaned ekstazi cache")


# hook called after pytest collection has been performed
def pytest_collection_modifyitems(session: Session, config: Config, items: list[Item]):
    global ekstazi_enabled, cache, new_cache
    if not ekstazi_enabled:
        return

    os.makedirs("jsonData", exist_ok=True)
    cache = loadCache(CACHE_FILE)
    new_cache = {}

    for test in items:
        test_id = test.nodeid
        deps = cache.get(test_id, {}).get("deps", [])
        if not deps:
            deps = {}
        changed = any(
            not os.path.exists(dep) or getHash(dep) != cache[test_id]["hashes"].get(dep)
            for dep in deps
        )
        # TODO: Skip only if previous run was successful
        if test_id in cache and not changed:
            test.add_marker(pytest.mark.skip(reason="Test and dependencies unchanged"))


# hook called before the setup, running, and teardown of every test
def pytest_runtest_logstart(nodeid: str, location: tuple[str, int | None, str]):
    global ekstazi_enabled, cache, new_cache, cov

    if not ekstazi_enabled:
        return

    cov = coverage.Coverage(data_file=None)
    cov.start()


# hook called after the setup, running, and teardown of every test
def pytest_runtest_logfinish(nodeid: str, location: tuple[str, int | None, str]):
    global ekstazi_enabled, cache, new_cache, cov

    if not ekstazi_enabled:
        return

    cov.stop()

    used_files = cov.get_data().measured_files()
    new_cache[nodeid] = {
        "deps": list(used_files),
        "hashes": {f: getHash(f) for f in used_files if os.path.exists(f)},
    }


def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode):
    global new_cache

    if not ekstazi_enabled:
        return

    saveCache(CACHE_FILE, new_cache)

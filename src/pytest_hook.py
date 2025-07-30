import coverage
import pytest
from pytest import TestReport
from _pytest.config import Config, ExitCode
from _pytest.main import Session
from _pytest.nodes import Item

from .storage import Storage, clear_cache

dep_cache = None
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
    global ekstazi_enabled, dep_cache
    if config.getoption("--ekstazi-clean"):
        clear_cache(config)
        terminal = config.pluginmanager.get_plugin("terminalreporter")
        if terminal:
            terminal.write_line("[ekstazi] Cleaned ekstazi cache")

    if config.getoption("--ekstazi") or config.getoption("--ekstazi-clean"):
        dep_cache = Storage(config)
        ekstazi_enabled = True


# hook called after pytest collection has been performed
def pytest_collection_modifyitems(session: Session, config: Config, items: list[Item]):
    global ekstazi_enabled, cache, new_cache
    if not ekstazi_enabled:
        return

    if dep_cache.is_first_run():
        # all tests run as normal
        return

    for test in items:
        if test.get_closest_marker("skip"):
            # already skipped so do nothing
            continue

        test_id = test.nodeid
        if dep_cache.is_skippable(test_id):
            test.add_marker(pytest.mark.skip(reason="Test and dependencies unchanged"))


# hook called before the setup, running, and teardown of every test
def pytest_runtest_logstart(nodeid: str, location: tuple[str, int | None, str]):
    global ekstazi_enabled, cache, new_cache, cov

    if not ekstazi_enabled:
        return

    cov = coverage.Coverage(data_file=None)
    cov.start()


def pytest_runtest_logreport(report: TestReport):
    if not ekstazi_enabled or report.when != "teardown" or report.skipped:
        return

    cov.stop()

    test_id = report.nodeid
    used_files = cov.get_data().measured_files()

    dep_cache.update_test(test_id, used_files, report.outcome)


def pytest_sessionfinish(session: Session, exitstatus: int | ExitCode):
    if not ekstazi_enabled:
        return

    dep_cache.save_cache()

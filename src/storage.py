import hashlib

from _pytest.config import Config

DEPS_FILE_PATH = "ekstazi/dependencies.json"
EMPTY_DICT = {"files": {}, "tests": {}}


def clear_cache(config: Config):
    config.cache.set(DEPS_FILE_PATH, EMPTY_DICT)


class Storage:
    _tracked_files = set()
    _changed_files = set()
    _data = {}
    """
    Structure:
    {
        "files": [ "path": "hash" ],
        "tests": [
            "test_id": {
                "deps": [ "filename" ],
                "passed": true/false
            }
        ]
    }
    """

    def __init__(self, config: Config):
        self._config = config
        self._data = self._load_data()
        self._process_file_changes()

    def _process_file_changes(self):
        for file, old_hash in list(self._data["files"].items()):
            new_hash = None
            try:
                new_hash = self._get_hash(file)
            except (FileNotFoundError, NotADirectoryError):
                # file doesn't exist (anymore)
                # treat as changed but remove from data
                self._changed_files.add(file)
                self._data["files"].pop(file)
                continue

            self._tracked_files.add(file)
            if new_hash != old_hash:
                self._changed_files.add(file)
                self._data["files"][file] = new_hash

    def _get_hash(self, path):
        """
        Raises:
            FileNotFoundError: File not found
            NotADirectoryError: Directory not found
        """
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _load_data(self):
        return self._config.cache.get(DEPS_FILE_PATH, EMPTY_DICT)

    def save_cache(self):
        self._config.cache.set(DEPS_FILE_PATH, self._data)

    def is_first_run(self):
        return not self._data

    def is_skippable(self, test_id):
        test_data = self._data["tests"].get(test_id)
        if test_data is None or not test_data["passed"]:
            # new test or failed previous run
            return False

        for file in test_data["deps"]:
            if file in self._changed_files:
                # dependency changed
                return False

        # passed previous run and no changed dependencies
        return True

    def update_test(self, test_id, file_deps, outcome):
        self._data["tests"][test_id] = {
            "deps": list(file_deps),
            "passed": outcome == "passed",
        }
        for file in file_deps:
            if file not in self._tracked_files:
                self._tracked_files.add(file)
                try:
                    self._data["files"][file] = self._get_hash(file)
                except (FileNotFoundError, NotADirectoryError):
                    # Edge case: transient .py files dependency (e.g., created by fixtures).
                    # Use hash "-1" because we can't track changes to these files.
                    # During collection:
                    #  - if exists: hash differs -> depending tests not skipped
                    #  - if doesn't exist: treated deleted -> depending tests not skipped
                    #
                    # Example: https://github.com/pytest-dev/pytest/blob/1b1375f/testing/_py/test_local.py#L1021
                    self._data["files"][file] = "-1"

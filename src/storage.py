import hashlib
import io
import tokenize
import ast
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

    def _get_ast_hash(self, path):
        """
        Returns a SHA256 hash of the Python file's AST, ignoring
        comments, whitespace, and docstrings.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()

            # Parse into AST
            tree = ast.parse(source)

            # Remove docstrings from all nodes
            self._remove_docstrings(tree)

            # Get a normalized string dump without line/col info
            ast_str = ast.dump(tree, include_attributes=False)

            return hashlib.sha256(ast_str.encode("utf-8")).hexdigest()

        except (SyntaxError, UnicodeDecodeError):
            # Fallback: binary or non-Python files
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()


    def _remove_docstrings(self, node):
        """
        Recursively remove docstrings from an AST node.
        """
        if not hasattr(node, "body"):
            return

        if isinstance(node.body, list) and node.body:
            # Check if first statement is a docstring
            if (isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
                node.body.pop(0)

            for child in node.body:
                self._remove_docstrings(child)
    
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
        try:
            return self._get_ast_hash(path)
        except FileNotFoundError:
            raise
        except NotADirectoryError:
            raise

    def _strip_comments(self, source):
        result = []
        io_obj = io.StringIO(source)
        for tok_type, tok_str, *_ in tokenize.generate_tokens(io_obj.readline):
            if tok_type == tokenize.COMMENT:
                continue
            elif tok_type == tokenize.STRING:
                # skip module-level or function-level docstrings
                if result and result[-1] == '\n':
                    continue
            result.append(tok_str)
        return ''.join(result)

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

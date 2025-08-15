# Ekstazi for Python
This repository contains the code for our CMPT 479 (Summer 2025) term project — **Ekstazi for Python**, a regression test selection tool inspired by Ekstazi for Java, adapted to work with Python projects using `pytest`.

## Project Structure

```
.
├── pyproject.toml
├── README.md
├── requirements.txt
└── src
    ├── config.py
    ├── __init__.py
    ├── pytest_hook.py
    └── storage.py
```

---

### 1. Install Project dependencies

From the root of the target project (e.g., `click`, `flask`, etc.):

```bash
pip install path/to/ekstazi4py/
```

---

### 2. Running the Tool

From the root directory of the project you want to test (i.e., the folder where your test files are located), run:

```bash
pytest --ekstazi
```

This will:
- Run only tests whose dependencies have changed since the last run
- Cache dependency info in `pytest_project_root/.pytest_cache/v/ekstazi/dependencies.json`


> ⚠️ **Note:** If you’re following along with our demo in the [Basic Example](#basic-example) below,  
> this root directory is the same folder where you created `test_sample.py`.  
> In your own project, simply replace `test_sample.py` with your actual test files.

---

## Cleaning the Cache

To delete the dependency cache:

```bash
pytest --ekstazi-clean
```

This resets the `.pytest_cache/v/ekstazi/dependencies.json` file contents at the start of the pytest run.

---

## Where Is the Cache Stored?

Dependencies and hash info are stored in:

```
pytest_project_root/.pytest_cache/v/ekstazi/dependencies.json
```

---

## Example
### Basic Example
Create a test file in a pytest project like:

**`test_sample.py`**:
```python
from sampleModule import add

def test_add():
    assert add(1, 2) == 3
```

**`sampleModule.py`**:
```python
def add(a, b):
    return a + b
```

Add `ekstazi4py` and `pytest` dependencies.

Now run:

```bash
pytest --ekstazi
```

---

### Realistic Example: Running Ekstazi for Python on Click
This example uses `click` project but can be adapted for other python test projects
```
# Clone repo
git clone https://github.com/pallets/click.git
cd click

# Create virtual environment (replace `python` with `python3` if needed):
# We recommend running ekstazi4py inside a virtual environment to keep dependencies isolated and avoid conflicts with other Python projects.
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install project's dev dependencies (pip doesn't fully support click's pyproject.toml so manually install pytest)
pip install -e . pytest

# Install Ekstazi for Python
pip install ../path/to/ekstazi4py
# or
pip install git+https://github.com/visha007/ekstazi4py 

# you may have to re-activate the environment 
$ source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Run all tests for the first time (builds dependency cache)
# you may have to re-activate the virtual environment first depending on the machine if there are issues
pytest --ekstazi

# Simulate a code change in test project
echo -e "\nx = 42" >> src/click/core.py

# Re-run tests — only those affected by the change will run
pytest --ekstazi

# Re-run once more with no changes - no new tests should run (compare results across runs)
pytest --ekstazi
```

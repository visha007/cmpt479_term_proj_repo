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

### 1. Install Python dependencies

From the root of the target project (e.g., `click`, `flask`, etc.):

```bash
pip install path/to/ekstazi4py/
pip install -r path/to/ekstazi4py/requirements.txt
```

---

## 2. Running the Tool

From the root directory of the project you want to test (i.e., the folder where your test files are located), run:

```bash
pytest --ekstazi
```

This will:
- Run only tests whose dependencies have changed since the last run
- Cache dependency info in `pytest_project_root/jsonData/deps.json`


> ⚠️ **Note:** If you’re following along with our demo in the [Basic Example](#basic-example) below,  
> this root directory is the same folder where you created `test_sample.py`.  
> In your own project, simply replace `test_sample.py` with your actual test files.

---

## Cleaning the Cache

To delete the dependency cache:

```bash
pytest --ekstazi-clean
```

This removes the `jsonData` directory at the start of the pytest run.

---

## Where Is the Cache Stored?

Dependencies and hash info are stored in:

```
pytest_project_root/jsondata/deps.json
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

Add `cmpt479_term_proj_repo` and `requirements.txt` dependencies.

Now run:

```bash
pytest --ekstazi
```

---

### Realistic Example: Running Ekstazi for Python on Click
This example uses `click` but can be adapted for other python test projects
```
# Clone Click
git clone https://github.com/pallets/click.git
cd click

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Click's dev dependencies
pip install .[dev]

# Install Ekstazi for Python
pip install ../path/to/ekstazi4py
pip install -r ../path/to/ekstazi4py/requirements.txt

# Run all tests for the first time (builds dependency cache)
pytest --ekstazi

# Simulate a code change
echo "# random change" >> src/click/core.py

# Run tests again — only those affected by the change will run
pytest --ekstazi

# Run once more with no changes — no tests should run
pytest --ekstazi
```

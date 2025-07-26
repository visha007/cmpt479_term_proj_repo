# cmpt479_term_proj_repo
This repo will contain code for our term project for CMPT479 D2 (Summer 2025)

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

From your pytest project using `pip`, do

```bash
pip install path/to/cmpt479_term_proj_repo/
pip install -r path/to/cmpt479_term_proj_repo/requirements.txt
```

---

## 2. Running the Tool

From the pytest project root (where `test_sample.py` is), run:

```bash
pytest --ekstazi
```

This will:
- Run only tests whose dependencies have changed
- Cache dependency info in `pytest_project_root/jsonData/deps.json`

---

## Cleaning the Cache

To delete the dependency cache:

```bash
pytest --ekstazi-clean
```

This removes the `jsonData` directory at the start of the pytest run.

---

## Where Is the Cache Stored?

- Dependencies and hash info are stored in:

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

### Realistic Example: Testing on the pytest repo
This example requires `pdm` but can be adapted for other package managers
```sh
git clone https://github.com/pytest-dev/pytest.git
cd pytest
pdm install
pdm add ../path/to/cmpt479_term_proj_repo
pdm run pytest --ekstazi testing/_py/test_local.py # run a minimal test set. observe results
echo "# random change" >> src/_pytest/_py/error.py
pdm run pytest --ekstazi testing/_py/test_local.py # only some tests depending on error.py will be run
pdm run pytest --ekstazi testing/_py/test_local.py # no tests should run
```

TODO: Sometimes tests are missed? I'm not sure why. Maybe there's some overlap in the coverage thing so we need a global dictionary or something

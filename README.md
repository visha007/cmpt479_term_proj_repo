# cmpt479_term_proj_repo
This repo will contain code for our term project for CMPT479 D2 (Summer 2025)

## Project Structure

```
.
├── cmpt479_term_proj_repo/
│   ├── __init__.py
│   ├── requirements.txt
│   ├── cli.py
│   ├── config.py
│   ├── runner.py
│   ├── storage.py
│   ├── tracker.py
│   └── utils.py
├── sampleModule.py
├── test_sample.py
```

---

### 1. Install Python dependencies

```bash
pip install -r cmpt479_term_proj_repo/requirements.txt
```

---

## 2. Running the Tool

From the project root (where `test_sample.py` is), run:

```bash
python -m cmpt479_term_proj_repo.cli run
```

This will:
- Discover test files matching `test_*.py`
- Run only tests whose dependencies have changed
- Cache dependency info in `cmpt479_term_proj_repo/jsonData/deps.json`

---

## Cleaning the Cache

To delete the dependency cache:

```bash
python -m cmpt479_term_proj_repo.cli clean
```

This removes the `jsonData` directory.

---

## Where Is the Cache Stored?

- Dependencies and hash info are stored in:

  ```
  cmpt479_term_proj_repo/jsondata/deps.json
  ```

---

## Example Test

Create a test file like:

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

Now run:

```bash
python -m cmpt479_term_proj_repo.cli run
```

---

## Realistic Example Test
[See example here](EXAMPLE.md)

# Testing on the pytest repo
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

from: https://github.com/catkira/py3gpp
- clone the repo
- install it

To install, need to enable python3 venv environment
from: https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install py3gpp

## or clone the repo and
python3 -m pip install -e .
```

if use for the first time, install other depedencies \
in vscode console
```
pip install numpy
pip install scipy
pip install matplotlib
```
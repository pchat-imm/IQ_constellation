from: https://github.com/catkira/py3gpp
- clone the repo
- install it

To install, need to enable python3 venv environment
from: https://stackoverflow.com/questions/75602063/pip-install-r-requirements-txt-is-failing-this-environment-is-externally-mana

- make **my_venv** environment
```
python3 -m venv my_venv
```
see if you have `my_venv` folder, then activate it
```
source my_venv/bin/activate
```
then install all infrastructure
```
pip install numpy
pip install scipy
pip install matplotlib
pip install py3gpp
pip3 install ipykernel
```
or
`python3 -m pip install py3gpp`

## or clone the repo and
`python3 -m pip install -e .`

## for jupyter
- create new notebook in `.ipynb`
- select kernel `my_venv/myproject_kernel`
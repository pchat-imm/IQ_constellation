### my_venv virtual environment
create `my_venv` environment
```
python3 -m venv my_venv
```
see if you have `my_venv` folder, then activate it
```
source my_venv/bin/activate
```
then install all required components
```
pip install numpy
pip install scipy
pip install matplotlib
pip install py3gpp
pip3 install ipykernel
```
for `py3gpp`, can clone then install 
from: https://github.com/catkira/py3gpp
`python3 -m pip install py3gpp`
or clone the repo and
`python3 -m pip install -e .`

## for jupyter
- create new notebook in `.ipynb`
- select kernel `my_venv/myproject_kernel`
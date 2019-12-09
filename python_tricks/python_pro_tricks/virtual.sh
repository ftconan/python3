# @author: magician
# @date: 2019/12/9
# @file: virtual.sh

which pip3
python3 -m venv ./venv
ls venv/
which pip3
source ./venv/bin/activate
which pip3
which python
pip list
pip install schedule
pip list
deactivate

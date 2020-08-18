#!/bin/bash
cd $(dirname $(readlink -f $0))/..

PYTHON3=python3.7
PYTHON2=python2.7

# python3
echo -e "\n* Setup application in develop mode for Python3"
$PYTHON3 -m virtualenv ../venv3
[ -d ../venv3 ] || { echo "failed to create py3 venv !!"; exit 1; }
. ../venv3/bin/activate
pip install -U pip setuptools wheel
pip install -e ./
pip install -r dev_requirements.txt
# fix till release flask-seasurf>=0.2.3 on pypi
python -c 'import flask_seasurf as m; print(m.__version__>="0.2.3")' |grep -iq 'true' || \
    pip install -U git+git://github.com/maxcountryman/flask-seasurf.git@0.2.3#egg=flask_seasurf
deactivate

# python2
echo -e "\n* Setup application in develop mode for Python2"
$PYTHON2 -m virtualenv ../venv2
[ -d ../venv2 ] || { echo "failed to create py2 venv !!"; exit 1; }
. ../venv2/bin/activate
pip install -U pip setuptools wheel
pip install -e ./
pip install -r dev_requirements.txt
# fix till release flask-seasurf>=0.2.3 on pypi
python -c 'import flask_seasurf as m; print(m.__version__>="0.2.3")' |grep -iq 'true' || \
    pip install -U git+git://github.com/maxcountryman/flask-seasurf.git@0.2.3#egg=flask_seasurf
deactivate

echo -e "\n* Done\n"

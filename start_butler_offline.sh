#!/bin/sh

set -e

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
VENV_DIR=$parent_path/.venv

if [[ ! -d $VENV_DIR ]]; then
    echo ""
    echo "#################################"
    echo "#### BudgetButlerWeb offline ####"
    echo "######### Installation ##########"
    echo "#################################"
    echo "#################################"
    echo ""

    python -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    pip install -r $parent_path/butler_offline/requirements.txt

    echo ""
    echo "#################################"
    echo "#### BudgetButlerWeb offline ####"
    echo "############ Ready  #############"
    echo "#################################"
    echo "#################################"
    echo ""
fi

source $VENV_DIR/bin/activate

echo ""
echo "#################################"
echo "#### BudgetButlerWeb offline ####"
echo "######### Starting ...  #########"
echo "#################################"
echo "#################################"
echo ""

echo "Starting BudgetButlerWeb local server"
cd "$parent_path/butler_offline"
export FLASK_APP=start_as_flask.py 

eval  "sleep 4s && chromium --app=http://localhost:5000" &
flask run


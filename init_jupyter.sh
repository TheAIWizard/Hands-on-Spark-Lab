#!/bin/sh

# Clone the repository in /home/jovyan/work
# REPO=tuto-interactif-minimal
REPO=Hands-on-Spark-Lab
REPO_URL=https://github.com/TheAIWizard/${REPO}.git
# $1 is a positional argument
IPYNB_PATH=$1
git clone $REPO_URL $ROOT_PROJECT_DIRECTORY/${REPO}
chown -R jovyan:users $ROOT_PROJECT_DIRECTORY/${REPO}

# Install dependencies
[ -f /home/jovyan/work/requirements.txt ] && pip install -r /home/jovyan/work/requirements.txt

# Open a given notebook when starting Jupyter Lab
jupyter server --generate-config
# echo "c.LabApp.default_url = '/lab/tree/${REPO}/First-steps-with-Spark/First-steps-with-Spark.ipynb'" >> $HOME/.jupyter/jupyter_server_config.py
[ -z "$IPYNB_PATH" ] || echo "c.LabApp.default_url = '/lab/tree/${REPO}/${IPYNB_PATH%.*}/${IPYNB_PATH}${.ipynb}'" >> $HOME/.jupyter/jupyter_server_config.py

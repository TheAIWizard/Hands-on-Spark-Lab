#!/bin/sh

# Clone the repository in /home/jovyan/work
REPO=tuto-interactif-minimal
REPO_URL=https://github.com/TheAIWizard/${REPO}.git
IPYNB_PATH=First steps with Spark.ipynb
git clone $REPO_URL $ROOT_PROJECT_DIRECTORY/${REPO}
chown -R jovyan:users $ROOT_PROJECT_DIRECTORY/${REPO}

# Install dependencies
[ -f /home/jovyan/work/requirements.txt ] && pip install -r /home/jovyan/work/requirements.txt

# Open a given notebook when starting Jupyter Lab
[ -z "$IPYNB_PATH" ] || echo "c.LabApp.default_url = '/lab/tree/${REPO}/${IPYNB_PATH%.*}/${IPYNB_PATH}'" >> $HOME/.jupyter/jupyter_server_config.py

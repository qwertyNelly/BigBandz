
from dotenv import load_dotenv
from os import getcwd
from pathlib import Path
from os import environ
from logging import getLogger

from bndni.app.src.env import load_env
from bndni.app.exceptions.EnviornmentExceptions import ErrorLoadingEnviornment

# Instantiate Log
log = getLogger('bndni')

# Instantiate Environment
ENV_PATH = Path(getcwd())
ENV_FILE = ENV_PATH.joinpath('.env')
load_env(ENV_FILE)








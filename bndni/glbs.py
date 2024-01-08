
from pathlib import Path
from os import getcwd
from logging import getLogger

log = getLogger('bndni.glbs')
ENV_PATH = Path(getcwd())
log.debug(f'Set Environment Path to : {ENV_PATH}')

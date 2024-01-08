
from dotenv import load_dotenv
from logging import getLogger
from pathlib import Path
from os.path import exists

from bndni.app.exceptions.EnviornmentExceptions import ErrorLoadingEnviornment

log = getLogger('bndni.app.src.env')


def load_env(env_path: Path):
    # Instantiate Environment
    if exists(env_path.joinpath('.env')):
        log.debug(f'Found Environment File : {env_path.joinpath(".env")}')
        env = load_dotenv(env_path.joinpath('.env'))
        if env:
            log.debug(f'Successfully Loaded Environment')
        else:
            log.exception(ErrorLoadingEnviornment(f'Path : {env_path.joinpath(".env")}'))
            raise ErrorLoadingEnviornment(f'Path : {env_path.joinpath(".env")}')
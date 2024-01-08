#!/bin/python3
import datetime
from pandas import read_json, DataFrame
from kucoin.user.user import UserData
from kucoin.client import Market, Trade
from os import environ
from pathlib import Path
from logging import getLogger
from dotenv import load_dotenv
from bndni.app.src.env import load_env
from vyper import e

from bndni.app.exceptions.APIExceptions import APIKeyError, APISecretError, APIPassphraseError

log = getLogger('bndni.app.api.user')
load_env(Path('/Users/ben/crypto/bndni/bndni/.env'))
load_dotenv('.env')

DATA_DIR = Path("/Users/ben/crypto/bndni/bndni/data")


class KUser(UserData):
    """

    """
    # TODO: Add logic for resource consumption
    spot_resource_limit: int = 3000
    future_resource_limit: int = 2000
    # Refresh after 30 seconds
    resource_limit_refresh: int = 30

    def __init__(self,
                 key: str = environ.get('API_KEY'),
                 secret: str = environ.get('API_SECRET'),
                 passphrase: str = environ.get('API_PASSPHRASE')
                 ):
        """
        Initializes the Client that Authenticates with Kucoin API
        :param key: API Key
        :param secret: API Secret
        :param passphrase: API Passphrase
        """

        if key is None:
            raise APIKeyError(f'Could not load API Key from the environment : {key}')
        if secret is None:
            raise APISecretError(f'Could not Load Secret from the environment : {secret}')
        if passphrase is None:
            raise APIPassphraseError(f'Could not load Passphrase from the enviornment : {passphrase}')
        super().__init__(key, secret, passphrase)
        self.market = Market(url='https://api.kucoin.com')
        self.trade = Trade(key, secret, passphrase)
        self.current_time = datetime.datetime.now()
        self.save_all_symbols()
        self.save_all_tickers()
        pass

    def get_all_symbols(self) -> DataFrame:
        """
        Query Kucoin to get all the currency symbols
        :return: A Dataframe of all the symbols
        """
        request_weight = 4
        self.spot_resource_limit = self.spot_resource_limit - request_weight
        try:
            print(self.market.get_symbol_list())
            res = (self.market.get_symbol_list())
            return res
        # TODO: Fix this Bigly
        except Exception as e:
            log.exception(e)

    def get_all_tickers(self):
        request_weight = 15
        self.spot_resource_limit = self.spot_resource_limit - request_weight
        # check if necessary resources are there
        if self.spot_resource_limit > (request_weight - 1):
            return self.market.get_all_tickers()

    def save_all_tickers(self):
        """

        :return:
        """
        ticker_filename = DATA_DIR.joinpath('tickers.csv')
        tickers = self.get_all_tickers()
        self.write_to_file(ticker_filename, tickers)
        pass

    def save_all_symbols(self):
        """
        Fetches and saves all symbols to the data directory
        :return:
        """
        symbol_filename = DATA_DIR.joinpath('symbols.csv')
        symbols = self.get_all_symbols()
        write_to_file(symbol_filename, symbols)


def write_to_file(filename, list_to_write):
    with open(filename, 'w+') as f:
        for sy in list_to_write:
            print(sy)
            f.write(sy.__str__())
            f.write('\n')


if __name__ == "__main__":
    usr = KUser()
    print(usr.market.get_all_tickers())

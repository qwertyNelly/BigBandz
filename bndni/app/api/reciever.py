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
from kucoin.client import WsToken

from bndni.app.exceptions.APIExceptions import APIKeyError, APISecretError, APIPassphraseError

log = getLogger('bndni.app.api.user')
load_env(Path('/Users/ben/crypto/bndni/bndni/.env'))
load_dotenv('.env')

DATA_DIR = Path("/Users/ben/crypto/bndni/bndni/data")


class KUser(UserData):
    """

    """
    market = Market(url='https://api.kucoin.com')
    trade: Trade = None
    # TODO: Add logic for resource consumption
    spot_resource_limit: int = 3000
    future_resource_limit: int = 2000
    # Refresh after 30 seconds
    resource_limit_refresh: int = 30
    last_trade = None
    last_trade_unit_price = None
    last_trade_volume = None

    # Accounts
    funds_usd = 0
    token_amount = 0

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
        self.token = WsToken()
        self.server = self.market.get_server_timestamp()

        # Trade Info
        self.last_trade = None
        self.last_trade_unit_price = None
        self.last_trade_volume = None

        self.save_all_symbols()
        self.save_all_tickers()
        pass

    @classmethod
    def contemplate_trade(cls, symbol: str, current_price, bid, ask, sequence, size):
        symbol = symbol.split(':')[1]
        print(cls.market.get_24h_stats(symbol))
        if cls.last_trade is None:
            cls.trade.create_limit_order(symbol=symbol, price=bid, side='buy', )


    def get_all_symbols(self) -> DataFrame:
        """
        Query Kucoin to get all the currency symbols
        :return: A Dataframe of all the symbols
        """
        request_weight = 4
        self.spot_resource_limit = self.spot_resource_limit - request_weight
        try:
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
        write_to_file(ticker_filename, tickers)
        pass

    def save_all_symbols(self):
        """
        Fetches and saves all symbols to the data directory
        :return:
        """
        symbol_filename = DATA_DIR.joinpath('symbols.csv')
        symbols = self.get_all_symbols()
        write_to_file(symbol_filename, symbols)
        pass


def write_to_file(filename, list_to_write):
    """

    :param filename:
    :param list_to_write:
    :return:
    """
    with open(filename, 'w+') as f:
        for sy in list_to_write:
            f.write(sy.__str__())
            f.write('\n')
            pass
        f.flush()
        f.close()
        pass



if __name__ == "__main__":
    usr = KUser()
    print(usr.market.get_all_tickers())

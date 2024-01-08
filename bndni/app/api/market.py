from kucoin.client import Market

global CLIENT

CLIENT = Market(url='https://api.kucoin.com')



def get_symbol_kline(symbol: str, time: str):
    """
    """
    try:
        return CLIENT.get_kline(symbol, time)

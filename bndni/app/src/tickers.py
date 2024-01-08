from kucoin.client import Market

client = Market(url='https://api.kucoin.com')


def get_symbol_kline(symbol: str, time: str):
    """
    """
    return client.get_kline(symbol, time)

#!/bin/python3.11

import asyncio
from kucoin.client import WsToken
from kucoin.ws_client import KucoinWsClient
from pandas import read_json
from json import loads
from bndni.app.api.reciever import KUser
from dotenv import load_dotenv


load_dotenv('../.env')


async def main():
    Client = KUser()
    print(Client.get_account_ledger())

    async def deal_msg(msg):
        """
        Route Messages
        :param msg:
        :return:
        """
        if msg['topic'] == '/market/ticker:BTC-USDT':
            handle_market(msg)
        elif msg['topic'] == '/spotMarket/level2Depth5:BTC-USDT':
            handle_spot(msg)
        return msg

    def handle_spot(msg):
        """{
        'topic': '/spotMarket/level2Depth5:BTC-USDT',
        'type': 'message',
        'data': {'asks':
                    [
                        ['43877.9', '1.41059829'],
                        ['43879.4', '0.0005'],
                        ['43879.5', '0.227972'],
                        ['43880.3', '0.06571392'],
                        ['43880.4', '0.28626377']
                    ],
                'bids':
                    [
                        ['43877.8', '1.91735691'],
                        ['43876.4', '0.07920392'],
                        ['43875.8', '0.09622868'],
                        ['43873.9', '0.1367832'],
                        ['43873.8', '0.227972']
                    ],
            'timestamp': 1704704505875},
            'subject': 'level2'}
        """
        data = msg['data']
        asks = data['asks']
        print(asks)

    def handle_market(msg):
        """
        {'bestAsk': '43891.1', 'bestAskSize': '3.05115453', 'bestBid': '43891', 'bestBidSize': '0.60044283',
        'price': '43891', 'sequence': '10337759482', 'size': '0.00088438', 'time': 1704704151243}
        :param msg:
        :return:
        """
        data = msg['data']
        current_price = data['price']
        ask = data['bestAsk']
        ask_size = data['bestAskSize']
        bid = data['bestBid']
        bid_size = data['bestBidSize']
        seq = data['sequence']
        size = data['size']
        time = data['time']
        KUser.contemplate_trade(msg['topic'], current_price, bid, ask, seq, size)




    # is public
    client = WsToken()
    #is private
    # client = WsToken(key='', secret='', passphrase='', is_sandbox=False, url='')
    # is sandbox
    # client = WsToken(is_sandbox=True)
    ws_client = await KucoinWsClient.create(None, client, deal_msg, private=False)
    await ws_client.subscribe('/market/ticker:BTC-USDT')
    await ws_client.subscribe('/spotMarket/level2Depth5:BTC-USDT')
    while True:
        await asyncio.sleep(60)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
from flask import Flask, render_template_string
from binance.client import Client
import pandas as pd
import time

# Testnet API bilgilerini gir
API_KEY = 'uf7ey6JcjtFGjBLUEumvFrTLatQh8aWQV1GL23X956hFf4ujoYBCYPuwLlmI3JHV'
API_SECRET = 'tjnWfFJxUxOkKQlO68ZQh1j7XyPZyvoxdfn1WDzYd8cVnxIpQGJTwQMmFjUkWUzd'

client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = 'ETHUSDT'
interval = '15m'
quantity = 0.001

app = Flask(__name__)

def get_data():
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['ma_short'] = df['close'].rolling(window=5).mean()
    df['ma_long'] = df['close'].rolling(window=20).mean()
    df['signal'] = 0
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1
    df.loc[df['ma_short'] < df['ma_long'], 'signal'] = -1
    df['trade'] = df['signal'].diff()
    return df

def get_wallet():
    info = client.get_account()
    balances = {b['asset']: float(b['free']) for b in info['balances'] if float(b['free']) > 0}
    eth = balances.get('ETH', 0)
    usdt = balances.get('USDT', 0)
    return eth, usdt

def place_order(signal):
    if signal == 1:
        return client.order_market_buy(symbol=symbol, quantity=quantity)
    elif signal == -2:
        return client.order_market_sell(symbol=symbol, quantity=quantity)

@app.route('/')
def index():
    df = get_data()
    latest = df.iloc[-1]
    signal = latest['trade']
    close_price = latest['close']
    signal_text = '⏳ Bekle'

    if signal == 1:
        signal_text = '📈 ALIM sinyali'
        place_order(signal)
    elif signal == -2:
        signal_text = '📉 SATIŞ sinyali'
        place_order(signal)

    eth, usdt = get_wallet()

    return render_template_string('''
    <html>
    <head><title>Testnet Bot</title></head>
    <body style="font-family:sans-serif; padding:20px;">
        <h1>🤖 Binance Testnet Alım-Satım Botu</h1>
        <p><b>Parite:</b> {{ symbol }}</p>
        <p><b>Son Fiyat:</b> {{ close }} USDT</p>
        <p><b>Sinyal:</b> {{ signal_text }}</p>
        <hr>
        <h2>💰 Cüzdan</h2>
        <p><b>ETH:</b> {{ eth }}</p>
        <p><b>USDT:</b> {{ usdt }}</p>
        <hr>
        <h2>📊 Son 5 Kapanış</h2>
        <ul>
        {% for price in last_prices %}
            <li>{{ price }}</li>
        {% endfor %}
        </ul>
        <p><i>Sayfa yenilendikçe güncellenir.</i></p>
    </body>
    </html>
    ''', symbol=symbol, close=close_price, signal_text=signal_text,
         eth=eth, usdt=usdt, last_prices=list(df['close'].tail(5)))

if __name__ == '__main__':
    app.run(debug=True)

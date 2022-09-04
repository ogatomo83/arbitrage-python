# API通信で利用
import json
import requests
import ccxt
from zaifapi import *
import pybitflyer

# APIキー＆シークレットキー(Huobi)
huobi_apiKey = "Huobi JapanのAPIキーを入力"
huobi_secret = "Huobi Japanのシークレットキーを入力"

# APIキー＆シークレットキー(Coincheck)
coincheck_apiKey  = "coincheckのAPIキーを入力"
coincheck_secret  = "coincheckのシークレットキーを入力"

# APIキー＆シークレットキー(bitflyer)
bitflyer_apiKey  = "xxxxxxxxxxxxxxxx"
bitflyer_secret  = "xxxxxxxxxxxxxxxx"

# インスタンス
huobi = ccxt.huobijp({'apiKey': huobi_apiKey,'secret': huobi_secret})
coincheck = ccxt.coincheck({'apiKey': coincheck_apiKey,'secret': coincheck_secret})
# https://github.com/yagays/pybitflyer
bitflyer = ccxt.bitflyer({'apiKey': bitflyer_apiKey, 'secret': bitflyer_secret})

# 取引通過（ビットコイン以外を指定したい場合はここを修正）
gmo_symbol = "BTC"
huobi_symbol = "BTC/JPY"
coincheck_symbol = "BTC/JPY"
zaif_symbol = "btc_jpy"
bitflyer_symbol = "BTC_JPY"
bit_point_symbol = "BTCJPY"

def zaif_ticker(symbol):
  zaif = ZaifPublicApi()
  result = zaif.ticker(symbol)
  return result

def huobi_ticker(symbol):
  result = huobi.fetch_ticker(symbol = symbol)
  return result

def coincheck_ticker(symbol):
  result = coincheck.fetch_ticker(symbol = symbol)
  return result

def bitflyer_ticker(symbol):
  result = bitflyer.fetch_ticker(symbol = symbol)
  return result

def bit_point_ticker(symbol):
  base_url = 'https://smartapi.bitpoint.co.jp/bpj-smart-api'
  path     = '/api/depth?symbol=' + symbol + '&limit=5'
  result = requests.get(base_url + path).json()
  return result
import repository
import time
from time import sleep
from itertools import count
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams
rcParams["font.family"]     = "sans-serif"
rcParams["font.sans-serif"] = "Hiragino Maru Gothic Pro"
plt.style.use('fivethirtyeight')

# グラフ軸
index           = count() # x軸(カウント)
x               = []          # x軸
y_huobi_ask     = []          # Huobi(買値)
y_huobi_bid     = []          # Huobi(売値)
y_zaif_ask      = []          # Zaif(買値)
y_zaif_bid      = []          # Zaif(売値)
y_coincheck_ask = []
y_coincheck_bid = []
y_bitflyer_ask  = []
y_bitflyer_bid  = []
y_bit_point_ask = []
y_bit_point_bid = []

# count
huobi_buy = 0
huobi_sell = 0
zaif_buy = 0
zaif_sell = 0
coincheck_buy = 0
coincheck_sell = 0
bitflyer_buy = 0
bitflyer_sell = 0
max_kakakusa = 0
beyond_value = 0
buy_sell_change = 0
buy_sell_change_beyond_value = 0
buy_sell_change_flag = 0
buy_sell_change_beyond_value_flag = 0

def animate(i):
  global huobi_buy
  global huobi_sell
  global zaif_buy
  global zaif_sell
  global coincheck_buy
  global coincheck_sell
  global bitflyer_buy
  global bitflyer_sell
  global max_kakakusa
  global beyond_value
  global buy_sell_change
  global buy_sell_change_beyond_value
  global buy_sell_change_flag
  global buy_sell_change_beyond_value_flag
  # X軸
  x.append(next(index) / 6)
  # Y軸
  with ThreadPoolExecutor(max_workers=5) as executor:
    executor.submit(get_huobi)
    # executor.submit(get_zaif)
    # executor.submit(get_coincheck)
    executor.submit(get_bitflyer)
    # executor.submit(get_bit_point)
  
  buy = {
    "huobi": y_huobi_ask[-1],
    # "zaif": y_zaif_ask[-1],
    # "coincheck": y_coincheck_ask[-1],
    "bitflyer": y_bitflyer_ask[-1],
    # "bit_point": y_bit_point_ask[-1]
  }
  sell = {
    "huobi": y_huobi_bid[-1],
    # "zaif": y_zaif_bid[-1],
    # "coincheck": y_coincheck_bid[-1],
    "bitflyer": y_bitflyer_bid[-1],
    # "bit_point": y_bit_point_bid[-1]
  }
  buy_min = min(
    y_huobi_ask[-1],
    # y_zaif_ask[-1],
    # y_coincheck_ask[-1],
    y_bitflyer_ask[-1],
    # y_bit_point_ask[-1]
  )
  sell_max = max(
    y_huobi_bid[-1],
    # y_zaif_bid[-1],
    # y_coincheck_bid[-1],
    y_bitflyer_bid[-1],
    # y_bit_point_bid[-1]
  )
  kakakusa = float(sell_max - buy_min)

  # アービトラージ(買い取引所特定)
  if buy_min == buy.get("huobi"):
    buy_name = "Huobi Japan"
  # elif buy_min == buy.get("zaif"):
  #   buy_name = "Zaif"
  # elif buy_min == buy.get("coincheck"):
  #   buy_name = "coincheck"
  elif buy_min == buy.get("bitflyer"):
    buy_name = "bitflyer"
    # bitflyer_buy += 1
  # elif buy_min == buy.get("bit_point"):
  #   buy_name = "bitpoint"

  # アービトラージ(売り取引所特定)
  if sell_max == sell.get("huobi"):
    sell_name = "Huobi Japan"
  # elif sell_max == sell.get("zaif"):
  #   sell_name = "Zaif"
  # elif sell_max == sell.get("coincheck"):
  #   sell_name = "coincheck"
  elif sell_max == sell.get("bitflyer"):
    sell_name = "bitflyer"
  #   bitflyer_sell += 1
  # elif sell_max == sell.get("bit_point"):
  #   sell_name = "bitpoint"

  if buy_name != sell_name:
    if buy_name == "Huobi Japan":
      huobi_buy += 1
      bitflyer_sell += 1
      if buy_sell_change_flag == 0 or buy_sell_change_flag == 2:
        buy_sell_change_flag = 1
        buy_sell_change += 1
      if (buy_sell_change_beyond_value_flag == 0 or buy_sell_change_beyond_value_flag == 2) and kakakusa > 5000:
        buy_sell_change_beyond_value_flag = 1
        buy_sell_change_beyond_value += 1
    if buy_name == "bitflyer":
      huobi_sell += 1
      bitflyer_buy += 1
      if buy_sell_change_flag == 0 or buy_sell_change_flag == 1:
        buy_sell_change_flag = 2
        buy_sell_change += 1
      if (buy_sell_change_beyond_value_flag == 0 or buy_sell_change_beyond_value_flag == 1) and kakakusa > 5000:
        buy_sell_change_beyond_value_flag = 2
        buy_sell_change_beyond_value += 1
    if kakakusa > max_kakakusa:
      max_kakakusa = kakakusa
    if kakakusa > 5000:
      beyond_value += 1

  # グラフ設定
  plt.cla()
  main_text = "買:" + buy_name + " 売:" + sell_name + " 価格差利益:" + str(float(kakakusa)) + "[円]" + "\nhuobi : (" + str(huobi_buy) + " : " + str(huobi_sell) + ") bitfliyer : (" + str(bitflyer_buy) + " : " + str(bitflyer_sell) + ")" + " 最大価格差 : " + str(max_kakakusa) + "   5000円以上回数" + str(beyond_value) + "\n売り買い変更回数 : " + str(buy_sell_change) + "   売り買い変更回数(価格差5000円以上) : " + str(buy_sell_change_beyond_value)
  plt.title(main_text, color="red")
  plt.xlabel("Time(分)")
  plt.ylabel("ビットコイン[BTC]")
  plt.plot(x, y_huobi_ask, label="Huobi[買]")
  plt.plot(x, y_huobi_bid, label="Huobi[売]")
  # plt.plot(x, y_zaif_ask, label="Zaif[買]")
  # plt.plot(x, y_zaif_bid, label="Zaif[売]")
  # plt.plot(x, y_coincheck_ask, label="coincheck[買]")
  # plt.plot(x, y_coincheck_bid, label="coincheck[売]")
  plt.plot(x, y_bitflyer_ask, label="bitflyer[買]")
  plt.plot(x, y_bitflyer_bid, label="bitflyer[売]")
  # plt.plot(x, y_bit_point_ask, label="bit_point[買]")
  # plt.plot(x, y_bit_point_bid, label="bit_point[売]")
  plt.legend(loc="upper left")
  # plt.tight_layout()
  
def createGraph():
  # アニメーショングラフ適用
  ani = FuncAnimation(plt.gcf(), animate, interval=10000)

  # # グラフ表示
  # plt.tight_layout()
  plt.show()


def get_huobi():
  result = repository.huobi_ticker(repository.huobi_symbol)
  y_huobi_ask.append(float(result["ask"]))
  y_huobi_bid.append(float(result["bid"]))

def get_zaif():
  result = repository.zaif_ticker(repository.zaif_symbol)
  y_zaif_ask.append(float(result['ask']))
  y_zaif_bid.append(float(result['bid']))

def get_coincheck():
  result = repository.coincheck_ticker(repository.coincheck_symbol)
  y_coincheck_ask.append(float(result['ask']))
  y_coincheck_bid.append(float(result['bid']))

def get_bitflyer():
  result = repository.bitflyer_ticker(repository.bitflyer_symbol)
  y_bitflyer_ask.append(float(result['ask']))
  y_bitflyer_bid.append(float(result['bid']))

def get_bit_point():
  result = repository.bit_point_ticker(repository.bit_point_symbol)
  y_bit_point_ask.append(float(result['asks'][0]['price']))
  y_bit_point_bid.append(float(result['bids'][0]['price']))
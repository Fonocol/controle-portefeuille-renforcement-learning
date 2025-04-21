import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

WIN = 20


# SMA
def sma(data, fenetre_size):
  """
  Cette fonction calcule la moyenne mobile simple (SMA)
    d'une série de données sur une fenêtre donnée. La SMA
     lisse les variations en prenant la moyenne des valeurs sur cette période.
  """
  return(data.rolling(window=fenetre_size)).mean()

# EMA
def ema(data : pd.DataFrame, fenetre_size):
  """
  Cette fonction calcule la moyenne mobile exponentielle (EMA)
    d'une série de données sur une fenêtre donnée. L'EMA attribue
    plus de poids aux données récentes pour mieux capter
    les tendances actuelles.
  """
  return( data.ewm(span= fenetre_size, adjust= False).mean())

# RSI
#Surachat  et survente
def rsi(data, fenetre_size):

  """
  La fonction rsi calcule l'indicateur RSI (Relative Strength Index)
    en comparant les gains moyens aux pertes moyennes sur une fenêtre donnée.
    Cet indicateur mesure la force d'une tendance et détecte les zones
    de surachat ou de survente.
  """
  delta = data.diff(1)
  gain_mean = (data.where(delta>0, 0)).rolling(window = fenetre_size).mean()
  perte_mean = (data.where(delta<0, 0)).rolling(window = fenetre_size).mean()
  rs = gain_mean/perte_mean
  rsi = 100-(100/(1+rs))
  return rsi

#macd
#repérer les pionts de changement de tendance

def macd(data, small_window, big_window, signal_window):
  """ 
  Cette  fonction calcule l'indicateur MACD (Moving Average Convergence Divergence)
  et sa ligne de signal en utilisant deux moyennes exponentielles (EMA) 
  de différentes périodes. Elle retourne la valeur du MACD 
  (différence entre EMA rapide et lente) et la ligne de signal (EMA du MACD).
  """
  ema_fast = ema(data, big_window)
  ema_slow = ema(data, small_window)
  macd = ema_fast - ema_slow
  signal = ema(macd, signal_window)
  return macd, signal


#bandes_bollinger
def bandes_bollinger(data, window_size, k=2):
  """ 
    Cette fonction calcule la moyenne mobile (SMA)
    et les bandes supérieure et inférieure en ajoutant/soustrayant
    un multiple de l'écart-type des données. Cela permet de mesurer
    la volatilité et d'identifier des tendances.
  """
  sma_bande = sma(data, window_size)
  std = data.rolling(window = window_size).std()
  bande_inf = sma_bande - k*std
  bande_sup = sma_bande + k*std
  return bande_inf, sma_bande, bande_sup


def laod_data(path: str):
  
  data = pd.read_csv(path)
  # data = data[:1000]
  
  data['ema'] = ema(data=data['Close'],fenetre_size=WIN)
  data['sma'] = sma(data=data['Close'],fenetre_size=WIN)
  data['rsi'] = rsi(data=data['Close'],fenetre_size=WIN)

  data['macd'], data['signal'] = macd(data=data['Close'],small_window=WIN,big_window=WIN+10,signal_window=9)
  data['bande_inf'], _ , data['bande_sup'] = bandes_bollinger(data=data['Close'],window_size=WIN)
  
  data.bfill(inplace= True)
  data.ffill(inplace= True)
  data.to_csv("data/data_model2.csv")
  
  return data
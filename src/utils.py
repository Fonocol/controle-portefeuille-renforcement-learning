import pandas as pd
import matplotlib.pyplot as plt
from IPython import display

# Calcul de la Moyenne Mobile Simple (SMA)
def calculate_sma(data, window):
    return data.rolling(window=window).mean()


# Calcul de la Moyenne Mobile Exponentielle (EMA)
def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()


# Calcul du Relative Strength Index (RSI)
def calculate_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Calcul du MACD (Moving Average Convergence Divergence)
def calculate_macd(data, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(data, window=fast)
    ema_slow = calculate_ema(data, window=slow)
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line


# Calcul des Bandes de Bollinger (Bollinger Bands)
def calculate_bbands(data, window=20, num_std=2):
    sma = calculate_sma(data, window=window)
    rolling_std = data.rolling(window=window).std()
    upper_band = sma + (rolling_std * num_std)
    lower_band = sma - (rolling_std * num_std)
    return upper_band, sma, lower_band


# Charger les données
def load_data(path, col="Close"):
    
    # Charger les données
    data = pd.read_csv(path, index_col=0, parse_dates=True)
    
    data['Close'] = data[col]
    
    # Ajouter les indicateurs techniques
    data['SMA'] = calculate_sma(data['Close'], window=20)
    data['EMA'] = calculate_ema(data['Close'], window=20)
    data['RSI'] = calculate_rsi(data['Close'], window=14)
    data['MACD'], data['MACD_signal'] = calculate_macd(data['Close'], fast=12, slow=26, signal=9)
    data['Upper_Band'], _ , data['Lower_Band'] = calculate_bbands(data['Close'], window=20, num_std=2)
    
    # Remplacer les valeurs manquantes par les voisin
    data.fillna(method='bfill', inplace=True)
    data.fillna(method='ffill', inplace=True)
    
    # Normaliser les colonnes
    #for column in ['SMA', 'EMA', 'RSI', 'MACD', 'MACD_signal', 'Upper_Band', 'Lower_Band']:
       # data[column] = (data[column] - data[column].min()) / (data[column].max() - data[column].min())
        
    #normalizer le priice
    #data['CloseNorm'] = (data['Close'] - data['Close'].min()) / (data['Close'].max() - data['Close'].min())
    
    # Retourner les données
    return data



def plot(portfolio_values,cash, quantites_detenues, actions_aleatoires):

    plt.clf()  

    # Tracer la valeur du portefeuille
    plt.plot(portfolio_values, label="Valeur du portefeuille", color="green")

    # Afficher les informations dynamiques
    current_action = actions_aleatoires
    current_quantity = quantites_detenues
    current_value = portfolio_values[-1]

    # Titre avec informations dynamiques
    action_label = {2: "Ne rien faire", 0: "Acheter", 1: "Vendre"}
    plt.title(
        f"Cash : {cash} | Action : {action_label[current_action]} | Quantité : {current_quantity} | Valeur : {current_value:.2f}"
    )

    # Configuration de l'axe
    plt.xlabel("Étape")
    plt.ylabel("Valeur")
    plt.ylim(ymin=0)
    plt.legend(loc="upper left")
    plt.gcf().canvas.draw()  # Forcer le rendu
    plt.pause(0.1)  # Pause pour animation

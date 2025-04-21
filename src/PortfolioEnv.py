import numpy as np
import pandas as pd
from util import laod_data


class PortfolioEnv:
    """
    Classe principale pour l'environnement de simulation d'un portefeuille financier.
    """

    def __init__(self, data: pd.DataFrame, initial_cash=10000, window_size=5, frais_transaction=10):
        """
        Initialisation de l'environnement du portefeuille.

        Args:
            data (array-like): Les données du marché utilisées pour la simulation.
            initial_cash (float): Montant initial en cash (par défaut 10 000).
            window_size (int): Taille de la fenêtre utilisée pour les observations.
            frais_transaction (float): Frais associés à chaque transaction.
        """
        self.initial_cash = initial_cash
        self.data = data
        self.cash = initial_cash
        self.frais_transaction = frais_transaction
        self.current_step = window_size
        self.quantite_detenue = 0
        self.window_size = window_size
        self.total_value = initial_cash
        self.STEP = 30  # Pas de temps par défaut pour chaque action

    def getCash(self):
        """
        Retourne le montant actuel de cash disponible.

        Returns:
            float: Le montant actuel de cash.
        """
        return self.cash

    def reset(self):
        """
        Réinitialise l'environnement à son état initial.

        """
        self.current_step = self.window_size
        self.cash = self.initial_cash
        self.quantite_detenue = 0
        self.total_value = self.initial_cash

    def _Env_observation(self):
        """
        Retourne l'état de l'environnement sous forme d'observation.

        Returns:
            array-like: La fenêtre des données du marché pour le pas de temps courant.
        """

        price = self.data['Close'].iloc[self.current_step]
        ema = self.data['ema'].iloc[self.current_step]
        sma = self.data['sma'].iloc[self.current_step]
        rsi = self.data['rsi'].iloc[self.current_step]
        macd = self.data['macd'].iloc[self.current_step]
        signal = self.data['signal'].iloc[self.current_step]
        lower_Band = self.data['bande_inf'].iloc[self.current_step]
        upper_Band = self.data['bande_sup'].iloc[self.current_step]

        portfolio_value = self.cash + (self.quantite_detenue * self.data['Close'].iloc[self.current_step])
        cash_ratio = self.cash / portfolio_value if portfolio_value > 0 else 0

        # open = self.data['Open'].iloc[self.current_step]
        # high = self.data['High'].iloc[self.current_step]
        # low = self.data['Low'].iloc[self.current_step]
        statapi = [sma, rsi, macd,upper_Band,lower_Band, cash_ratio]

        #return np.array([price,open,high,low, ema,sma,macd,rsi])
        return np.array([price, ema,sma,macd,rsi]), statapi

    def step1(self, action):
        """
        Exécute une action (achat, vente ou maintien) et met à jour l'état de l'environnement.

        Args:
            action (int): 
                - [0, 0, 1] 1: ne rien faire
                - [1, 0, 0] 2 : Acheter
                - [0, 1, 0] 3: Vendre

        Returns: 
            tuple: (observation, reward, done)
                - observation (array-like): La nouvelle observation après l'action.
                - reward (float): La récompense obtenue après l'action.
                - done (bool): Indique si l'épisode est terminé.
        """

        reward = 0
        self.current_step +=1
        
        #Acheter
        current_price = self.data['Close'].iloc[self.current_step]
        if np.array_equal(action,[1,0,0]):
            if(self.cash >= self.frais_transaction+current_price):
                self.cash -= current_price+self.frais_transaction
                self.quantite_detenue += 1
                
                reward += 0.5
            else:
                reward -= 0.1

        #Vendre
        elif np.array_equal(action,[0,1,0]):
            if( self.quantite_detenue>0):
                self.quantite_detenue -=1
                self.cash += current_price

                reward += 0.5
            
            else:
                reward -= 0.1

        #ne rien faire
        else:
            reward -= 0.01

        done = (self.current_step >= self.data.shape[0]-1)
        if self.current_step % self.STEP ==0:
            done=True
            
        self.total_value = self.cash + self.quantite_detenue*current_price
        return self._Env_observation(), reward, done
    
    def step(self, action):
        if self.current_step >= len(self.data):
            raise IndexError("current_step dépasse la longueur des données.")

        current_price = self.data['Close'].iloc[self.current_step]
        previous_price = self.data['Close'].iloc[self.current_step - 1] if self.current_step > 0 else current_price
        rsi = self.data['rsi'].iloc[self.current_step]
        self.current_step += 1

        reward = 0  

        # Actions : [0, 0, 1] = Ne rien faire, [1, 0, 0] = Acheter, [0, 1, 0] = Vendre
        if np.array_equal(action, [1, 0, 0]):  # Acheter
            if self.cash >= (current_price + self.frais_transaction):
                self.cash -= (current_price + self.frais_transaction)
                self.quantite_detenue += 1
                if rsi < 40:
                    reward += 2
                elif rsi > 60:
                    reward -= 2
            else:
                reward -= 0.1  # Pénalité faible pour tentative d'achat sans fonds

        elif np.array_equal(action, [0, 1, 0]):  # Vendre
            if self.quantite_detenue > 0:
                self.cash += (current_price - self.frais_transaction)
                self.quantite_detenue -= 1

                gain_perte = (current_price - previous_price) / previous_price if previous_price > 0 else 0
                reward += gain_perte # * 100   Récompense proportionnelle
                if rsi > 60:
                    reward += 2
                elif rsi < 40:
                    reward -= 2
            else:
                reward -= 0.1  # Pénalité faible pour tentative de vente sans actions

        elif np.array_equal(action, [0, 0, 1]):  # Ne rien faire
            if rsi < 40 or rsi > 60:
                reward -= 1  # Opportunité manquée

        # Récompense pour la croissance/stabilité du portefeuille
        portfolio_value = self.cash + (self.quantite_detenue * current_price)
        performance = (portfolio_value - self.total_value) / self.total_value if self.total_value > 0 else 0
        reward += performance  # * 100
        self.total_value = portfolio_value

        # Diversification du portefeuille
        portfolio_allocation = self.quantite_detenue * current_price / portfolio_value if portfolio_value > 0 else 0
        reward += (0.5 - abs(portfolio_allocation - 0.5))

        done = self.current_step >= len(self.data) - 1
        if self.current_step % self.STEP == 0:
            done = True

        if done:
            final_performance = (self.total_value - self.initial_cash) / self.initial_cash if self.initial_cash > 0 else 0
            reward += final_performance #* 100


        # print(f"Step: {self.current_step}, Reward: {reward:.2f}, Portfolio Value: {portfolio_value:.2f}")
        return self._Env_observation(), reward, done
    
    def getcurentPrice(self):
        return self.data['Close'].iloc[self.current_step]


if __name__ == '__main__':

    path = 'C:/Users/User/Desktop/s8/projet_tech/projet-controle-portefeuille/data/crypto_data_updated_13_november.csv'
    data = laod_data(path)

    env = PortfolioEnv(data)
    print(env._Env_observation())

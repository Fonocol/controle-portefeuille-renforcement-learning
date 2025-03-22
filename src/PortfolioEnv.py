import numpy as np

class PortfolioEnv:
    """les gars ici c'est la classe principale de notre 
    environnement vous pouvez ajouter des methodes
    """
    def __init__(self, data, initial_cash=10000,window_size=5,frais_transaction=10):
        self.initial_cash = initial_cash
        self.data = data
        self.cash = initial_cash
        self.frais_transaction= frais_transaction
        self.current_step = window_size
        self.quantite_detenue = 0
        self.window_size = window_size
        self.total_value = initial_cash
        self.STEP = 30
        

    def getCash(self):
        return self.cash
    
    def reset(self):
        self.current_step = self.window_size 
        #self.cash = self.initial_cash
        #self.quantite_detenue = 0
        #self.total_value = self.initial_cash
        return self._Env_observation() 
    
    def getcurentPrice(self):
        return self.data['Close'].iloc[self.current_step]
    
    def _Env_observation(self):
        # Séries temporelles de prix et indicateurs
        prices = self.data['Close'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
        
        sma = self.data['SMA'].iloc[self.current_step]
        #ema = self.data['EMA'].iloc[self.current_step]
        rsi = self.data['RSI'].iloc[self.current_step]
        macd = self.data['MACD'].iloc[self.current_step]
        #macd_signal = self.data['MACD_signal'].iloc[self.current_step]
        upper_Band = self.data['Upper_Band'].iloc[self.current_step]
        lower_Band = self.data['Lower_Band'].iloc[self.current_step]
        
        portfolio_value = self.cash + (self.quantite_detenue * self.data['Close'].iloc[self.current_step])
        cash_ratio = self.cash / portfolio_value if portfolio_value > 0 else 0
        
        
        statapi = [sma, rsi, macd,upper_Band,lower_Band, cash_ratio]
        observation = np.concatenate((prices, [sma, rsi, macd,upper_Band,lower_Band, cash_ratio]))
        
        observation = np.array(observation, dtype=np.float32)

        return observation,statapi


    def step(self, action):
        if self.current_step >= len(self.data):
            raise IndexError("current_step dépasse la longueur des données.")

        current_price = self.data['Close'].iloc[self.current_step]
        previous_price = self.data['Close'].iloc[self.current_step - 1] if self.current_step > 0 else current_price
        rsi = self.data['RSI'].iloc[self.current_step]
        self.current_step += 1

        reward = 0  

        # Actions : [0, 0, 1] = Ne rien faire, [1, 0, 0] = Acheter, [0, 1, 0] = Vendre
        if np.array_equal(action, [1, 0, 0]):  # Acheter
            if self.cash >= (current_price + self.frais_transaction):
                self.cash -= (current_price + self.frais_transaction)
                self.quantite_detenue += 1
                if rsi < 30:
                    reward += 2
                elif rsi > 70:
                    reward -= 2
            else:
                reward -= 0.1  # Pénalité faible pour tentative d'achat sans fonds

        elif np.array_equal(action, [0, 1, 0]):  # Vendre
            if self.quantite_detenue > 0:
                self.cash += (current_price - self.frais_transaction)
                self.quantite_detenue -= 1

                gain_perte = (current_price - previous_price) / previous_price if previous_price > 0 else 0
                reward += gain_perte * 100  # Récompense proportionnelle
                if rsi > 70:
                    reward += 2
                elif rsi < 30:
                    reward -= 2
            else:
                reward -= 0.1  # Pénalité faible pour tentative de vente sans actions

        elif np.array_equal(action, [0, 0, 1]):  # Ne rien faire
            if rsi < 30 or rsi > 70:
                reward -= 1  # Opportunité manquée

        # Récompense pour la croissance/stabilité du portefeuille
        portfolio_value = self.cash + (self.quantite_detenue * current_price)
        performance = (portfolio_value - self.total_value) / self.total_value if self.total_value > 0 else 0
        reward += performance * 100
        self.total_value = portfolio_value

        # Diversification du portefeuille
        portfolio_allocation = self.quantite_detenue * current_price / portfolio_value if portfolio_value > 0 else 0
        reward += (0.5 - abs(portfolio_allocation - 0.5))

        done = self.current_step >= len(self.data) - 1
        if self.current_step % self.STEP == 0:
            done = True

        if done:
            final_performance = (self.total_value - self.initial_cash) / self.initial_cash if self.initial_cash > 0 else 0
            reward += final_performance * 100


        #print(f"Step: {self.current_step}, Reward: {reward:.2f}, Portfolio Value: {portfolio_value:.2f}")
        return self._Env_observation(), reward, done


       
    def get_state(self,aleatoir):
        return {
            "Valeur Portefeuille": self.total_value,
            "Quantité Détenue": self.quantite_detenue,
            "Action": ["Ne rien faire", "Acheter", "Vendre"][aleatoir],
            "Prix Actuel":  self.data['Close'].iloc[self.current_step],
        }
        
 
 
 
 
from utils import load_data 
        
if __name__ == '__main__':
  data = load_data() 
  portfolioEnv = PortfolioEnv(data, initial_cash=80559)
  
  state = portfolioEnv._Env_observation()
  print(state)
  print(state.shape)
  
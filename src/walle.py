def step(self, action):
        current_price = self.data['Close'].iloc[self.current_step]
        self.current_step += 1
        
        # Actions : [0, 0, 1] = Ne rien faire, [1, 0, 0] = Acheter, [0, 1, 0] = Vendre
        previous_price = self.data['Close'].iloc[self.current_step - 1]  # Le prix précédent pour comparaison
        reward = 0  # Initialisation de la récompense
        rsi = self.data['RSI'].iloc[self.current_step]
        
        if np.array_equal(action, [1, 0, 0]) and self.cash >= current_price + self.frais_transaction:  # Acheter
            self.cash -= (current_price + self.frais_transaction)
            self.quantite_detenue += 1
            if rsi < 30:  # RSI faible, acheter
                reward += 0.05
            
        elif np.array_equal(action, [0, 1, 0]) and self.quantite_detenue > 0:  # Vendre
            self.cash += (current_price - self.frais_transaction)
            self.quantite_detenue -= 1
            if current_price > previous_price:  # Vendre après un gain
                reward += 0.01
            elif current_price < previous_price:  # Vendre après une perte
                reward -= 0.01
            if rsi > 70:  # RSI élevé, vendre
                reward += 0.05
        
        # Calcul de la valeur totale du portefeuille
        portfolio_value = self.cash + (self.quantite_detenue * current_price)
        reward += (portfolio_value - self.total_value) / self.total_value  # Gain en pourcentage
        
        self.total_value = portfolio_value
        
        # Fin
        done = self.current_step >= len(self.data) - 1
        if self.current_step % self.STEP == 0:
            done = True
        
        return self._Env_observation(), reward, done
    
    
    
    
    
    
    sma = self.data['SMA'].iloc[self.current_step]
    ema = self.data['EMA'].iloc[self.current_step]
    rsi = self.data['RSI'].iloc[self.current_step]
    macd = self.data['MACD'].iloc[self.current_step]
    macd_signal = self.data['MACD_signal'].iloc[self.current_step]
    upper_Band = self.data['Upper_Band'].iloc[self.current_step]
    lower_Band = self.data['Lower_Band'].iloc[self.current_step]
    
    observation = np.concatenate((prices, [sma,ema, rsi, macd,macd_signal,upper_Band,lower_Band, cash_ratio]))
    
    
    
    
    def step(self, action):
        current_price = self.data['Close'].iloc[self.current_step]
        previous_price = self.data['Close'].iloc[self.current_step - 1] if self.current_step > 0 else current_price
        rsi = self.data['RSI'].iloc[self.current_step]
        self.current_step += 1

        # Initialisation des récompenses et pénalités
        reward = 0  

        # Actions : [0, 0, 1] = Ne rien faire, [1, 0, 0] = Acheter, [0, 1, 0] = Vendre
        if np.array_equal(action, [1, 0, 0]):  # Acheter
            if self.cash >= (current_price + self.frais_transaction):  # Vérification des fonds
                self.cash -= (current_price + self.frais_transaction)
                self.quantite_detenue += 1
                if rsi < 20:  
                    reward += 0.4  # Encouragement fort
                elif rsi < 30:
                    reward += 0.1
            else:
                reward -= 0.3  # Pénalité pour tentative d'achat sans fonds suffisants

        elif np.array_equal(action, [0, 1, 0]):  # Vendre
            if self.quantite_detenue > 0:  # Vérification des quantités détenues
                self.cash += (current_price - self.frais_transaction)
                self.quantite_detenue -= 1

                # Récompense proportionnelle aux gains/pertes
                gain_perte = (current_price - previous_price) / previous_price
                reward += gain_perte  

                if rsi > 80:
                    reward += 0.5  # Encouragement fort
                elif rsi > 70:
                    reward += 0.2
            else:
                reward -= 0.3  # Pénalité pour tentative de vente sans actions

        elif np.array_equal(action, [0, 0, 1]):  # Ne rien faire
            if 30 <= rsi <= 70:  
                reward += 0.1  # Récompense neutre si inaction justifiée
            else:
                reward -= 0.6  # Pénalité pour opportunité manquée

        # Calcul de la valeur totale du portefeuille
        portfolio_value = self.cash + (self.quantite_detenue * current_price)
        stability_factor = (portfolio_value - self.total_value) / self.total_value if self.total_value > 0 else 0
        reward += stability_factor * 0.5  # Récompense pour stabilité/croissance

        # Mise à jour de la valeur totale
        self.total_value = portfolio_value
        print("reward = " , reward)

        # Vérification de la fin de l'épisode
        done = self.current_step >= len(self.data) - 1
        if self.current_step % self.STEP == 0:
            done = True

        # Récompense finale si l'épisode se termine
        if done:
            final_reward = (self.total_value - self.initial_cash) / self.initial_cash if self.initial_cash > 0 else 0
            reward += final_reward

        return self._Env_observation(), reward, done

    
    
    
sma = self.data['SMA'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
ema = self.data['EMA'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
rsi = self.data['RSI'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
macd = self.data['MACD'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
macd_signal = self.data['MACD_signal'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
upper_Band = self.data['Upper_Band'].iloc[max(0, self.current_step - self.window_size):self.current_step].values
lower_Band = self.data['Lower_Band'].iloc[max(0, self.current_step - self.window_size):self.current_step].values








def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size1)  
        self.linear2 = nn.Linear(hidden_size1, hidden_size2)  
        self.linear3 = nn.Linear(hidden_size2, output_size)  

    def forward(self, x):
        x = F.relu(self.linear1(x))  
        x = F.relu(self.linear2(x))  
        x = self.linear3(x)  
        return x
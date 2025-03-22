import numpy as np
from utils import  plot



# Agent aléatoire
def AgentAleatoire(envPortfolio):
    
    observation = envPortfolio.reset()  # Réinitialiser l'environnement
    done = False
    portfolio_values = []

    while not done:
        action = [0,0,0]
        aleatoir = np.random.choice([0, 1, 2])
        action[aleatoir] = 1
        
      
        observation, reward, done, info = envPortfolio.step(action)
        portfolio_values.append(envPortfolio.total_value)  
        
        
        plot(portfolio_values,envPortfolio.quantite_detenue,aleatoir)

    return portfolio_values
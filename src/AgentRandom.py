import numpy as np
from PortfolioEnv import PortfolioEnv
import util as ut



def AgentRandom(portfolioEnv: PortfolioEnv):

    portfolioEnv.reset()
    done = False

    portfolio_value = []

    while not done:
        action = [0,0,0]
        random = np.random.choice([0,1,2])
        action[random] = 1
        observation, reward, done = portfolioEnv.step(action)
        #print(action)
        portfolio_value.append(portfolioEnv.total_value)


    #print("quantite detenue = ", portfolioEnv.quantite_detenue)
    #print("cash = ", portfolioEnv.cash)

    return portfolio_value

 # creation d'un agent baser sur le RSI

def rsiagent(portfolioEnv: PortfolioEnv):

    portfolioEnv.reset()
    done = False
    portfolio_value = []
    while not done:
        action= [0, 0, 0]
        if portfolioEnv.data['rsi'].iloc[portfolioEnv.current_step]>65 :
            action [1]=1
        elif portfolioEnv.data['rsi'].iloc[portfolioEnv.current_step] <45 :
            action [0] =1
        else:
            action[2]= 1
        _, _, done = portfolioEnv.step(action)
        portfolio_value.append(portfolioEnv.total_value)
    return portfolio_value
    
     



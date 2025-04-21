from util import laod_data
import pandas as pd
from AgentRandom import AgentRandom, rsiagent
from PortfolioEnv import PortfolioEnv
import matplotlib.pyplot as plt



if __name__ == '__main__':

    path = 'C:/Users/User/Desktop/s8/projet_tech/projet-controle-portefeuille/data/data_model2.csv'
    data = pd.read_csv(path)

    for i in range(10 ):
        print( i)
        env = PortfolioEnv(data)
        agent = AgentRandom(env)
        agentRSI= rsiagent(env)
        
        print ( "----------- plot en cours -----------------------")
        plt.plot(agent, label= "agent random")
        plt.plot(agentRSI, label= " agent RSI")
        plt.xlabel('temps')
        plt.ylabel('valeur total')
        plt.title('evolution of total value')
        plt.legend()
        plt.savefig( f"C:/Users/User/Desktop/s8/projet_tech/projet-controle-portefeuille/results/image_a_rsi{i}.png")
        plt.show()
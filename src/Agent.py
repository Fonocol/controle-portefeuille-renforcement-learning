from collections import deque
import random

import torch
from PortfolioEnv import PortfolioEnv
from model import Linear_QNet, QTrainer
from util import laod_data
import pandas as pd
import matplotlib.pyplot as plt
from util import plot



MEMOIRE_LEN = 100_000
BATCH = 10_000
LR= 0.001

class Agent:
    """
    Agent
    """
    def __init__(self):
        self.nbr_game = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MEMOIRE_LEN)
        self.model = Linear_QNet(5, 256, 3)  # entree => couche intermediere => sorntie
        # TODO   Double DQN (réduction du biais)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)

    def get_state(self,portfolioEnv: PortfolioEnv):
        return portfolioEnv._Env_observation()

    def souvenir(self,state, action, reward, next_state,done):
        self.memory.append((state, action, reward, next_state,done))
        

    def train_long_memory(self):
        if len(self.memory) > BATCH:
            mini_memory = random.sample(self.memory,BATCH) #souvenir liste de tuple
        else:
            mini_memory = self.memory
 
        states,actions,rewards,next_stats,dones = zip(*mini_memory)
        self.trainer.train_step(states,actions,rewards,next_stats,dones)
       

    def train_short_mamory(self,state, action, reward,next_state,done):
        self.trainer.train_step(state, action, reward,next_state,done)

    def get_action(self,state):
        self.epsilon = 80 - self.nbr_game
        final_decision = [0,0,0]
        decision = 0
       
        if random.randint(0,120) < self.epsilon:
            decision = random.randint(0,2)
            final_decision[decision] = 1
        else:
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            decision = torch.argmax(prediction).item()  #retourne l'index de la valeur max exemple [3,6,8] => 2
            #print("pred = " ,prediction)
            final_decision[decision] = 1
        return final_decision, decision



def train():
    """
    boucle d'entrainement principale
    """
    path = 'C:/Users/User/Desktop/s8/projet_tech/projet-controle-portefeuille/data/data_model2.csv'
    data = pd.read_csv(path)
    Portfolio_value= []
    score= 0
    record= 0
    portfolioEnv = PortfolioEnv(data)
    agent= Agent()
    i = 0
    rewards=[]
    while(i<= (len( data)- 2)):

        i+=1
        old_state= agent.get_state(portfolioEnv)
        final_decision, decision= agent.get_action(old_state)

        _,reward, done= portfolioEnv.step(final_decision)
        rewards.append(reward)
        Portfolio_value.append(portfolioEnv.total_value)

        new_state= agent.get_state(portfolioEnv)

        agent.train_short_mamory(old_state, final_decision,reward,new_state,done)
        if portfolioEnv.current_step >= len(portfolioEnv.data) -1:
            portfolioEnv.reset()

        agent.souvenir(old_state,final_decision,reward,new_state,done)
        score= portfolioEnv.total_value

        if done== True:
            agent.nbr_game+=1
            agent.train_long_memory()
            if score >= record:
                record= score
                agent.model.save()
            # print ( 'game', agent.nbr_game, 'score ', score, 'record', record)
        # plot(Portfolio_value,portfolioEnv.cash,portfolioEnv.quantite_detenue,decision)
    plt.plot(rewards)
    plt.xlabel('step')
    plt.ylabel('reward')
    plt.show()

if __name__ == '__main__':
    train()


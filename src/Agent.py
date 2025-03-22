import numpy as np
from utils import  plot
import random
from collections import deque
import torch
from model import Linear_QNet, QTrainer
from PortfolioEnv import PortfolioEnv
from utils import load_data

#constantes
MAX_MEMORY = 100_000
BATCH_SIZE = 10000
LR = 0.001


class Agent:
    def __init__(self):
        self.nbr_game = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)  # entree => couche intermediere => sorntie
        # TODO   Double DQN (réduction du biais)
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)
        
        #TODO : cree le model de reseaux de neuronne apes
        
    def get_state(self,portfolioEnv:PortfolioEnv):
        return portfolioEnv._Env_observation()
    
    def souvenir(self,state,action,reward,next_stat,done):
        self.memory.append((state,action,reward,next_stat,done))
        
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_memory = random.sample(self.memory,BATCH_SIZE) #souvenir liste de tuple
        else:
            mini_memory = self.memory

        states,actions,rewards,next_stats,dones = zip(*mini_memory)
        self.trainer.train_step(states,actions,rewards,next_stats,dones)
        
    def train_short_memory(self,state,action,reward,next_stat,done):
        self.trainer.train_step(state,action,reward,next_stat,done)
        
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
    

# def train():
#     record = 0
#     score = 0
#     portfolio_values = []
#     data = load_data(path="C:/Users/etudiant/Documents/MesEtudes/projet-controle-portefeuille/data/ble_price.csv")
#     print(data)
#     portfolioEnv = PortfolioEnv(data, initial_cash=500,frais_transaction=1.50)
#     agent = Agent()
    
        
#     while True:
#         old_state = agent.get_state(portfolioEnv)
        
#         final_decision ,decision= agent.get_action(old_state)
        
#         _, reward, done = portfolioEnv.step(final_decision)
#         portfolio_values.append(portfolioEnv.total_value) 
#         new_state = agent.get_state(portfolioEnv)
        
#         agent.train_short_memory(old_state,final_decision,reward,new_state,done)
        
#         #remenber
#         # state,action,reward,next_stat,done
#         if portfolioEnv.current_step >= len(portfolioEnv.data) - 1:
#             portfolioEnv.reset()
            
#         agent.souvenir(old_state,final_decision,reward,new_state,done)
#         score = portfolioEnv.total_value
        
            
        
#         if done== True:
#             agent.nbr_game += 4
#             print(agent.epsilon)
#             agent.train_long_memory()
            
#             if score >= record:
#                 record = score
#                 agent.model.save()
                
#             print('Game',agent.nbr_game,'Score',score,'Record',record)
            
#         plot(portfolio_values,portfolioEnv.cash,portfolioEnv.quantite_detenue,decision)


        
        
# if __name__ == '__main__':
#   train() 
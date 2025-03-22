from flask import Flask
from flask_socketio import SocketIO
import time
import threading
from Agent import Agent
from PortfolioEnv import PortfolioEnv
from utils import load_data

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  


    
    
def train():
    record = 0
    score = 0
    portfolio_values = []
    data = load_data(path="C:/Users/etudiant/Documents/MesEtudes/projet-controle-portefeuille/data/ble_price.csv")
    portfolioEnv = PortfolioEnv(data, initial_cash=5000,frais_transaction=1.50)
    agent = Agent()
    
        
    while True:
        time.sleep(2)
        old_state,statapi = agent.get_state(portfolioEnv)
        currentprice = portfolioEnv.getcurentPrice()
        
        final_decision ,decision= agent.get_action(old_state)
        
        _, reward, done = portfolioEnv.step(final_decision)
        portfolio_values.append(portfolioEnv.total_value) 
        new_state ,_ = agent.get_state(portfolioEnv)
        
        agent.train_short_memory(old_state,final_decision,reward,new_state,done)
        
        #remenber
        # state,action,reward,next_stat,done
        if portfolioEnv.current_step >= len(portfolioEnv.data) - 1:
            portfolioEnv.reset()
            
        agent.souvenir(old_state,final_decision,reward,new_state,done)
        score = portfolioEnv.total_value
        
            
        
        if done== True:
            agent.nbr_game += 4
            print(agent.epsilon)
            agent.train_long_memory()
            
            if score >= record:
                record = score
                agent.model.save()
                
            print('Game',agent.nbr_game,'Score',score,'Record',record)
        print(portfolioEnv.cash,portfolioEnv.quantite_detenue)
        data = {
            "decision": ["Acheter", "Vendre", "Rien faire"][decision],
            "total_value": portfolioEnv.total_value,
            "cash":portfolioEnv.cash,
            "quantite_detenue": portfolioEnv.quantite_detenue,
            "timestamp": time.strftime("%H:%M:%S"),
            "state":statapi,
            "price":currentprice
        }
        socketio.emit("update", data) 
            

        
        

threading.Thread(target=train, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

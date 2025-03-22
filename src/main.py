from PortfolioEnv import PortfolioEnv  
from utils import load_data
from AgentAleatoire import AgentAleatoire



# Main
if __name__ == "__main__":
    data = load_data()  
    envPortfolio = PortfolioEnv(data, initial_cash=80559)  
    portfolio_values = AgentAleatoire(envPortfolio)  


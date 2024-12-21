import numpy as np

class PortfolioEnv:
    """les gars ici c'est la classe principale de notre 
    environnement vous pouvez ajouter des methodes
    """
    def __init__(self, data, initial_cash=10000):
        self.data = data
        self.cash = initial_cash

    def getCash(self):
        return self.cash
    
    
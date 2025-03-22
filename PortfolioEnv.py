import numpy as np



class PortfolioEnv:
    """
    Classe principale pour l'environnement de simulation d'un portefeuille financier.
    """

    def __init__(self, data, initial_cash=10000, window_size=5, frais_transaction=10):
        """
        Initialisation de l'environnement du portefeuille.

        Args:
            data (array-like): Les données du marché utilisées pour la simulation.
            initial_cash (float): Montant initial en cash (par défaut 10 000).
            window_size (int): Taille de la fenêtre utilisée pour les observations.
            frais_transaction (float): Frais associés à chaque transaction.
        """
        self.initial_cash = initial_cash
        self.data = data
        self.cash = initial_cash
        self.frais_transaction = frais_transaction
        self.current_step = window_size
        self.quantite_detenue = 0
        self.window_size = window_size
        self.total_value = initial_cash
        self.STEP = 30  # Pas de temps par défaut pour chaque action

    def getCash(self):
        """
        Retourne le montant actuel de cash disponible.

        Returns:
            float: Le montant actuel de cash.
        """
        return self.cash

    def reset(self):
        """
        Réinitialise l'environnement à son état initial.

        """
        pass

    def _Env_observation(self):
        """
        Retourne l'état de l'environnement sous forme d'observation.

        Returns:
            array-like: La fenêtre des données du marché pour le pas de temps courant.
        """
        pass

    def step(self, action):
        """
        Exécute une action (achat, vente ou maintien) et met à jour l'état de l'environnement.

        Args:
            action (int): 
                - [0, 0, 1]: ne rien faire
                - [1, 0, 0] : Acheter
                - [0, 1, 0] : Vendre

        Returns: 
            tuple: (observation, reward, done)
                - observation (array-like): La nouvelle observation après l'action.
                - reward (float): La récompense obtenue après l'action.
                - done (bool): Indique si l'épisode est terminé.
        """
        
        
        
        return observation, reward, done
    
    def getcurentPrice(self):
        return self.data['Close'].iloc[self.current_step]

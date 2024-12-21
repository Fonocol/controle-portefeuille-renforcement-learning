# Contrôle de Portefeuille avec Apprentissage par Renforcement

## Description
Ce projet vise à développer un agent intelligent capable de gérer un portefeuille d'actifs financiers en utilisant des techniques d'apprentissage par renforcement. L'objectif est d'optimiser la rentabilité du portefeuille tout en minimisant les risques, grâce à un entraînement basé sur des données financières historiques.

---

## Fonctionnalités
- Simulation d'un **environnement de marché financier personnalisé**.
- Entraînement d'un agent intelligent via des algorithmes d'**apprentissage par renforcement profond** (Deep Reinforcement Learning) comme **PPO** (Proximal Policy Optimization) ou **DQN** (Deep Q-Network).
- Visualisation des performances du portefeuille :
  - **ROI (Return on Investment)**
  - **Volatilité**
  - **Répartition des actifs**

---

## Technologies Utilisées
- **Langage :** Python  
- **Frameworks :** Stable-Baselines3, TensorFlow, PyTorch  
- **Données :** Yahoo Finance, Kaggle  
- **Outils :** Jupyter Notebook, VSCode  

---

## Organisation du Projet
Le projet est structuré comme suit :
```
projet-controle-portefeuille/
├── data/                 # Données financières
├── notebooks/            # Notebooks Jupyter pour l'analyse
├── src/                  # Code source principal
│   ├── environment/      # Scripts de simulation de marché
│   ├── agents/           # Implémentation des agents RL
│   ├── utils/            # Fonctions utilitaires
├── results/              # Visualisations et métriques de performance
├── README.md             # Documentation du projet
├── LICENSE               # License
```

---

## Installation

### Prérequis
- Python 3.9+
- Conda ou un autre gestionnaire d'environnements virtuels

### Étapes
1. **Clonez ce dépôt :**
   ```bash
    git clone https://github.com/Fonocol/-projet-controle-portefeuille-.git
    cd -projet-controle-portefeuille-
   ```

2. **Créez et activez l'environnement virtuel :**
   ```bash
    conda create -n portefeuille-rl python=3.9 -y
    conda activate portefeuille-rl
   ```

3. **Installez les dépendances :**
   ```bash
    pip install -r requirements.txt
   ```

4. **Lancez les notebooks ou le script principal :**
   ```bash
    jupyter notebook
    # ou
    python src/...
   ```

---

## Contribution
Les contributions sont les bienvenues ! Si vous souhaitez proposer des améliorations ou signaler des problèmes, n'hésitez pas à :
- **Ouvrir une issue** dans le dépôt GitHub.
- **Soumettre une pull request** avec vos modifications.

---

## Licence
Ce projet est sous licence **MIT**. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## Équipe
**Équipe Portefeuille RL**  
- **Membre 1 :** Responsable de l'architecture du projet et des algorithmes RL.  
- **Membre 2 :** Analyse des données et création de l'environnement.  
- **Membre 3 :** Visualisation des résultats et intégration.


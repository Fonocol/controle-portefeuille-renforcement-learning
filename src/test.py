import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import time
import threading

# Simulation d'environnement simplifié
from PortfolioEnv import PortfolioEnv  
from utils import load_data

# Environnement
marche = load_data()
env = PortfolioEnv(marche, initial_cash=80559)

# Données initiales pour Dash
data = pd.DataFrame(columns=["Étape", "Valeur Portefeuille", "Quantité Détenue", "Action", "Prix Actuel"])
current_step = 0

# Agent aléatoire
def AgentAleatoire(envPortfolio):
    global current_step, data
    observation = envPortfolio.reset()  # Réinitialiser l'environnement
    done = False

    while not done:
        action = [0, 0, 0]
        aleatoir = np.random.choice([0, 1, 2])
        action[aleatoir] = 1
        
        state = env.get_state(aleatoir)
        state["Étape"] = envPortfolio.current_step
      
        observation, reward, done, info = envPortfolio.step(action)
        
        # Ajouter les données
        new_row = pd.DataFrame([state])
        if not new_row.empty and not new_row.isna().all(axis=None):
            data = pd.concat([data, new_row], ignore_index=True)
        
        current_step = envPortfolio.current_step
        time.sleep(0.5)

# Lancer la simulation dans un thread séparé
threading.Thread(target=AgentAleatoire, args=(env,), daemon=True).start()

# Application Dash
app = dash.Dash(__name__)

# CSS personnalisé pour le style
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Portfolio RL Dashboard</title>
        <style>
            body {
                background-color: #1e1e1e;
                color: #f1f1f1;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            h1 {
                color: #ff8800;
                text-align: center;
                margin-top: 20px;
            }
            .dash-container {
                text-align: center;
                margin: 20px auto;
                width: 90%;
            }
            .dash-graph {
                margin: 0 auto;
                width: 80%;
            }
            .info-box {
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
                text-align: left;
                color: #f1f1f1;
                margin: 10px 0;
                width: 300px;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
            }
            .info-box p {
                margin: 5px 0;
                font-size: 16px;
            }
            .info-title {
                font-size: 18px;
                font-weight: bold;
                color: #ff8800;
            }
        </style>
    </head>
    <body>
        <div id="react-entry-point">
            <div class="dash-container">
                <h1>Contrôle du Portefeuille avec RL</h1>
                {%app_entry%}
            </div>
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout de l'application
app.layout = html.Div([
    dcc.Graph(id="portfolio-graph", className="dash-graph"),
    html.Div(id="current-info", className="info-box"),
    dcc.Interval(id="interval-update", interval=1000, n_intervals=0)  # Mise à jour toutes les secondes
])

# Callback pour mettre à jour le graphique et les infos
@app.callback(
    [Output("portfolio-graph", "figure"),
     Output("current-info", "children")],
    [Input("interval-update", "n_intervals")]
)
def update_graph(n):
    if data.empty:
        return {}, ""

    # Dernières données
    last_row = data.iloc[-1]

    # Graphique
    figure = {
        "data": [
            {"x": data["Étape"], "y": data["Valeur Portefeuille"], "type": "line", "name": "Valeur"},
            {"x": data["Étape"], "y": data["Quantité Détenue"], "type": "line", "name": "Quantité"},
        ],
        "layout": {
            "title": "Évolution du Portefeuille",
            "xaxis": {"title": "Étape", "color": "#f1f1f1"},
            "yaxis": {"title": "Valeur", "color": "#f1f1f1"},
            "plot_bgcolor": "#1e1e1e",
            "paper_bgcolor": "#1e1e1e",
            "font": {"color": "#f1f1f1"},
        },
    }
    # Graphique
   

    # Infos actuelles
    info = html.Div([
        html.Div([
            html.P("Action :", className="info-title"),
            html.P(f"{last_row['Action']}"),
        ]),
        html.Div([
            html.P("Quantité Détenue :", className="info-title"),
            html.P(f"{last_row['Quantité Détenue']}"),
        ]),
        html.Div([
            html.P("Valeur Portefeuille :", className="info-title"),
            html.P(f"{last_row['Valeur Portefeuille']:.2f}"),
        ]),
        html.Div([
            html.P("Prix Actuel :", className="info-title"),
            html.P(f"{last_row['Prix Actuel']:.2f}"),
        ])
    ])

    return figure, info

# Lancer l'application
if __name__ == "__main__":
    port = 5000  
    print(f"Le serveur Dash est lancé sur : http://127.0.0.1:{port}")
    app.run_server(debug=True, port=port)

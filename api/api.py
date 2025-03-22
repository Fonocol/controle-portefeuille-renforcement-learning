from flask import Flask
from flask_socketio import SocketIO
import time
import random
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  

value = 1000  
prixVente = 50  

def send_data():
    global value  
    while True:
        time.sleep(2)
        decision = random.choice(["Acheter", "Vendre", "Rien faire"])

        if decision == "Acheter":
            value -= prixVente
        elif decision == "Vendre":
            value += prixVente  

        data = {
            "decision": decision,
            "price": value,
            "timestamp": time.strftime("%H:%M:%S")
        }
        socketio.emit("update", data)  

threading.Thread(target=send_data, daemon=True).start()

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

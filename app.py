from flask import Flask, request, jsonify, render_template
from agents.price_agent import PriceSuggestorAgent
from agents.moderation_agent import ChatModerationAgent
import pandas as pd
import os

app = Flask(__name__)

# Load dataset
DATA_PATH = "data/dataset.csv"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

# Initialize agents
price_agent = PriceSuggestorAgent(df)
moderation_agent = ChatModerationAgent()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/negotiate", methods=["GET", "POST"])
def negotiate():
    if request.method == "GET":
        data = request.args.to_dict()
    else:
        data = request.json
    result = price_agent.suggest(data)
    return jsonify(result)

@app.route("/moderate", methods=["GET", "POST"])
def moderate():
    if request.method == "GET":
        msg = request.args.get("message", "")
    else:
        msg = request.json.get("message", "")
    result = moderation_agent.moderate(msg)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

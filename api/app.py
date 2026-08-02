from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('outputs/sector_strategy_rankings.csv')

@app.route('/')
def home():
    return jsonify({
        "message": "Climate Emission Strategy Ranking API",
        "usage": "GET /strategies?sector=<sector_name>"
    })

@app.route('/strategies')
def strategies():
    sector = request.args.get('sector')

    if not sector:
        return jsonify({"error": "Please provide a sector parameter"}), 400

    result = df[df['original_inventory_sector'] == sector]

    if result.empty:
        return jsonify({"error": f"No data found for sector '{sector}'"}), 404

    result = result.sort_values('rank_by_priority')
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
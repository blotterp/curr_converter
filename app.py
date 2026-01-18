from flask import Flask, jsonify, request
from database import db
from models import CurrencyRate
from services import update_rates
from flask import render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/update-rates', methods=['POST'])
def update_rates_endpoint():
    timestamp = update_rates()
    return jsonify({
        "status": "ok",
        "updated_at": timestamp.isoformat()
    })

@app.route('/api/last-update', methods=['GET'])
def last_update():
    rate = CurrencyRate.query.first()
    if not rate:
        return jsonify({"updated_at": None})

    return jsonify({
        "updated_at": rate.updated_at.isoformat()
    })

@app.route('/api/convert', methods=['POST'])
def convert_currency():
    data = request.json

    from_currency = data.get("from").upper().strip()
    to_currency = data.get("to").upper().strip()
    amount = float(data.get("amount"))
    
    if from_currency == "EUR":
        rate_obj = CurrencyRate.query.filter_by(
        target_currency=to_currency).first()

        if not rate_obj:
            return jsonify({"error": "Currency not found"}), 400

        rate = rate_obj.rate
        result = amount * rate
    else:
        from_rate_obj = CurrencyRate.query.filter_by(
            target_currency=from_currency
        ).first()
        if not from_rate_obj: 
            return jsonify({"error": "Currency not found"}), 400
        from_rate = from_rate_obj.rate
        to_rate_obj = CurrencyRate.query.filter_by(
            target_currency=to_currency
        ).first()

        if not to_rate_obj:
            return jsonify({"error": "Currency not found"}), 400
        to_rate = to_rate_obj.rate
        result = amount / from_rate * to_rate

    return jsonify({
        "result": round(result, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
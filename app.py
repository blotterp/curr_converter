from flask import Flask, jsonify, request
from database import db
from models import CurrencyRate
from services import update_rates
from flask import render_template
from services import convert_currency, CurrencyNotFoundError

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
def convert_currency_endpoint():
    data = request.json

    try:
        amount = float(data.get("amount"))
        from_currency = data.get("from").upper().strip()
        to_currency = data.get("to").upper().strip()

        result = convert_currency(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency
        )

    except CurrencyNotFoundError as e:
        return jsonify({"error": f"Currency not found: {e}"}), 400
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    return jsonify({"result": round(result, 2)})

@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    currencies = (
        CurrencyRate.query
        .with_entities(CurrencyRate.target_currency)
        .distinct()
        .all()
    )

    return jsonify({
        "currencies": [c[0] for c in currencies]
    })

if __name__ == '__main__':
    app.run(debug=True)
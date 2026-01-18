import os
import requests
from datetime import datetime
from database import db
from models import CurrencyRate

API_KEY = os.getenv("EXCHANGE_API_KEY")

if not API_KEY:
    raise RuntimeError("EXCHANGE_API_KEY is not set")

API_URL = "http://api.exchangeratesapi.io/v1/latest"

def update_rates(base_currency="EUR"):
    response = requests.get(API_URL, params={"access_key": API_KEY,
                                             "base": base_currency})
    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)
    data = response.json()
    print("PARSED JSON:", data)
    rates = data.get("rates", {})
    print("RATES:", rates)
    timestamp = datetime.utcnow()
    if not rates:
        raise Exception(f"Empty rates received: {data}")
    CurrencyRate.query.delete()

    for currency, rate in rates.items():
        db.session.add(
            CurrencyRate(
                base_currency=base_currency,
                target_currency=currency,
                rate=rate,
                updated_at=timestamp
            )
        )

    db.session.commit()
    return timestamp
import os
import requests
from datetime import datetime
from database import db
from models import CurrencyRate

API_KEY = os.getenv("EXCHANGE_API_KEY")

if not API_KEY:
    raise RuntimeError("EXCHANGE_API_KEY is not set")

API_URL = "http://api.exchangeratesapi.io/v1/latest"

class CurrencyNotFoundError(Exception):
    pass

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

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return amount

    from_rate_obj = CurrencyRate.query.filter_by(
        target_currency=from_currency
    ).first()

    if not from_rate_obj:
        raise CurrencyNotFoundError(from_currency)

    to_rate_obj = CurrencyRate.query.filter_by(
        target_currency=to_currency
    ).first()

    if not to_rate_obj:
        raise CurrencyNotFoundError(to_currency)

    return amount / from_rate_obj.rate * to_rate_obj.rate
function convert() {
    fetch('/api/convert', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            amount: document.getElementById('amount').value,
            from: document.getElementById('from').value,
            to: document.getElementById('to').value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').innerText =
            "Result: " + data.result;
    });
    
}

function updateRates() {
    fetch('/api/update-rates', {
        method: 'POST'
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('update-status').innerText =
            'Курсы обновлены: ' + data.updated_at;
    })
    .catch(() => {
        document.getElementById('update-status').innerText =
            'Ошибка обновления курсов';
    });
}

document.addEventListener('DOMContentLoaded', loadCurrencies);

function loadCurrencies() {
    fetch('/api/currencies')
        .then(res => res.json())
        .then(data => {
            const from = document.getElementById('from');
            const to = document.getElementById('to');

            data.currencies.forEach(currency => {
                from.add(new Option(currency, currency));
                to.add(new Option(currency, currency));
            });
        });
}
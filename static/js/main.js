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
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Mock data to simulate backend dynamic statistics
    stats = {
        "users": 1245,
        "revenue": "$34,200",
        "conversion": "4.2%"
    }
    return render_template('dashboard.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)

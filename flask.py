from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({
        "temperature": 28.5,
        "humidity": 60,
        "status": "Normal"
    })

if __name__ == '__main__':
    app.run(port=5000)

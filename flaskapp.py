import os
from flask import Flask

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT', '5000')

@app.route('/', methods=['GET'])
def home():
    return 'Hello Predix!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',
	port=port)
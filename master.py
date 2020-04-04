from flask import Flask, jsonify, request, render_template_string, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/upload',methods=['POST'])
@cross_origin(supports_credentials=True)
def data():
    file = request.files['resume']
    print("1")
    return file

if __name__ == '__main__':
    app.run(debug=True)
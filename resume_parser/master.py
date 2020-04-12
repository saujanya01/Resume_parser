from flask import Flask, jsonify, request, render_template_string, render_template
from flask_cors import CORS, cross_origin
import os
from werkzeug.utils import secure_filename
import process_pdf
import process_docx
import csv

ALLOWED_EXTENSIONS = {'pdf','docx'}

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/file')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    files = request.files.get('file')
    print(type(files))
    filename = secure_filename(files.filename)
    print(filename)
    files.save(os.path.join(app.config['UPLOAD_FOLDER']))
    os.rename('./static/file',"./static/"+filename)
    if (filename.split('.')[1]=='pdf'):
      data = process_pdf.to_text(filename)
    # print(data)
    else:
      data=process_docx.to_text(filename)
    print(data)
    l = []
    for i in list(data.keys()):
        for j,k in data[i].items():
            temp = [j,k]
            l.append(tuple(temp))
    csvfile = open("static/file.csv",'w',newline='')
    obj = csv.writer(csvfile)
    for i in l:
        obj.writerow(i)
    csvfile.close()
    return jsonify({"data":"done"})

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)
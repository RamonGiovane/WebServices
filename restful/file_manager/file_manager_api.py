import json
import os
from flask import Flask
from flask import request
from dicttoxml import dicttoxml

app = Flask(__name__)

@app.route('/<path:dir>/json', methods=['GET'])
def get_json(dir):
    dic = {}
    dic['files'] = os.listdir(dir)
    return json.dumps(dic)

@app.route('/<path:dir>/xml', methods=['GET'])
def get_xml(dir):
    return dicttoxml(os.listdir(dir), custom_root="files", attr_type=False)    

@app.route("/<path:dir>", methods=['DELETE'])
def delete_dir(dir):
    try:
        os.rmdir(dir)
        return True   
    
    except Exception:
        return json.dumps("{'error:' : ' Directory not found.'}")

@app.route('/<path:dir>/<arquivo>', methods=['DELETE'])
def delete(dir, arquivo):
    try:
        os.remove(arquivo)
   
    except Exception:
        return json.dumps("{'error:' : 'File not found.'}")

@app.route('/<path:dir>/<arquivo>', methods=['PUT'])
def put(dir, arquivo):
    try:
        with open(str(dir)+str(arquivo), "w") as f:
            f.write(request.form['data'])
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'Failed to write file.'}")

if __name__ == "__main__":
    app.run(port=7777, debug=True)

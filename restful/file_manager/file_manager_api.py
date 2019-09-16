import json
import os
from flask import Flask
from flask import Response
from flask import request
from dicttoxml import dicttoxml

app = Flask(__name__)


def success_message():
    return json.dumps("[{'status' : '200'}, {notice' : 'Operation completed successfully!'}")

@app.route('/<path:dir>/json', methods=['GET'])
def get_json(dir):
    dic = {}
    dic['files'] = os.listdir(dir)
    return json.dumps(dic)

@app.route('/<path:dir>/content', methods=['GET'])
def get_file(dir):
    dic = {}
    try:
        with open(dir, 'r') as file:
            text = file.read().replace('\n', '')
        dic['file-content'] = text
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'File not found.'}")
    return json.dumps(dic)

@app.route('/<path:dir>/xml', methods=['GET'])
def get_xml(dir):
    return  Response(dicttoxml(os.listdir(dir), custom_root="files", attr_type=False), mimetype='text/xml')  

@app.route("/<path:dir>", methods=['DELETE'])
def delete_dir(dir):
    try:
        os.rmdir(dir)
        return success_message()   
    
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : ' Directory not found.'}")

@app.route('/<path:dir>/<arquivo>', methods=['DELETE'])
def delete(dir, arquivo):
    try:
        os.remove(arquivo)
        return success_message()
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'File not found.'}")

@app.route('/<path:dir>/<arquivo>', methods=['PUT'])
def put(dir, arquivo):
    try:
        with open(str(dir)+str(arquivo), "w") as f:
            f.write(request.form['data'])
        return success_message()
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'Failed to write file.'}")



if __name__ == "__main__":
    app.run(port=7777, debug=True)

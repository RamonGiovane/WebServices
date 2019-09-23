import json
import os
from flask import Flask
from flask import Response
from flask import request
from dicttoxml import dicttoxml

app = Flask(__name__)


def success_message():
    return json.dumps("[{'status' : '200'}, {notice' : 'Operation completed successfully!'}")


def format_dir(diretorio):
    if ':' in diretorio:
        return diretorio
    else: 
        return "/" + diretorio 

@app.route('/<path:diretorio>/json', methods=['GET'])
def get_json(diretorio):
   
    dic = {}
    dic['files'] = os.listdir(format_dir(diretorio))
    return json.dumps(dic)

@app.route('/<path:diretorio>/content', methods=['GET'])
def get_file(diretorio):

    
    dic = {}
    try:
        with open(format_dir(diretorio), 'r') as file:
            text = file.read()#.replace('\n', '')
        dic['file-content'] = text
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'File not found.'}")
    return json.dumps(dic)

@app.route('/<path:diretorio>/xml', methods=['GET'])
def get_xml(diretorio):
    return  Response(dicttoxml(os.listdir(diretorio), custom_root="files", attr_type=False), mimetype='text/xml')  

@app.route("/<path:diretorio>", methods=['DELETE'])
def delete_dir(diretorio):
    try:
        os.rmdir(format_dir(diretorio))
        return success_message()   
    
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : ' Directory not found.'}")

@app.route('/<path:diretorio>/<arquivo>', methods=['DELETE'])
def delete(diretorio, arquivo):
    
    try:
        
        
        os.remove(format_dir(diretorio) + "/" + arquivo)
        return success_message()
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'File not found.'}")

@app.route('/<path:diretorio>/<arquivo>', methods=['PUT'])
def put(diretorio, arquivo):
    try:
        print(json.loads(request.data)['file-content'])
        with open(str(format_dir(diretorio))+ "/" + str(arquivo), "w") as f:
            f.write(json.loads(request.data)['file-content'])
        return success_message()
    except Exception as e:
        print(e)
        return json.dumps("{'error:' : 'Failed to write file.'}")



if __name__ == "__main__":
    app.run(port=7777, debug=True)

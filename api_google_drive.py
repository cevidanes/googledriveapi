import flask
import requests
import base64
from flask import request, jsonify
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST'])
def home():
    json_data = request.get_json(force=True)
    url_criativo = json_data['url_criativo']
    tipo_midia = json_data['tipo_midia']
    phone_number = json_data['phone_number']
    contato = json_data['contato']
    print(phone_number)
    print(contato)

    if url_criativo == None:
        dict_response = [{
            "imagem": "Imagem nao encontrada"
        }]

        return jsonify(dict_response)

    def submmit_image(contato, phone_number, base64Data):
        URL = "	http://127.0.0.1:3333/sendFile"

        body_request = {
            "sessionName": "rdb",
            "number": "5581999989702",
            "base64Data": base64Data,
            "fileName": "xx.jpg"
        }
        resp = requests.post(URL, json=body_request)

        return resp

    def download_file_from_google_drive(id, destination):
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()

        response = session.get(URL, params={'id': id}, stream=True)
        token = get_confirm_token(response)

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(URL, params=params, stream=True)

        save_response_content(response, destination)

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    if __name__ == "__main__":
        url_criativo = str(url_criativo)
        file_id = url_criativo.split('/')[5]

        file_id = url_criativo.split('/')[5]

        destination = 'img' + tipo_midia
        download_file_from_google_drive(file_id, destination)
        with open("img.jpg", "rb") as image_file:
            binary_file_data = image_file.read()
            base64_encoded_data = base64.b64encode(binary_file_data)
            encoded_string = base64_encoded_data.decode('utf-8')

        resp =submmit_image(contato, phone_number, encoded_string)

        dict_response = {
            "imagem": str(encoded_string)
        }

    return resp


app.debug = True
http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()

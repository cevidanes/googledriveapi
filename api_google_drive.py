import flask
import requests
import base64
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    query_parameters = request.args
    url_criativo = query_parameters.get('urlcriativo')

    if url_criativo ==None:
        dict_response = [{
            "imagem": "Imagem nao encontrada"
        }]

        return jsonify(dict_response)

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
        destination = 'img.jpg'

        download_file_from_google_drive(file_id, destination)


        with open("img.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print(type(encoded_string))
        dict_response = [{
            "imagem": str(encoded_string)
        }]

    return jsonify(dict_response)

app.run()
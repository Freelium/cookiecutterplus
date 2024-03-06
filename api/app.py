from flask import Flask, request, jsonify
from marshmallow import ValidationError
from waitress import serve
from cookiecutterplus import CookieCutterPlus, CCPStateManager
from .schema import MainSchema


class CookieCutterPlusAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route('/generate', methods=['POST'])(self.generate)

    @staticmethod
    def generate():
        # Validate the incoming request's content using MainSchema
        schema = MainSchema()
        try:
            valid_data = schema.load(request.json)
        except ValidationError as e:
            return jsonify({'error': f"Invalid request {e}"}), 400
        # Instantiate your CookieCutterPlus class and run the process
        try:
            print(f"Valid data {valid_data}\n type {type(valid_data)}")
            CookieCutterPlus(valid_data).run()
            return jsonify({'message': 'CookieCutter generation completed successfully'}), 201
        except ValueError or ValidationError as e:
            return jsonify({'error': f"Missing required parameters {e}"}), 400

    def run(self):
        serve(self.app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    cookie_cutter_api = CookieCutterPlusAPI()
    cookie_cutter_api.run()

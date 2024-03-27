from flask import Flask, request, jsonify
from flask_cors import CORS
from marshmallow import ValidationError
from waitress import serve
from cookiecutterplus import CookieCutterPlus, CookieCutterPlusError
from .schema import MainSchema


class CookieCutterPlusAPI:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.app.route('/generate', methods=['POST'])(self.generate)

    @staticmethod
    def generate():
        # Validate the incoming request's content using MainSchema
        schema = MainSchema()
        response = None
        valid_data = None
        try:
            print(f"Request JSON: {request.json}")
            valid_data = schema.load(request.json)
            print(f"Validated JSON: {valid_data}")
        except ValidationError as e:
            response = jsonify({'error': f"Invalid request {e}"}), 400
        # After Validation, Instantiate your CookieCutterPlus class and run the process
        try:
            print(f"Initializing cc+ with: {valid_data}")
            CookieCutterPlus(valid_data).run()
            response = jsonify({'message': 'CookieCutter generation completed successfully'}), 201
        except ValueError or ValidationError as e:
            response = jsonify({'error': f"Missing required parameters {e}"}), 400
        except CookieCutterPlusError as e:
            response = jsonify({'error': f"Cookiecutter plus issue {e}"}), 400

        
        return response

    def get_flask_app(self):
        return self.app
        
    def run(self):
        serve(self.app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    cookie_cutter_api = CookieCutterPlusAPI()
    cookie_cutter_api.run()

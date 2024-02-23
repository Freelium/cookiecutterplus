from flask import Flask, request, jsonify
from cookiecutterplus import CookieCutterPlus

class CookieCutterPlusAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route('/generate', methods=['POST'])(self.generate)

    @staticmethod
    def generate():
        data = request.json

        template_repo = data.get('template_repo')
        payload = data.get('payload')
        output_path = data.get('output_path')
        no_input = data.get('no_input', True)

        if not template_repo or not payload or not output_path:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Instantiate your CookieCutterPlus class and run the process
        cookie_cutter_instance = CookieCutterPlus(
            template_repo,
            payload,
            output_path,
            no_input
        )

        return jsonify({'message': 'CookieCutter generation completed successfully'}), 200

    def run(self):
        self.app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    cookie_cutter_api = CookieCutterPlusAPI()
    cookie_cutter_api.run()

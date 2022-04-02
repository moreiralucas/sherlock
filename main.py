import os
import json
from subprocess import check_output
from flask import (
    Flask, Response, request,
)
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    try:
        # Remove previous files
        os.system('rm submissions/*.*')

        extension = request.json.get('extension')
        submission1 = request.json.get('submission1')
        submission2 = request.json.get('submission2')

        with open(f'submissions/submission1.{extension}', 'wb') as file:
            file.write(submission1.encode())

        with open(f'submissions/submission2.{extension}', 'wb') as file:
            file.write(submission2.encode())

        command = ['./sherlock', '-e', extension, 'submissions']
        response = check_output(command).decode('utf-8')

        return Response(
            json.dumps({'resposta': response}),
            status=200,
            mimetype='application/json',
        )
    except Exception as err:
        app.logger.error('Failed to run plagiarism: %s', err)

    return Response(
        status=500,
        mimetype='application/json',
    )

if __name__ == '__main__':
    app.run()

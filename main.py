from flask import Flask, render_template, request
from template_manager import TemplateManager
import json
import base64
from os import path as osp

app = Flask(__name__)

@app.route('/api/job/<data>')
def generate_job_summary(data):
    data = base64.b64decode(data)
    data = json.loads(data)

    current_directory = osp.dirname(osp.realpath(__file__))


    tm = TemplateManager(current_directory, 'templates/job_summary.html')
    tm.add_css('css/job_summary.css')

    if 'repeated_parts' in data:
        for part_name, part_data in data['repeated_parts'].items():
            tm.fill_template_repeated_parts(part_name, part_data)

    if 'fields' in data:
        tm.fill_template_fields(data['fields'])

    # return 'PDF'
    return tm.generate_pdf()



if __name__ == '__main__':
    app.run()
    # generate_job_summary()
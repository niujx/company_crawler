from flask import Flask
from flask import render_template, make_response
from datetime import date
from export import export_to_excel

app = Flask(__name__)


@app.route('/test')
def hello_world():
    return 'Hello World!'


@app.route('/template/<name>')
def template(name):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    return 'this is task list'


@app.route('/download/<crawler>', methods=['GET', 'POST'])
def download(crawler):
    response = make_response(export_to_excel().export(crawler))
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.xls' % (crawler + '_' + str(date.today()))
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8964)

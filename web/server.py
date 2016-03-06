from flask import Flask
from flask import render_template, make_response
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from export import export_to_excel
from db.databases import Sqlite3DB
from run import start_crawler

app = Flask(__name__)


def job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_crawler, 'cron', hour='1')
    try:
        scheduler.start()
    except:
        scheduler.shutdown()


@app.route('/test')
def hello_world():
    return 'Hello World!'


@app.route('/template/<name>')
def template(name):
    return render_template('hello.html', name=name)


@app.route('/')
@app.route('/pages')
def index():
    page = request.args.get('page', '0')
    sqlite3db = Sqlite3DB()
    tasks = sqlite3db.find_task_by_limit(page)
    return render_template('list.html', list=tasks, pre=0 if int(page) - 20 < 0 else int(page) - 20,
                           next=int(page) + 20)


@app.route('/download/<crawler>/<today>', methods=['GET', 'POST'])
def download(crawler, today):
    print crawler, today
    response = make_response(export_to_excel().export(crawler, today))
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename=%s.xls' % (crawler + '_' + today)
    return response


if __name__ == '__main__':
    job()
    app.run(host='0.0.0.0', port=8964, debug=True)

from db.databases import Sqlite3DB

for i in xrange(0,100):
    Sqlite3DB().create_crawler_task('lagou')
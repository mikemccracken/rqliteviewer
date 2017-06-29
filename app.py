#!python

from flask import Flask
app = Flask(__name__)

import pyrqlite.dbapi2 as dbapi2

import sys

print("about to connect, sys.argv is {}".format(sys.argv))
# Connect to the database
connection = dbapi2.connect(
    host=sys.argv[1],
    port=sys.argv[2]
)
print("connected, {}".format(connection))

@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/tables')
def databases():
    r = "<html><head><title>Tables</title></head><body>"
    try:
        with connection.cursor() as cur:
            result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            table_names = sorted(zip(*result)[0])
            for table_name in table_names:
                r += "\n<h2>" + table_name + "</h2>"
                result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
                column_names = zip(*result)[1]
                r += "\t".join(column_names)
                r += "<br>"
                result2 =  cur.execute("select * from {}".format(table_name)).fetchall()
                for row in result2:
                    r += "\n" + "\t".join(["{}".format(v) for v in tuple(row)])

    finally:
        connection.close()
    r += "</html>"
    return r

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

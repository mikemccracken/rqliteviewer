#!python

from flask import Flask
app = Flask(__name__)

import pyrqlite.dbapi2 as dbapi2

import sys

connection = None

@app.route('/')
def main_page():
    r = "<html><head><title>Tables</title></head><body>"    
    if connection is None:
        return 'No connection, waiting for a relation.'
    else:
        r += "\n<h1>Connected to RQLite at {}:{} </h1>".format(sys.argv[1], sys.argv[2])
        try:
            with connection.cursor() as cur:
                result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                if len(result) == 0:
                    r += "No tables found!"
                else: 
                    table_names = sorted(zip(*result)[0])
                    for table_name in table_names:
                        r += "\n<h2>" + table_name + "</h2>"
                        result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
                        column_names = zip(*result)[1]
                        r += "<table><tr>"
                        for cn in column_names:
                            r += "<td>{}</td>".format(cn)
                        r += "</tr>\n"
                        result2 =  cur.execute("select * from {}".format(table_name)).fetchall()
                        for row in result2:
                            r += "<tr>"
                            for val in tuple(row):
                                r += "<td>{}</td>".format(val)
                            r += "</tr>"
                        r += "</table>"
        finally:
            connection.close()
        r += "</html>"
        return r


if __name__ == '__main__':

    print("about to connect, sys.argv is {}".format(sys.argv))
    if len(sys.argv) == 3:
        # Connect to the database
        connection = dbapi2.connect(
            host=sys.argv[1],
            port=sys.argv[2]
        )

    app.run(debug=True,host='0.0.0.0')

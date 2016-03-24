__author__ = 'robin.louvet@ge.com' #Some chunks coming from 'dattnguyen82'

import os
import flask as flsk
import sqlalchemy as sqla
import pandas as pd
import numpy as np
import json
import psycopg2

app = flsk.Flask(__name__)

errStr = ""

#Configuration
port = None
vcap = None
jdbc_uri = None
database_name = None
username = None
password_str = None
db_host = None
db_port = None
connected = False
conn = None
cur = None

portStr = os.getenv("VCAP_APP_PORT")

if portStr is not None:
    port = int(portStr)

services = os.getenv("VCAP_SERVICES")

if services is not None:
    vcap = json.loads(services)

if vcap is not None:
    postgres = vcap['postgres'][0]['credentials']
    if postgres is not None:
        jdbc_uri = postgres['jdbc_uri']
        database_name = postgres['database']
        username = postgres['username']
        password_str = postgres['password']
        db_host = postgres['host']
        db_port = postgres['port']

else:
    database_name = '<DATABASE_NAME>'
    username = '<USERNAME>'
    password_str = '<PASSWORD>'
    db_host = 'localhost'
    db_port = 5432


dialect = 'postgresql'
driver = 'psycopg2'
createEngineURL = dialect + '+' + driver + '://' + username + ':' + password_str + '@' + db_host + ':' + db_port + '/' + database_name

try:
    engine = sqla.create_engine(createEngineURL)
    connected = True
except:
    print "Could not create sqla engine!"
    connected = False

if connected:
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

    df.to_sql('data', engine)


### Main api - GET - provides connection info
@app.route('/', methods=['GET'])
def main():
    response = '<h1>Database Connection Info</h1><hr>'

    if jdbc_uri is not None:
        response += '<b>jdbc_uri:</b> ' + jdbc_uri + "<BR>"

    if database_name is not None:
        response += '<b>database:</b> ' + database_name + "<BR>"

    if username is not None:
        response += '<b>username:</b> ' + username + "<BR>"

    if password_str is not None:
        response += '<b>password:</b> ' + password_str + "<BR>"

    if db_host is not None:
        response += '<b>host:</b> ' + db_host + "<BR>"

    if db_port is not None:
        response += '<b>port:</b> ' + str(db_port) + "<BR>"

    response += '<hr>'

    if connected is True:
        response += '<font color="#00FF00"><b>Database connection is active</b></font>'
    else:
        response += '<font color="#FF0000"><b>Database is not connected</b></font>' + '<b>error:</b> ' + str(errStr) + "<BR>" 

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',
	port=port)
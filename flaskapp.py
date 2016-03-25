__author__ = 'robin.louvet@ge.com' #Some chunks coming from 'dattnguyen82'

import os
import sys
import logging
import flask as flsk
import sqlalchemy as sqla
import pandas as pd
import numpy as np
import json
import psycopg2

# Setup logging
app = flsk.Flask(__name__)

#formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
#handler = logging.StreamHandler(stream=sys.stdout)
#handler.setFormatter(formatter)
#handler.setLevel(logging.DEBUG)

#app.logger.addHandler(handler)
#app.logger.setLevel(logging.DEBUG)

#app.logger.info("Starting Flask Application")


def setupConfig():
    #Configuration
    #app.logger.info("Setting configuration")
    config = {
        'port' : None,
        'vcap' : None,
        'jdbc_uri' : None,
        'database_name' : None,
        'username' : None,
        'password_str' : None,
        'db_host' : None,
        'db_port' : None,
        'connected' : False,
        'conn' : None,
        'cur' : None
    }

    portStr = os.getenv("VCAP_APP_PORT")

    if portStr is not None:
        config['port'] = int(portStr)
        #app.logger.info("Flaskapp operating on port: %i", port)

    services = os.getenv("VCAP_SERVICES")

    if services is not None:
        config['vcap'] = json.loads(services)

    if config['vcap'] is not None:
        postgres = config['vcap']['postgres'][0]['credentials']
        if postgres is not None:
            config['jdbc_uri'] = postgres['jdbc_uri']
            config['database_name'] = postgres['database']
            config['username'] = postgres['username']
            config['password_str'] = postgres['password']
            config['db_host'] = postgres['host']
            config['db_port'] = postgres['port']
            #app.logger.info("Postgres configuration OK")

    else:
        config['database_name'] = '<DATABASE_NAME>'
        config['username'] = '<USERNAME>'
        config['password_str'] = '<PASSWORD>'
        config['db_host'] = 'localhost'
        config['db_port'] = 5432

    return config


def connectDb(username, password_str, db_host, db_port, database_name):
    dialect = 'postgresql'
    driver = 'psycopg2'
    createEngineURL = dialect + '+' + driver + '://' + username + ':' + password_str + '@' + db_host + ':' + db_port + '/' + database_name

    #app.logger.info("Trying to connect to POSTGRES db...")
    try:
        engine = sqla.create_engine(createEngineURL)
        connected = True
        #app.logger.info("Connected to postgres db: %s", database_name)
    except:
        connected = False
        #app.logger.info("Could not connect to postgres db")

    return connected, engine


def addEntry(engine):
    now = pd.to_datetime('now')
    df = pd.DataFrame(np.random.randn(1,4), index=now, columns=list('ABCD'))

    df.to_sql('data', engine, if_exists='append')

errStr = ""

config = setupConfig()
[connected, engine] = connectDb(config['username'], config['password_str'], config['db_host'], config['db_port'], config['database_name'])

# Main api - GET - provides connection info

@app.route('/', methods=['GET'])
def main():
    #addEntry(engine)

    response = '<h1>Database Connection Info</h1><hr>'

    if config['jdbc_uri'] is not None:
        response += '<b>jdbc_uri:</b> ' + config['jdbc_uri'] + "<BR>"

    if config['database_name'] is not None:
        response += '<b>database:</b> ' + config['database_name'] + "<BR>"

    if config['username'] is not None:
        response += '<b>username:</b> ' + config['username'] + "<BR>"

    if config['password_str'] is not None:
        response += '<b>password:</b> ' + config['password_str'] + "<BR>"

    if config['db_host'] is not None:
        response += '<b>host:</b> ' + config['db_host'] + "<BR>"

    if config['db_port'] is not None:
        response += '<b>port:</b> ' + str(config['db_port']) + "<BR>"

    response += '<hr>'

    if connected is True:
        response += '<font color="#00FF00"><b>Database connection is active</b></font>'
    else:
        response += '<font color="#FF0000"><b>Database is not connected</b></font>' + '<b>error:</b> ' + str(errStr) + "<BR>" 

    return response

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=config['port']
    )

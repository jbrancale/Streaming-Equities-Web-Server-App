import threading
from RandomDealData import *
import mysql.connector
from datetime import datetime
import json
from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


sqlHostAddr = 'mysql'
sqlRootPass = 'E3kWrJQRpNmytMNK'


# sqlHostAddr='192.168.99.100'
# sqlRootPass = 'ppp'


@app.route("/webserver_to_dao", methods=['GET'])
def deal_with_query():
    # collect JSON with query
    data = request.json

    # Connect to DB and run query
    connection = mysql.connector.connect(host=sqlHostAddr,
                                         database='mydb',
                                         user='root',
                                         password=sqlRootPass)
    cursor = connection.cursor()
    query = data['query']

    # Collect results of query
    results = cursor.execute(query)

    # Close DB connection and return record with rows
    cursor.close()
    connection.close()
    return results, 200

@app.route("/login", methods=['GET'])
def login():
    username = request.args.get('username', None)
    password = request.args.get('password', None)

    is_user_authenticated = authenticate_user(username, password)
    if is_user_authenticated == 1:
        params = {"type":"Trader"}
        return params, 200
    else:
        params = {"type": "None"}
        return params, 401

def authenticate_user(userid, password):
    connection = mysql.connector.connect(host=sqlHostAddr,
                                         database='mydb',
                                         user='root',
                                         password=sqlRootPass)
    query = ('SET @userId = "%s", @password ="%s"; ' % (userid, password))
    query += 'SELECT COUNT(1) FROM `Users` WHERE userId = @userId AND password = @password;'
    print(query)
    cursor = connection.cursor()
    results = cursor.execute(query, multi=True)
    result = 0
    is_user_authenticated = False
    for cur in results:
        if cur.with_rows:
            result = cur.fetchall()[0][0]
            print(result)

    if result == 1:
        is_user_authenticated = True

    cursor.close()
    connection.close()

    return is_user_authenticated


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def as_user(dct):
    return User(dct.get('username', None), dct.get('password', None))


def activate_stream():
    connection, cursor = connect_to_db()
    thr = threading.Thread(target=data_stream, args=(connection, cursor), kwargs={})
    thr.start()  # Will run "data_stream"

def data_stream(connection, cursor):
    # Create Random Data Generator Object
    randDataObj = RandomDealData()
    # Create instrument list
    instrumentList = randDataObj.createInstrumentList()
    while True:
        jsonRaw = randDataObj.createRandomData(instrumentList)
        jsonData = json.loads(jsonRaw)
        stream_to_sql(jsonData, connection, cursor)


def connect_to_db():
    try:
        connection = mysql.connector.connect(host=sqlHostAddr,
                                             database='mydb',
                                             user='root',
                                             password=sqlRootPass)
        cursor = connection.cursor()
        # result = cursor.execute("DELETE FROM Deals")
        return connection, cursor
    except mysql.connector.Error as error:
        connection.rollback()  # rollback if any exception occurred
        print("Failed inserting record into Deals table {}".format(error))

def disconnect_from_db(connection, cursor):
    # closing database connection.
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


def stream_to_sql(jsonData, connection, cursor):

    try:
        # Formats the time
        date_obj = datetime.strptime(jsonData['time'], "%d-%b-%Y (%H:%M:%S.%f)")
        dt = date_obj.strftime("%y-%m-%d %H:%M:%S.%f")

        sql_insert_query = " INSERT INTO Deals " \
                       " (dealId, `instrumentName`, `cpty`, `price`, `type`, `quantity`, `time`) " \
                       ' VALUES (' + str(jsonData['dealId']) + ' , "'+ jsonData['instrumentName'] + '","' \
                           + jsonData['cpty']+ '",' + str(jsonData['price']) + ',"' + jsonData['type'] + '",'\
                           +  str(jsonData['quantity'])\
                           + ',"' + str(dt) + '");'
        result = cursor.execute(sql_insert_query)

        connection.commit()
        print("Record inserted successfully into Deals table")
    except:
        print('skip. Deal ID exists')
        print(jsonData['dealId'])



def boot_app():
    app.run(debug=True, threaded=True, host='0.0.0.0', port='7000')

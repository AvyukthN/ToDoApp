from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
from credentials import creds
import datetime

client = MongoClient(creds['mongoConfigURI'])
db = client.ToDoDatabase

items = db.items

def itemAdder(description, date):
    itemDoc = {
        "desc": description,
        "duedate": date
    }
    items.insert_one(itemDoc)

app = Flask(__name__)

@app.route('/')
def home():
    description = request.args.get('item')
    date = request.args.get('date')
    
    if (description != None and date != None) and (description != "" and date != ""):
        itemAdder(description, date)
        # print(description, date)


    return render_template('index.html')

@app.route('/todo')
def todolist():
    arrDicts = []

    db = client['ToDoDatabase']
    collection = db['items']

    for post in collection.find():
        arrDicts.append(post)
    length = len(arrDicts)

    desc = request.args.get('desc')
    if desc != None:
        desc = desc[10:]
        collection.delete_one({"desc": desc})


    return render_template('todolist.html', arrayOfData=arrDicts, numAssignments=length)

if __name__ == '__main__':
    app.run(debug = True)
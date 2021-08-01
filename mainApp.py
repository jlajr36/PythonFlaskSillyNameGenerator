import os, random
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, func
from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = 'test'

#Make current dir working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

engine = create_engine('sqlite:///namesDB.db', echo = True)
meta = MetaData()
firstName = Table(
    'firstNames', meta,
    Column('ID', Integer, primary_key = True),
    Column('name', String),
)

lastName = Table(
    'lastNames', meta,
    Column('ID', Integer, primary_key = True),
    Column('name', String),
)

@app.route('/')
def index():
    conn = engine.connect()
    
    fnames = firstName.select()
    results = conn.execute(fnames)
    firstNames = []
    for row in results:
        firstNames.append(row[1])
    
    lnames = lastName.select()
    results = conn.execute(lnames)
    lastNames = []
    for row in results:
        lastNames.append(row[1])

    fcount = len(firstNames)
    lcount = len(lastNames)

    findex = random.randrange(fcount-1)
    lindex = random.randrange(lcount-1)

    strFirst = firstNames[findex]
    strLast = lastNames[lindex]
    
    conn.close()
    return render_template('index.html',strFirst=strFirst,strLast=strLast)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
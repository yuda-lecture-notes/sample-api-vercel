# import package
import psycopg2
from fastapi import FastAPI, Form, Request
from psycopg2.extras import RealDictCursor
import pandas as pd

try:
    # connection to database
    conn = psycopg2.connect(
        "dbname=db_api user=postgres.lewqnljcudghydncbnkb password=DswNVYj8MxEddPrV port=5432 host=aws-0-ap-southeast-1.pooler.supabase.com"
    )
except:
    print("error connected to db")

# create FastAPI instance/object
app = FastAPI()

# endpoint - main
@app.get("/")
def getMain(req: Request):
    return {
        "message": "welcome to sample-api-vercel",
        "url docs": "/docs",
        "url get data from db": "/data",
        "url get data from csv": "/csv",
    }

# endpoint - get all data from db
@app.get("/data")
def getDataDB():
    # fetch data from db
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from mock_users;")

    return cur.fetchall()
    
# endpoint - get data by id from db
@app.get("/data/{id}")
def getDataDBById(id: int):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"select * from mock_users where id = {id};")

    return cur.fetchone()

# endpoint - create new data in db
@app.post("/data/create")
def createDataDB(payload: dict):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"""
        insert into mock_users (first_name, last_name, email, gender)
        values ('{payload['first_name']}', '{payload['last_name']}', '{payload['email']}', '{payload['gender']}');
    """)
    # commit the changes to the database
    conn.commit()
    return {
        "data": payload,
        "status": "success"
    }

# endpoint - update data by id in db
@app.put("/data/update/{id}")
def updateDataEmailDB(id: int, email: str = Form(...)):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"""
        update mock_users 
        set email = '{email}'
        where id = {id};
    """)
    # commit the changes to the database
    conn.commit()
    return f"data with id {id} has been updated"


# endpoint - delete data by id in db
@app.delete("/data/delete/{id}")
def deleteDataDB(id: int):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(f"delete from mock_users where id = {id}")

    # commit the changes to the database
    conn.commit()
    return f"data with id {id} has been deleted"

# endpoint - get all data from csv
@app.get("/csv")
def getDataCSV():
    df = pd.read_csv('mock_users.csv')
    return df.to_dict(orient='records')

# endpoint - get data by id from csv
@app.get("/csv/{id}")
def getDataCSVById():
    df = pd.read_csv('mock_users.csv')

    # filter df
    filter_df = df[df['id'] == id]
    return filter_df.to_dict(orient='records')
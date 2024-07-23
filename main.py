# import package
from fastapi import FastAPI, Request, Header, HTTPException
import pandas as pd

# buat dataframe baru
df = pd.DataFrame()

# mengisi dataframe
df['UserName'] = ['Undertaker', 'Rey Mysterio', 'Edge']
df['Location'] = ['Texas', 'Mexico', 'Colorado']

# password api_key
API_KEY = "testingapitokenkey1234"

# buat object 
app = FastAPI()

# membuat function + url (endpoint)
# endpoint untuk retrieve all data
# http://www.domain.com
@app.get("/")
def handlerData(request: Request):
    # get request headers
    headers = request.headers

    return {
        "message": "this is fastapi data",
        "headers": headers
    }

# endpoint get all data from dataframe
# domain.com/data/texas -> return data yang location == texas
# domain.com/data/jakarta -> return data yang location == jakarta
@app.get("/data/{loc}")
def handlerDf(loc):
    # filter dataframe
    result = df.query(f"Location == '{loc}'")

    return result.to_dict(orient="records")

# endpoint secret
@app.get("/secret")
def handlerSecret(password: str = Header(None)):
    # cek api_key
    if password != API_KEY or password == None:
        raise HTTPException(detail="password salah!", status_code=401)

    return {
        "secret": "hanya saya dan tuhan yang tahu"
    }
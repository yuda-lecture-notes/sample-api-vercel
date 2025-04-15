from fastapi import FastAPI

# create FastAPI instance/object
app = FastAPI()

# endpoint - main
@app.get("/")
def getMain():
    return {
        "message": "Hello World",
    }
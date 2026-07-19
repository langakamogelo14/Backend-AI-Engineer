#Resource: https://realpython.com/get-started-with-fastapi/

#Step 1: Import the FastAPI library
from fastapi import FastAPI

# Step 2: a variable called app is created and it is assigned the value of FastAPI()
app = FastAPI()

#Step 3: a route or endpoint called "/" is created using the app.get() decorator.
#it calls a function called read_root()
@app.get("/")                         #When a GET request is made to the root URL ("/"), the read_root function will be called.
def read_root():                      #This function takes no arguments and returns a dictionary with a key-value pair of "Hello": "World"
    return {"Hello ": "World"}        #The dictionary is then converted into a JSON response by FastAPI and sent back to the client.




#fastapi dev main.py                (to start the server)
#fastapi run main.py                (to run the server in production mode, NOT recommended for production)
#Ctrl + c                           (to stop the server)


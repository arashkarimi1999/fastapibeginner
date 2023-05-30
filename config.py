from datetime import datetime
from fastapi import FastAPI
from routers import users
from time import time


app = FastAPI()
app.include_router(users.router, tags=['users'])


@app.middleware('http')
async def add_proccess_time_header(request, call_next):
    start = time()
    responce = await call_next(request)
    proccess_time = time() - start
    responce.headers['X-Proccess-Time'] = str(proccess_time)
    return responce


@app.on_event('startup')
def startup_event():
    with open('server_time_log.log', "a") as log:
        log.write(f'application started at:{datetime.now()} \n')


@app.on_event('shutdown')
def shutdown_event():
    with open('server_time_log.log', "a") as log:
        log.write(f'application shut down at:{datetime.now()} \n')


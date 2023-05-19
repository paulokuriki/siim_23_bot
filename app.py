# https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

import io

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
# Import necessary modules
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from image_lib import download_image, rotate_image
import messages as msgs
import database as db
import db_schema
import hyperparameters as hp
# Import functions from other modules
from telegram_aux import *

scheduler = BackgroundScheduler(jobstores={'default': SQLAlchemyJobStore(url=db_schema.DATABASE_URL)})
scheduler.start()

# Create FastAPI app object
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Route for the root directory; handles Telegram messages
@app.post("/", response_class=HTMLResponse)
async def index(request: Request):
    # Get the message from the POST request
    req = await request.json()

    # Parse the message to a structured dictionary
    dict_msg = tel_parse_message(req)

    user_id = dict_msg.get('user_id', '')
    txt = dict_msg.get('txt', '')

    # load dict from disk, update it and save it back to disk
    dict_user_hp = db.load_dict(user_id)
    dict_user_hp = msgs.update_dict_user_hps(dict_user_hp, dict_msg)
    db.save_dict(dict_user_hp, user_id)

    # register the competitor in the database, if necessary
    if not db.list_competitors(dict_msg):
        db.insert_competitor(dict_msg)

    # evaluate the user's message and respond accordingly
    if txt == 'new_model':
        dict_user_hp = {}
        db.save_dict(dict_user_hp, user_id)
        msgs.select_batch_size(dict_msg)

    elif txt in hp.batch_sizes:
        msgs.select_epochs(dict_msg)

    elif txt in hp.epochs:
        msgs.select_lr(dict_msg)

    elif txt in hp.learning_rates:
        msgs.select_batch_norm(dict_msg)

    elif txt in hp.batch_norm:
        msgs.select_filters(dict_msg)

    elif txt in hp.filters:
        msgs.select_dropout(dict_msg)

    elif txt in hp.dropout:
        msgs.select_image_size(dict_msg)

    elif txt in hp.image_size:
        msgs.select_gpu(dict_msg, dict_user_hp)

    elif txt in msgs.GPU_NAMES:
        msgs.submit_training(dict_msg, dict_user_hp, request=request, scheduler=scheduler)

    elif txt == "list_competitors":
        results = json.dumps(db.list_competitors(), indent=2, default=str)
        msg = 'Users:\n' + results
        tel_send_message(dict_msg, msg)

    elif txt == "show_leaderboard":
        msgs.show_leaderboard(dict_msg)

    elif txt == "show_status":
        msgs.show_training_status(dict_msg, request=request)

    else:
        # clear dict user hyperparameters
        dict_user_hp = {}
        db.save_dict(dict_user_hp, user_id)
        msgs.welcome_message(dict_msg)

    return JSONResponse('ok', status_code=200)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    df = db.get_leaderboard_df()
    df['last_submission'] = df['last_submission'].apply(msgs.calculate_time_ago)
    df['rank'] = df.index + 1
    df = df[['rank', 'fullname', 'score', 'entries', 'last_submission']]
    df.columns = ['#', 'Team', 'Score', 'Entries', 'Last']
    return templates.TemplateResponse("index.html", {"request": request, "df": df}, status_code=200)


# Route for uploading JSON records to the database
@app.post("/upload_json")
async def upload_json(request: Request):
    try:
        # Get the JSON record from the POST request
        json_record = await request.json()
        # insert the record into the database using a function from database.py
        results = db.insert_json(json_record)
        # return an appropriate response based on the result of the insertion
        if results == 'JSON inserted successfully.':
            return JSONResponse(results, status_code=200)
        else:
            return JSONResponse(results, status_code=500)

    except Exception as e:
        # return an error response if the insertion fails
        return JSONResponse(e, status_code=500)


# Route for listing pretrained model metrics
@app.get("/list_pretrained_metrics", response_class=JSONResponse)
def list_pretrained_metrics():
    # get the pretrained metrics from the database using a function from database.py
    results = json.dumps(db.list_pretrained(), indent=2, default=str)
    # return the results as a JSON object
    return JSONResponse(results, status_code=200)


# route for listing pretrained model metrics
@app.get("/notify_results")
@app.head("/notify_results")  # https://uptimerobot.com/ calls the api through a HEAD request each 5 min
def notify_results(request: Request):
    # Notify the competitors
    results = msgs.notify_finished_trainings(base_url=str(request.base_url))

    # Return the number of users notified
    return JSONResponse(f'{str(results)} users notified.', status_code=200)


# route for listing pretrained model metrics
@app.get("/list_competitors", response_class=JSONResponse)
def list_competitors():
    # get the pretrained metrics from the database using a function from database.py
    results = json.dumps(db.list_competitors(), indent=2, default=str)
    # return the results as a JSON object
    return JSONResponse(results, status_code=200)


# Route for listing pretrained model metrics
@app.get("/api/leaderboard", response_class=JSONResponse)
async def get_leaderboard():
    df = db.get_leaderboard_df()
    df['last_submission'] = await df['last_submission'].apply(msgs.calculate_time_ago)
    df['rank'] = df.index + 1
    df = df[['rank', 'fullname', 'score', 'entries', 'last_submission']]
    df.columns = ['#', 'Team', 'Score', 'Entries', 'Last']

    return JSONResponse(df.to_dict(orient="records"), status_code=200)


@app.get("/rotate_image", tags=["images"], name="rotate_image")
async def get_rotated_image(image_url: str = Query(...)):
    image_bytes = await download_image(image_url)
    rotated_image_bytes = await rotate_image(io.BytesIO(image_bytes))

    return StreamingResponse(rotated_image_bytes, media_type="image/png")

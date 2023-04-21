# https://www.pragnakalp.com/create-telegram-bot-using-python-tutorial-with-examples/

# Import necessary modules
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import aiohttp

from messages import *
# Import functions from other modules
from telegram_aux import *

# Create FastAPI app object
app = FastAPI(docs_url=None, redoc_url=None)

# Route for the root directory; handles Telegram messages
@app.post("/", response_class=HTMLResponse)
async def index(request: Request):
    # Get the message from the POST request
    msg = await request.json()

    # Parse the message to a structured dictionary
    dict_msg = tel_parse_message(msg)

    user_id = dict_msg.get('user_id', '')
    txt = dict_msg.get('txt', '')

    # load dict from disk, update it and save it back to disk
    dict_user_hp = db.load_dict(user_id)
    dict_user_hp = update_dict_user_hps(dict_user_hp, dict_msg)
    db.save_dict(dict_user_hp, user_id)

    # register the competitor in the database, if necessary
    if not db.list_competitors(dict_msg):
        db.insert_competitor(dict_msg)

    # evaluate the user's message and respond accordingly
    if txt in 'new_model':
        dict_user_hp = {}
        db.save_dict(dict_user_hp, user_id)
        select_batch_size(dict_msg)

    elif txt in hp.batch_sizes:
        select_epochs(dict_msg)

    elif txt in hp.epochs:
        select_lr(dict_msg)

    elif txt in hp.learning_rates:
        select_batch_norm(dict_msg)

    elif txt in hp.batch_norm:
        select_filters(dict_msg)

    elif txt in hp.filters:
        select_dropout(dict_msg)

    elif txt in hp.dropout:
        select_image_size(dict_msg)

    elif txt in hp.image_size:
        confirm_training(dict_msg, dict_user_hp)

    elif txt == "submit_training":
        submit_model(dict_msg, dict_user_hp)

    elif txt == "list_competitors":
        results = json.dumps(db.list_competitors(), indent=2, default=str)
        msg = 'Users:\n' + results
        tel_send_message(dict_msg, msg)

    elif txt == "show_leaderboard":
        show_leaderboard(dict_msg)

    elif txt == "show_status":
        show_training_status(dict_msg)
    else:
        dict_user_hp = {}
        db.save_dict(dict_user_hp, user_id)
        welcome_message(dict_msg)

    return JSONResponse('ok', status_code=200)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    uptime_robot_page = await fetch_uptime_robot_page()
    return HTMLResponse(f"""
        <h1>Welcome to the SIIM AI Playground API!</h1>
        <p>Open Telegram and look for the bot called @siim_23_bot to start to play.</p>
        <iframe srcdoc="{uptime_robot_page}" width="100%" height="600px" frameborder="0"></iframe>
    """, status_code=200)


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
@app.head("/notify_results")   # https://uptimerobot.com/ calls the api through a HEAD request each 5 min
def notify_results():
    # Notify the competitors
    results = notify_finished_trainings()

    # Return the number of users notified
    return JSONResponse(f'{str(results)} users notified.', status_code=200)



# route for listing pretrained model metrics
@app.get("/list_competitors", response_class=JSONResponse)
def list_competitors():
    # get the pretrained metrics from the database using a function from database.py
    results = json.dumps(db.list_competitors(), indent=2, default=str)
    # return the results as a JSON object
    return JSONResponse(results, status_code=200)


async def fetch_uptime_robot_page():
    url = "https://stats.uptimerobot.com/KVqA7IDVgq"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
from telegram_aux import tel_send_message, tel_send_inlinebutton
import hyperparameters as hp

# Sends a welcome message to the user and provides options for training a new model or checking status
def welcome_message(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"Hello, {fullname}! Welcome to the SIIM 2023 AI Playground")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train new model", "callback_data": "new_model"},
                           {"text": "Check Status", "callback_data": "show_status"}])

# Sends options for selecting batch size to the user
def select_batch_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, "It's time to have fun. Let's train your new model.")
    tel_send_message(chat_id, "First, you have to select a batch size.")
    tel_send_inlinebutton(chat_id, "Batch Size:", create_dict_options(hp.batch_sizes))

# Sends options for selecting number of epochs to the user
def select_epochs(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"Now, select the number of epochs to be trained.")
    tel_send_inlinebutton(chat_id, "Epochs:", create_dict_options(hp.epochs))

# Sends options for selecting learning rate to the user
def select_lr(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, "Great, now let's select the learning rate.")
    tel_send_inlinebutton(chat_id, "Learning Rates:", create_dict_options(hp.learning_rates))

# Sends options for selecting whether or not to use batch normalization to the user
def select_batch_norm(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"It's time to decide if you want to use batch normalization.")
    tel_send_inlinebutton(chat_id, "Batch Norm:", create_dict_options(hp.batch_norm))

# Sends options for selecting number of filters to the user
def select_filters(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, "Awesome. Now, a important hyperparameter: the number of filters.")
    tel_send_inlinebutton(chat_id, "Number of Filters:", create_dict_options(hp.filters))

# Sends options for selecting whether or not to use dropout to the user
def select_dropout(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"Optionally, you can opt to apply dropout to your model.")
    tel_send_inlinebutton(chat_id, "Dropout:", create_dict_options(hp.dropout))

# Sends options for selecting image size to the user
def select_image_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, "For last, but not the least, select the image size to input in your model.")
    tel_send_inlinebutton(chat_id, "Image Size:", create_dict_options(hp.image_size))


def confirm_training(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id,
                     f"Nice work, {fullname}! If you are ready to train you model, click on the TRAIN button below.")
    tel_send_message(chat_id, "The system will estimate the training time.")
    tel_send_message(chat_id, "If you want to cancel and define a new model, click on the button CANCEL.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "TRAIN", "callback_data": "submit_training"},
                           {"text": "CANCEL", "callback_data": "new_model"}])


def submit_model(chat_id: str, txt: str = "", user_id: str = "", username: str = "", fullname: str = ""):
    tel_send_message(chat_id, "Your model was submitted to the training queue. ")
    tel_send_message(chat_id, "The estimated training time is <TODO function calculate_estimated_time()>")
    tel_send_message(chat_id, "Time remaining: <TODO function calculate_remaining_time()>")
    tel_send_message(chat_id,
                     "If you want to cancel the training process and define a new model, click on the CANCEL button.")
    tel_send_message(chat_id, "Otherwise, WAIT for the time to finish your model's training session.")
    tel_send_message(chat_id, "You'll receive a message with metrics results and your position on the leaderboard.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "CANCEL", "callback_data": "new_model"},
                           {"text": "STATUS", "callback_data": "show_status"},
                           {"text": "LEADERBOARD", "callback_data": "show_leaderboard"}])


def show_training_status(chat_id: str, txt: str = "", user_id: str = "", username: str = "", fullname: str = ""):
    tel_send_message(chat_id, "*TRAINING STATUS:*")
    tel_send_message(chat_id, "The estimated training time is <function calculate_estimated_time()>")
    tel_send_message(chat_id, "Time remaining: <TODO function calculate_remaining_time()>")
    tel_send_message(chat_id,
                     "If you want to cancel the training process and define a new model, click on the CANCEL button.")
    tel_send_message(chat_id, "Otherwise, you can check the training session STATUS at any time.")
    tel_send_message(chat_id, "You'll receive a message with the metrics results and your position on the leaderboard as soon as the model's training is finished.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "CANCEL", "callback_data": "new_model"},
                           {"text": "STATUS", "callback_data": "show_status"},
                           {"text": "LEADERBOARD", "callback_data": "show_leaderboard"}])


def show_leaderboard(chat_id: str, txt: str = "", user_id: str = "", username: str = "", fullname: str = ""):
    tel_send_message(chat_id, "LEADERBOARD")
    tel_send_message(chat_id, "<TODO function show_leaderboard()>")


def create_dict_options(list_options):
    list_dict = []
    for option in list_options:
        text = option.split("_")[1]
        callback_data = option
        list_dict.append({"text": text, "callback_data": callback_data})

    return list_dict

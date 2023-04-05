from telegram_aux import tel_send_message, tel_send_inlinebutton
import hyperparameters as hp


def welcome_message(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Hello, {fullname}! Welcome to the SIIM 2023 AI Playground")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train new model", "callback_data": "new_model"},
                           {"text": "Check Status", "callback_data": "check_status"},
                           {"text": "List Competitors", "callback_data": "list_competitors"}])


def select_batch_size(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, "It's time to have fun. Let's train your new model.")
    tel_send_message(chat_id, "First, you have to select a batch size.")
    tel_send_inlinebutton(chat_id, "", create_dict_options(hp.batch_sizes))


def select_epochs(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Now, select the number os epochs to be trained.")
    tel_send_inlinebutton(chat_id, "Epochs:", create_dict_options(hp.epochs))


def select_lr(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Great, now let's select the learning rate.")
    tel_send_inlinebutton(chat_id, "Learning Rates:", create_dict_options(hp.learning_rates))


def select_batch_norm(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"It's time to decide if you want to use batch normalization.")
    tel_send_inlinebutton(chat_id, "Batch Norm:", create_dict_options(hp.batch_norm))


def select_filters(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Awesome. Now, a important hyperparameter: the number of filters.")
    tel_send_inlinebutton(chat_id, "Number of Filters:", create_dict_options(hp.filters))


def select_dropout(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Optionally, you can opt to apply dropout to your model.")
    tel_send_inlinebutton(chat_id, "Dropout:", create_dict_options(hp.dropout))


def select_image_size(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"For last, but not the least, select the image size to input in your model.")
    tel_send_inlinebutton(chat_id, "Image Size:", create_dict_options(hp.image_size))


def confirm_training(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id,
                     f"Nice work, {fullname}! If you are ready to train you model, click on the TRAIN button below.")
    tel_send_message(chat_id, "The system will estimated training time.")
    tel_send_message(chat_id, "If you want to cancel and define a new model, click on the button CANCEL.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "TRAIN", "callback_data": "submit_training"},
                           {"text": "CANCEL", "callback_data": "new_model"}])


def submit_model(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Your model was submitted to the training queue. ")
    tel_send_message(chat_id, "The estimated training time is <function calculate_estimated_time()>")
    tel_send_message(chat_id, "Time remaining: <function calculate_remaining_time()>")
    tel_send_message(chat_id,"If you want to cancel the training process and define a new model, click on the CANCEL button.")
    tel_send_message(chat_id, "Otherwise, WAIT for the time to finish your model's training session.")
    tel_send_message(chat_id, "You'll receive a message with metrics results and your position on the leaderboard.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "WAIT", "callback_data": ""},
                           {"text": "CANCEL", "callback_data": "new_model"}])


def create_dict_options(list_options):
    list_dict = []
    for option in list_options:
        text = option.split("_")[1]
        callback_data = option
        list_dict.append({"text": text, "callback_data": callback_data})

    return list_dict

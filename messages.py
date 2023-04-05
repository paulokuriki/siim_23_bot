from telegram_aux import tel_send_message, tel_send_inlinebutton

def welcome_message(chat_id: str, txt: str, username: str, fullname: str)
    tel_send_message(chat_id, f"Hello, {fullname}! Welcome to the SIIM 2023 AI Playground")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train new model", "callback_data": "new_model"},
                          {"text": "Check Status", "callback_data": "check_status"},
                          {"text": "List Competitors", "callback_data": "list_competitors"}])



def create_new_model(chat_id: str, txt: str, username: str, fullname: str):
    tel_send_message(chat_id, f"Creating a new model for user {username}.")
    tel_send_inlinebutton(chat_id, "Select your architecture:",
                          [{"text": "EfficientNet", "callback_data": "efficient_net"},
                           {"text": "ResNet", "callback_data": "res_net"}])
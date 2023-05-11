import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Request

import database as db
import db_schema
import hyperparameters as hp
from telegram_aux import tel_send_message, tel_send_inlinebutton, tel_send_image

from apscheduler.schedulers.background import BackgroundScheduler

def update_dict_user_hps(dict_user_hp: dict = {}, dict_msg: dict = {}) -> dict:
    # Get the user_id and txt fields from the dict_msg dictionary, providing default values if the keys are not found
    txt = dict_msg.get('txt', '')

    # Call the extract_dict_options function to parse the txt field into a key-value pair
    key, value = extract_dict_options(txt)

    # If key and value variables have 'values'
    if key != '' and value != '':
        # Update the user's dictionary with the new key-value pair
        dict_user_hp[key] = value

    # Return the updated main dictionary (dict_users_hp)
    return dict_user_hp


# Sends a welcome message to the user and provides options for training a new model or checking status
def welcome_message(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    fullname = dict_msg.get('fullname', '')

    tel_send_message(chat_id, f"Hello, {fullname}! Welcome to the SIIM 2023 AI Playground 🛝.")
    tel_send_message(chat_id, "Today you will be developing a deep learning-based model to segment kidneys in MR images. The model is based on the U-Net architecture. There are many hyper-parameters that need to be adjusted to create a high performing model. We will walk through these parameters, and you will be able to learn about them, and specify their values in your model. You will then see how well your model was trained and its performance on a hold-out data set. Your performance will be compared with others, and you can see how well you did on the leaderboard 🏆📊.")
    tel_send_message(chat_id, "*Some details:*📝\n"
                     "*1. 💻 Deep Learning Model:* In this project, you'll be using a deep learning model, which is a type of artificial intelligence algorithm that can learn complex patterns from data. In this case, the data consists of MR images of kidneys.\n"
                     "*2. 🎭 Segmentation:* The goal of this project is to segment kidneys in MR images, which means identifying the boundaries and regions of the kidneys in the images. You are creating an AI model that decides for every voxel (a 3D pixel) whether it is, or isn’t, a kidney voxel.\n"
                     "*3. 🩻 U-Net Architecture:* U-Net is a popular convolutional neural network (CNN) architecture specifically designed for image segmentation tasks. Its unique U-shaped structure allows it to capture both local and global context in images, making it suitable for medical image segmentation."
                     )
    tel_send_inlinebutton(chat_id, "Let’s get started!",
                          [{"text": "Train new model", "callback_data": "new_model"},
                           {"text": "Check Status", "callback_data": "show_status"}])


# Sends options for selecting batch size to the user
def select_batch_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "🗃️ *BATCH SIZE*")
    tel_send_message(chat_id, "This parameter determines the *number of images* used in each update of the model's weights. A *smaller batch* size may lead to *more accurate* weight updates, but it will also require more iterations and, therefore, *longer training times*.\n"
                              "*- ⬆️ Increasing batch size:* This can lead to *faster training* since more data points are processed simultaneously, but it might require more memory. A larger batch size can also result in *less accurate* gradient estimates, potentially making the training less stable.\n"
                              "*- ⬇️ Decreasing batch size:* This can lead to *slower training*, as fewer data points are processed at once, but it can also provide *more accurate* gradient estimates, making training more stable. Additionally, it requires less memory, which can be helpful for training on limited hardware.")
    tel_send_inlinebutton(chat_id, "*Select the Batch Size:*", create_dict_options(hp.batch_sizes))


# Sends options for selecting number of epochs to the user
def select_epochs(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "📆 *EPOCHS*")

    tel_send_message(chat_id, "This is the number of times the model will iterate through the entire dataset during training. More epochs might result in better performance but at the cost of longer training time.\n"
                              "*- 🔁 Increasing the number of epochs:* When you increase the number of epochs, your model will iterate through the entire dataset more times during training. This may result in *improved performance*, as the model has more opportunities to learn from the data. However, it also *increases the training time* and may lead to _overfitting_ if the model starts memorizing the training data instead of learning to generalize.\n"
                              "*- ▶️ Decreasing the number of epochs:* Decreasing the number of epochs means the model will iterate through the dataset fewer times during training. This can lead to *shorter training* times but may result in _underfitting_, as the model might not have enough time to learn the underlying patterns in the data. A model with too few epochs might show *poor performance* on both the training and validation datasets."
                              )
    tel_send_inlinebutton(chat_id, "*Select the Number of Epochs:*", create_dict_options(hp.epochs))


# Sends options for selecting learning rate to the user
def select_lr(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "👣 *LEARNING RATE*")
    tel_send_message(chat_id, "This is a critical hyperparameter that controls the step size of the model's weight updates during training. A smaller learning rate leads to slower convergence but potentially more accurate results, while a larger learning rate leads to faster convergence but possibly less accurate results.\n"
                              "*- 🦾 Increasing the learning rate:* A higher learning rate allows the model to update its weights more aggressively during training. This can lead to *faster convergence* but may cause the model to _overshoot_ the optimal weights, resulting in *reduced accuracy or unstable training*. In some cases, a high learning rate can cause the model to diverge, meaning it will not learn anything useful.\n"
                              "*- 🦿 Decreasing the learning rate:* A lower learning rate causes the model to update its weights more cautiously during training. While this can lead to *more accurate results*, it also *increases the time* it takes for the model to converge. In some cases, a low learning rate can cause the model to get stuck in a _suboptimal solution_, never reaching the best possible performance."                              )
    tel_send_inlinebutton(chat_id, "*Select the Learning Rate*:", create_dict_options(hp.learning_rates))


# Sends options for selecting whether or not to use batch normalization to the user
def select_batch_norm(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "☮️ *BATCH NORMALIZATION*")
    tel_send_message(chat_id, "This is a technique used to improve the training of deep neural networks by normalizing the inputs of each layer. It helps reduce the internal covariate shift, which means that the distribution of inputs to a layer remains more stable during training. This results in faster convergence and improved overall performance. In a U-Net architecture, you can apply batch normalization after each convolutional layer. Try training with and without Batch Normalization to see how training and performance are affected.")
    tel_send_message(chat_id, "♒ *Training WITH batch normalization:*\n" 
                              "_- Faster convergence:_ Batch normalization helps reduce the internal covariate shift by normalizing the inputs to each layer during training. This can lead to faster convergence, as the model's weights can be updated more efficiently. It allows you to use higher learning rates without the risk of divergence.\n"
                              "_- Improved performance:_ By normalizing the inputs, batch normalization can help the model learn more complex features and generalize better to unseen data. This can result in improved performance on the validation dataset.\n"
                              "_- Regularization effect:_ Batch normalization introduces some noise into the model during training, which can have a slight regularization effect. This may help reduce the risk of overfitting.\n"
                              "_- Increased computational complexity:_ While batch normalization can improve the training process, it also adds computational complexity to the model. This can result in longer training times and increased memory requirements.")
    tel_send_message(chat_id, "📈 *Training WITHOUT batch normalization:*\n" 
                              "_- Faster convergence:_ Batch normalization helps reduce the internal covariate shift by normalizing the inputs to each layer during training. This can lead to faster convergence, as the model's weights can be updated more efficiently. It allows you to use higher learning rates without the risk of divergence.\n"
                              "_- Improved performance:_ By normalizing the inputs, batch normalization can help the model learn more complex features and generalize better to unseen data. This can result in improved performance on the validation dataset.\n"
                              "_- Regularization effect:_ Batch normalization introduces some noise into the model during training, which can have a slight regularization effect. This may help reduce the risk of overfitting.\n"
                              "_- Increased computational complexity:_ While batch normalization can improve the training process, it also adds computational complexity to the model. This can result in longer training times and increased memory requirements.")

    tel_send_inlinebutton(chat_id, "*Select the Batch Norm*:", create_dict_options(hp.batch_norm))


# Sends options for selecting number of filters to the user
def select_filters(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "📔 *FILTER KERNELS*")
    tel_send_message(chat_id, "In a convolutional neural network, filters (or kernels) are used to extract features from the input images. The number of filters in each layer determines the complexity of features the network can learn. In a U-Net architecture, the number of filters typically doubles at each down-sampling layer and halves at each up-sampling layer. A common starting point for the first layer is 64 filters, followed by 128, 256, and so on, as you go deeper into the network. However, you can experiment with different numbers of filters based on your specific problem and computational resources.\n"
                              "*- 📚 Increasing the number of convolutional filters:* Using more filters in each layer allows the model to learn a greater variety of features from the input images. This can lead to improved performance, especially for complex tasks or high-resolution images. However, increasing the number of filters also increases the model's complexity and computational requirements, which can lead to longer training times and the risk of overfitting.\n"
                              "*- 📗 Decreasing the number of convolutional filters:* Reducing the number of filters in each layer simplifies the model, which can reduce the risk of overfitting and decrease the computational requirements. However, this simplification may also limit the model's ability to learn complex features from the input images, potentially reducing its overall performance.")


    tel_send_inlinebutton(chat_id, "*Select the Number of Filters:*", create_dict_options(hp.filters))


# Sends options for selecting whether or not to use dropout to the user
def select_dropout(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "🫣 *DROPOUT*")
    tel_send_message(chat_id, "Dropout is a regularization technique that helps prevent overfitting in deep learning models. During training, dropout randomly sets a fraction of the neurons (units) in a layer to zero at each update, which prevents the model from becoming too reliant on any single neuron. The dropout rate is a hyperparameter that determines the fraction of neurons to drop; common values are between 0.1 and 0.5. In a U-Net architecture, you can apply dropout between the layers or after each convolutional layer, depending on your preference.")
    tel_send_message(chat_id, "🙈🙈🙈 *Increasing dropout rate:* If you increase the dropout rate, a larger fraction of neurons will be dropped out (set to zero) during training. This can have several effects on the model:\n" 
                              "_- Regularization effect:_ A higher dropout rate can improve the model's ability to generalize to new data by preventing overfitting. By dropping out more neurons, the model becomes less reliant on any single neuron, which encourages it to learn more robust and diverse features from the data.\n"
                              "_- Slower convergence:_ Since more neurons are dropped out, the model's effective capacity is reduced during training, which can slow down the learning process. This may result in longer training times to reach the desired performance.\n"
                              "_- Underfitting risk:_ If the dropout rate is set too high, the model may struggle to learn from the data, leading to underfitting. In this case, the model's performance on both the training and validation datasets may be poor.\n")
    tel_send_message(chat_id, "🐵 *Decreasing dropout rate:* If you decrease the dropout rate, a smaller fraction of neurons will be dropped out during training. This can have the following effects on the model:\n" 
                              "_- Reduced regularization effect:_ A lower dropout rate reduces the regularization effect, which may increase the risk of overfitting. If the model becomes too reliant on specific neurons, it might perform well on the training data but poorly on new, unseen data.\n"
                              "_- Faster convergence:_ Since fewer neurons are dropped out, the model's effective capacity during training is increased. This can lead to faster learning and shorter training times to reach the desired performance.\n"
                              "_- Overfitting risk:_ If the dropout rate is set too low, the model might overfit the training data, learning to memorize it instead of generalizing to new data. In this case, the model's performance on the training dataset may be very good, but its performance on the validation dataset may be poor.\n")


    tel_send_inlinebutton(chat_id, "*Use Dropout:*", create_dict_options(hp.dropout))


# Sends options for selecting image size to the user
def select_image_size(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')

    tel_send_message(chat_id, "🖼️ *IMAGE SIZE*")
    tel_send_message(chat_id, "The image input size is an important parameter that defines the dimensions (width and height) of the input images fed to the neural network. In the U-Net architecture, the input size should be divisible by the number of down-sampling operations (usually a power of 2), to ensure the model can process the images without issues. For instance, if your U-Net has four down-sampling operations, an input size of 256x256 would be appropriate. You may need to resize or crop your original MR images to match the chosen input size.")
    tel_send_message(chat_id, "🔷 *Increasing image input size:* If you increase the image input size, you will feed larger images into the model during training. This can have several effects on the model:\n" 
                              "_- More details:_ Larger images contain more details and can potentially help the model learn more fine-grained features. This might improve the model's performance, especially for tasks that require high-resolution input data.\n"
                              "_- Increased computational requirements:_ Processing larger images requires more memory and computational resources, which can lead to longer training times and greater hardware demands. This can be a limitation, especially on systems with limited GPU memory.\n"
                              "_- Risk of overfitting:_ Feeding larger images into the model may increase the risk of overfitting if the dataset is small or if the model's capacity is not adjusted accordingly. The model may start learning to memorize noise or artifacts specific to the training images rather than generalizing to unseen data.\n")
    tel_send_message(chat_id, "🔹 *Decreasing image input size:* If you decrease the image input size, you will feed smaller images into the model during training. This can have the following effects on the model:\n" 
                              "_- Less details:_ Smaller images contain less detail, which can limit the model's ability to learn fine-grained features. This might negatively affect the model's performance, especially for tasks that require high-resolution input data.\n"
                              "_- Reduced computational requirements:_ Processing smaller images requires less memory and computational resources, which can result in shorter training times and lower hardware demands. This can be beneficial, especially on systems with limited GPU memory.\n"
                              "_- Increased risk of underfitting:_ Feeding smaller images into the model may increase the risk of underfitting if the reduced resolution leads to the loss of important information. In this case, the model may struggle to learn the underlying patterns in the data, resulting in poor performance on both training and validation datasets.\n")

    tel_send_inlinebutton(chat_id, "*Select the Image Size:*", create_dict_options(hp.image_size))


def confirm_training(dict_msg: dict = {}, dict_user_hp: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    fullname = dict_msg.get('fullname', '')

    txt_user_hps = parse_user_hps(dict_user_hp)

    tel_send_message(chat_id, f"🎉🎊 Nice work, {fullname}!")
    tel_send_message(chat_id, f"Here are your selected hyperparameters:{txt_user_hps}")
    tel_send_message(chat_id, "If you are happy with your selection, click on the [Train] button below.")
    tel_send_message(chat_id, "If you want to cancel and define a new model, click on the [Cancel] button.")
    tel_send_inlinebutton(chat_id, "Select your option:",
                          [{"text": "Train", "callback_data": "submit_training"},
                           {"text": "Cancel", "callback_data": "new_model"}])


def submit_model(dict_msg: dict = {}, dict_user_hp: dict = {}, request=Request, scheduler=BackgroundScheduler):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    estimated_time, datetime_results_available = db.make_submission(dict_user_hp, user_id, chat_id)

    print(datetime_results_available)
    print(request)
    print(user_id)
    scheduler.add_job(notify_finished_trainings, 'date', run_date=datetime_results_available, args=[request, user_id])

    if estimated_time > 0:
        tel_send_message(chat_id, "📃 Your model was submitted to the training queue.")
        tel_send_message(chat_id, f"🕐 The estimated training time is {convert_seconds(estimated_time)}")
        tel_send_message(chat_id, "🛎️ You'll receive an automatic message when your training is finished.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Cancel Training", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        tel_send_message(chat_id, "😥 There was a problem submitting your model to the training queue. "
                                  "Try again in a few minutes. "
                                  "If the problem persists, notify the SIIM AI Playground organizers.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Try new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


def show_training_status(dict_msg: dict = {}, request: Request = None):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    # Loads user's submissions
    df = db.load_df_submissions(user_id)

    if len(df) == 0:
        # If there is no submission
        tel_send_message(chat_id, "🤚 You didn't submit any model to training yet.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Create new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])
    else:
        # Submission were found
        rec = df.loc[0]

        if rec.training_status in db_schema.TRAINING_STATUS_TRAINING:
            # The last submission is training

            estimated_time = calc_timestamp_diff_in_secs(str(rec.datetime_submission),
                                                         str(rec.datetime_results_available))

            time_remaining = calc_timestamp_diff_in_secs(str(datetime.datetime.now()),
                                                         str(rec.datetime_results_available))

            # checks if it is finished
            if time_remaining > 0:
                # the training session period is not over yet. the competitor has to wait
                tel_send_message(chat_id, "🏋️ *TRAINING STATUS:*\n"
                                          f"🕐 Estimated training time: {convert_seconds(estimated_time)}\n"
                                          f"🕙 Time remaining: {convert_seconds(time_remaining)}")
                tel_send_message(chat_id, "🛎️ You'll receive an automatic message when your training is finished.")
                tel_send_inlinebutton(chat_id, "Select your option:",
                                      [{"text": "Check Status", "callback_data": "show_status"},
                                       {"text": "Cancel Training", "callback_data": "new_model"},
                                       {"text": "Leaderboard", "callback_data": "show_leaderboard"}])

            else:
                # The training session is over. Notify the user and change status in the database
                notify_finished_trainings(request=request, user_id=user_id)


def show_leaderboard(dict_msg: dict = {}):
    chat_id = dict_msg.get('chat_id', '')
    user_id = dict_msg.get('user_id', '')

    df = db.get_leaderboard_df()

    df['last_submission'] = df['last_submission'].apply(calculate_time_ago)
    df['rank'] = df.index + 1

    # Look for the user_id in the dataframe
    df_user = df[df['user_id'] == user_id]

    df = df[['rank', 'fullname', 'score', 'entries', 'last_submission']]
    df.columns = ['Pos', 'Name', 'Score', 'Entries', 'Last']
    leaderboard = df.to_string(index=False)

    if not df_user.empty:
        # Find the position (index) of the first matching row and add 1 to start counting from 1
        position = int(df_user.index[0] + 1)

        # Create a series called rec of the first matching row
        row = df_user.iloc[0]

        tel_send_message(chat_id,
                         f"👏 Your are in the *{number_to_ordinal(position)}* position. Your best score is *{row.score}*")
        tel_send_message(chat_id, "🏆 *LEADERBOARD (Top 10)*")
        tel_send_message(chat_id, '```' + leaderboard + '```')
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Try new model", "callback_data": "new_model"},
                               {"text": "Leaderboard", "callback_data": "show_leaderboard"}])


    else:
        # User not found in the dataframe.
        tel_send_message(chat_id, "🏆 *LEADERBOARD*")
        tel_send_message(chat_id, f"You have not ranked yet. Create a new model or wait your model to finish training.")
        tel_send_inlinebutton(chat_id, "Select your option:",
                              [{"text": "Check Status", "callback_data": "show_status"},
                               {"text": "Create new model", "callback_data": "new_model"}])

    return


def create_dict_options(list_options):
    list_dict = []

    for option in list_options:
        text = option.split(hp.sep)[1]
        callback_data = option
        list_dict.append({"text": text, "callback_data": callback_data})

    return list_dict


def extract_dict_options(txt):
    key = ''
    value = ''

    if len(txt.split(hp.sep)) == 2:
        key = txt.split(hp.sep)[0]
        value = txt.split(hp.sep)[1]

    return key, value


def parse_user_hps(dict_user_hp: dict = {}, user_id: str = '') -> str:
    txt = ''

    for key, value in dict_user_hp.items():
        txt = '\n'.join([txt, f'{key}: {value}'])

    # Remove _ to avoid formatting issues (italic)
    txt = txt.replace('_', ' ')

    return txt


def calc_timestamp_diff_in_secs(timestamp1, timestamp2):
    # Convert the strings to datetime objects using strptime()
    # Adjust the format string if your input has a different format
    print(timestamp1, timestamp2)
    dt1 = datetime.datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S.%f")
    dt2 = datetime.datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S.%f")

    # Calculate the time difference and convert it to seconds
    time_difference = dt2 - dt1
    time_difference_seconds = int(time_difference.total_seconds())

    return time_difference_seconds


def notify_finished_trainings(request: Request, user_id: str = None):
    df = db.load_df_finished_trainings(user_id)

    list_competitors_notified = []

    for idx, row in df.iterrows():
        if row.user_id not in list_competitors_notified:
            tel_send_message(row.chat_id, "Your model training is *FINISHED*. Here are your results:\n"
                                          f"*Training set:* {row.metrics_train_set:.5f}\n"
                                          f"*Validation set:* {row.metrics_val_set:.5f}\n"
                                          f"*Test set:* {row.metrics_test_set:.5f}")

            dice, jacloss, sample = db_schema.imgs_url(0, row.epochs, row.learning_rate, row.batch_norm, row.filters,
                                                       row.dropout, row.image_size, row.batch_size)

            # rotates the sample image as they as originally they were created rotated
            sample = request.url_for("rotate_image").include_query_params(image_url=sample)

            tel_send_image(row.chat_id, dice)
            tel_send_image(row.chat_id, jacloss)
            tel_send_image(row.chat_id, sample)

            tel_send_inlinebutton(row.chat_id, "Select your option:",
                                  [{"text": "Leaderboard", "callback_data": "show_leaderboard"},
                                   {"text": "Try new model", "callback_data": "new_model"}])

            list_competitors_notified.append(row.user_id)

    db.mark_submissions_notified(list_competitors_notified)

    return len(list_competitors_notified)


def convert_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"


def calculate_time_ago(timestamp: str):
    # Parse the input timestamp string
    timestamp = str(timestamp)
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

    # Calculate the difference between now and the input timestamp
    now = datetime.datetime.now()
    time_difference = now - timestamp
    relative_difference = relativedelta(now, timestamp)

    # Check if the difference is less than one minute
    if time_difference < datetime.timedelta(minutes=1):
        return 'Now'

    # Check if the difference is more than a year
    elif relative_difference.years >= 1:
        years = relative_difference.years
        return f'{years}y'

    # Check if the difference is more than a month but less than a year
    elif relative_difference.months >= 1:
        months = relative_difference.months + relative_difference.years * 12
        return f'{months}mo'

    # Check if the difference is more than a day
    elif time_difference >= datetime.timedelta(days=1):
        days = time_difference.days
        return f'{days}d'

    # Check if the difference is more than an hour but less than a day
    elif time_difference >= datetime.timedelta(hours=1):
        hours = time_difference.seconds // 3600
        return f'{hours}h'

    # If the difference is less than a day but more than a minute
    else:
        minutes = time_difference.seconds // 60
        return f'{minutes}min'


def number_to_ordinal(n):
    if isinstance(n, (int, float)):
        n = int(n)
    else:
        raise TypeError("The input should be a number.")

    if n < 0:
        raise ValueError("The input should be a non-negative integer.")

    if n % 100 in [11, 12, 13]:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    return str(n) + suffix


def read_html_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        content = f.read()
    return content

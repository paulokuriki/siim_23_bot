import datetime
import json

import sqlalchemy
from sqlalchemy import NUMERIC
from sqlalchemy import create_engine, select, insert
from sqlalchemy import func

# import tables from the db_schema module
from db_schema import tb_pretrained, tb_competitors, tb_submissions, DATABASE_URL

# create a SQLAlchemy engine object using the DATABASE_URL
engine = create_engine(DATABASE_URL)


def insert_competitor(dict_msg: dict = {}):
    user_id = dict_msg.get('user_id', '')
    username = dict_msg.get('username', '')
    fullname = dict_msg.get('fullname', '')

    # create an insert statement for the tb_competitors table with the given username and fullname
    stmt = insert(tb_competitors).values(user_id=user_id, username=username, fullname=fullname)

    try:
        # execute the insert statement within a transaction and commit it
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
            return True

    except sqlalchemy.exc.IntegrityError as e:
        # handle the case where the insert fails due to a unique constraint violation (i.e., the username already exists)
        # and do nothing; return None
        # print the error message for debugging purposes
        pass
    except Exception as e:
        # handle all other exceptions by printing the error message and returning None
        print(e)

    return


def list_competitors(dict_msg: dict = {}):
    if dict_msg == {}:
        # create a select statement for the tb_competitors table that retrieves all rows
        sql = select(tb_competitors)
    else:
        # create a select statement for the tb_competitors table that retrieves the row(s) with the given username
        sql = select(tb_competitors).where(tb_competitors.c.user_id == dict_msg.get('user_id', ''))

    # execute the select statement within a transaction and retrieve all results
    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    # extract the first column of each result (i.e., the username) and return them in a list
    results = [tuple(row) for row in results]

    return results


def list_pretrained(dict_msg: dict = {}):
    id = dict_msg.get('id', None)
    if id:
        # create a select statement for the tb_pretrained table that retrieves the row(s) with the given id
        sql = select(tb_pretrained).where(tb_pretrained.c.id == id)
    else:
        # create a select statement for the tb_pretrained table that retrieves all rows
        sql = select(tb_pretrained)

    # execute the select statement within a transaction and retrieve all results
    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    # convert each result row into a tuple and return them in a list
    results = [tuple(row) for row in results]

    return results


def insert_json(json_record: dict):
    try:
        # execute an insert statement for the tb_pretrained table with the given JSON record within a transaction
        # and commit it
        with engine.connect() as conn:
            conn.execute(tb_pretrained.insert(), [json_record])
            conn.commit()
            return 'JSON inserted successfully.'

    except sqlalchemy.exc.IntegrityError as e:
        # handle the case where the insert fails due to a unique constraint violation and print the error message for
        # debugging purposes; return the exception object
        print(e)
        return e
    except Exception as e:
        # handle all other exceptions by printing the error message and returning None
        print(e)

    return


def return_metrics(dict_user_hp: dict = {}, user_id: str = '') -> dict:
    if dict_user_hp.get('batch_norm', '') == 'True':
        bn = True
    else:
        bn = False

    if dict_user_hp.get('dropout', '') == 'None':
        drop = 0
    else:
        drop = 0.2

    sql = select(func.avg(tb_pretrained.c.training_secs).label('avg_training_secs'),
                 func.stddev(tb_pretrained.c.training_secs).label('stddev_training_secs'),
                 func.avg(tb_pretrained.c.metrics_train_set).label('avg_metrics_train_set'),
                 func.stddev(tb_pretrained.c.metrics_train_set).label('stddev_metrics_train_set'),
                 func.avg(tb_pretrained.c.metrics_val_set).label('avg_metrics_val_set'),
                 func.stddev(tb_pretrained.c.metrics_val_set).label('stddev_metrics_val_set'),
                 func.avg(tb_pretrained.c.metrics_test_set).label('avg_metrics_test_set'),
                 func.stddev(tb_pretrained.c.metrics_test_set).label('stddev_metrics_test_set')). \
        where(tb_pretrained.c.batch_size == dict_user_hp.get('batch_size', 0),
              tb_pretrained.c.epochs == dict_user_hp.get('epochs', 0),
              tb_pretrained.c.learning_rate == dict_user_hp.get('learning_rate', 0),
              tb_pretrained.c.batch_norm == bn,
              tb_pretrained.c.filters == dict_user_hp.get('filters', 0),
              func.round(func.cast(tb_pretrained.c.dropout, NUMERIC), 2) == drop,
              tb_pretrained.c.image_size == dict_user_hp.get('image_size', 0),
              )

    print(sql.compile(compile_kwargs={"literal_binds": True}))

    # execute the select statement within a transaction and retrieve all results
    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    print(results)

    if results == [(None, None, None, None, None, None, None, None)]:
        result = [0, 0, 0, 0, 0, 0, 0, 0]
    elif len(results) == 1:
        result = results[0]
    else:
        result = [0, 0, 0, 0, 0, 0, 0, 0]

    dict_result = {
        'avg_training_secs': result[0],
        'stddev_training_secs': result[1],
        'avg_metrics_train_set': result[2],
        'stddev_metrics_train_set': result[3],
        'avg_metrics_val_set': result[4],
        'stddev_metrics_val_set': result[5],
        'avg_metrics_test_set': result[6],
        'stddev_metrics_test_set': result[7]
    }

    return dict_result


def generate_random_number(base_number, std_dev, max_percentage_from_std_dev: float = 0.03):
    import random

    rand_multiplier = random.uniform(0, max_percentage_from_std_dev)
    new_std_dev = float(std_dev) * float(rand_multiplier)

    add_or_subtract = random.randint(0, 1)
    if add_or_subtract == 0:
        random_number = float(base_number) + new_std_dev
    else:
        random_number = float(base_number) - new_std_dev

    return random_number


def save_dict(dict_user_hp: dict, user_id: str):
    filename = user_id + '.json'

    try:
        # Save the dictionary to a file
        with open(filename, "w") as file:
            json.dump(dict_user_hp, file)
    except Exception as e:
        # Handle exceptions and print an error message
        print(f"An error occurred while saving the file: {e}")


def load_dict(user_id: str):
    filename = user_id + '.json'

    try:
        # Read the dictionary from the file
        with open(filename, "r") as file:
            loaded_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if there's an error
        loaded_dict = {}

    return loaded_dict


def make_submission(dict_user_hp, user_id, random_estimated_time, random_metrics_train_set, random_metrics_val_set,
                    random_metrics_test_set):
    # create an insert statement for the tb_submissions

    now = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=random_estimated_time)
    datetime_results_available = now + time_delta

    if dict_user_hp.get('learning_rate', '') == 'True':
        lr = True
    else:
        lr = False

    stmt = insert(tb_submissions).values(
        datetime_submission=datetime.datetime.now(),
        user_id=user_id,
        batch_size=dict_user_hp.get('batch_size', 0),
        epochs=dict_user_hp.get('epochs', 0),
        learning_rate=lr,
        batch_norm=dict_user_hp.get('batch_norm', 0),
        filters=dict_user_hp.get('filters', 0),
        dropout=dict_user_hp.get('dropout', 0),
        image_size=dict_user_hp.get('image_size', 0),
        metrics_train_set=random_metrics_train_set,
        metrics_val_set=random_metrics_val_set,
        metrics_test_set=random_metrics_test_set,
        datetime_results_available=datetime_results_available,
        telegram_sent=False,
        loss_fig_url='',
        metrics_fig_url='',
        sample_figs_urls='',
        training_status='Training')

    try:
        # execute the insert statement within a transaction and commit it
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
            return True
    except Exception as e:
        print(f'Error making submission\e{e}')
        return False

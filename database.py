import sqlalchemy
from sqlalchemy import create_engine, select, insert
from sqlalchemy import func

# import tables from the db_schema module
from db_schema import tb_pretrained, tb_competitors, DATABASE_URL

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


def return_metrics(dict_users_hp: dict = {}, user_id: str = '') -> dict:
    dict_user = dict_users_hp.get(user_id, {})

    if dict_user.get('batch_norm', '') == 'True':
        bn = True
    else:
        bn = False

    sql = select(func.avg(tb_pretrained.c.training_secs).label('avg_training_secs'),
                 func.stddev(tb_pretrained.c.training_secs).label('stddev_training_secs'),
                 func.avg(tb_pretrained.c.metrics_train_set).label('avg_metrics_train_set'),
                 func.stddev(tb_pretrained.c.metrics_train_set).label('stddev_metrics_train_set'),
                 func.avg(tb_pretrained.c.metrics_val_set).label('avg_metrics_val_set'),
                 func.stddev(tb_pretrained.c.metrics_val_set).label('stddev_metrics_val_set'),
                 func.avg(tb_pretrained.c.metrics_test_set).label('avg_metrics_test_set'),
                 func.stddev(tb_pretrained.c.metrics_test_set).label('stddev_metrics_test_set')). \
        where(tb_pretrained.c.batch_size == dict_user.get('batch_size', 0),
              tb_pretrained.c.epochs == dict_user.get('epochs', 0),
              tb_pretrained.c.learning_rate == dict_user.get('learning_rate', 0),
              tb_pretrained.c.batch_norm == bn,
              tb_pretrained.c.filters == dict_user.get('filters', 0),
              tb_pretrained.c.dropout == dict_user.get('dropout', 0),
              tb_pretrained.c.image_size == dict_user.get('image_size', 0),
              )

    print(sql)

    # execute the select statement within a transaction and retrieve all results
    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    print(results)

    if len(results) == 1:
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
    }

    return dict_result


def generate_random_number_from_stddev(base_number, std_dev, max_diff: int = 3):
    import random

    rand_multiplier = random.randint(0, max_diff)
    new_std_dev = std_dev * rand_multiplier

    add_or_subtract = random.randint(0, 1)
    if add_or_subtract == 0:
        random_number = base_number + new_std_dev
    else:
        random_number = base_number - new_std_dev

    return random_number

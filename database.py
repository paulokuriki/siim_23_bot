import sqlalchemy
from sqlalchemy import create_engine, select, insert

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

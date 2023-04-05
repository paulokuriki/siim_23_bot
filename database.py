import os

import sqlalchemy
from sqlalchemy import create_engine, select, insert

# import tables from the db_schema module
from db_schema import tb_pretrained, tb_competitors

# get the database URL from an environment variable or use a default value
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

# create a SQLAlchemy engine object using the DATABASE_URL
engine = create_engine(DATABASE_URL)


def insert_competitor(username: str = '', fullname: str = ''):
    # create an insert statement for the tb_competitors table with the given username and fullname
    stmt = insert(tb_competitors).values(username=username, fullname=fullname)

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


def list_competitors(username: str = ''):
    if username:
        # create a select statement for the tb_competitors table that retrieves the row(s) with the given username
        sql = select(tb_competitors).where(tb_competitors.c.username == username)
    else:
        # create a select statement for the tb_competitors table that retrieves all rows
        sql = select(tb_competitors)

    # execute the select statement within a transaction and retrieve all results
    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    # extract the first column of each result (i.e., the username) and return them in a list
    results = [r[0] for r in results]

    return results


def list_pretrained(id: str = None):
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

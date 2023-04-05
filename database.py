import os
import json

import sqlalchemy
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session

from db_schema import tb_pretrained, tb_competitors

DATABASE_URL = os.environ.get('DATABASE_URL', '')

engine = create_engine(DATABASE_URL)


def insert_competitor(username: str = '', fullname: str = ''):
    stmt = insert(tb_competitors).values(username=username, fullname=fullname)

    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
            return True

    except sqlalchemy.exc.IntegrityError as e:
        # (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "users_pkey"
        # DETAIL:  Key (username) already exists.
        pass
    except Exception as e:
        print(e)

    return


def list_competitors(username: str = ''):
    if username:
        sql = select(tb_competitors).where(tb_competitors.c.username == username)
    else:
        sql = select(tb_competitors)

    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    results = [r[0] for r in results]

    return results


def list_pretrained(id: str = None):
    if id:
        sql = select(tb_pretrained).where(tb_pretrained.c.id == id)
    else:
        sql = select(tb_pretrained)

    with engine.connect() as conn:
        results = conn.execute(sql).fetchall()

    results = [tuple(row) for row in results]

    return results


def insert_json(json_record: dict):
    try:
        with engine.connect() as conn:
            conn.execute(tb_pretrained.insert(), [json_record])
            conn.commit()
            return 'JSON inserted successfully.'

    except sqlalchemy.exc.IntegrityError as e:
        # (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "users_pkey"
        # DETAIL:  Key (username) already exists.
        print(e)
        return e
    except Exception as e:
        print(e)

    return
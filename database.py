import os
from sqlalchemy import create_engine,  select, text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import DateTime as TimeStamp, SmallInteger as smallint, Text as text, REAL as real, BOOLEAN as boolean

metadata_obj = MetaData()

competitors = Table("competitors", metadata_obj,
                    Column("id", text, primary_key=True),
                    Column("username", text))

pretrained = Table("pretrained_results", metadata_obj,
                   Column("id", smallint, primary_key=True),
                   Column("timestamp", TimeStamp),
                   Column("trainer", text),
                   Column("gpu", text),
                   Column("training_secs", smallint),
                   Column("model_name", text),
                   Column("batch_size", smallint),
                   Column("epochs", smallint),
                   Column("learning_rate", real),
                   Column("batch_norm", boolean),
                   Column("filters", smallint),
                   Column("dropout", real),
                   Column("image_size", smallint),
                   Column("metrics_train_set", real),
                   Column("metrics_val_set", real),
                   Column("metrics_test_set", real))


DATABASE_URL = os.environ.get('DATABASE_URL', '')

engine = create_engine(DATABASE_URL)
conn = engine.connect()

def list_usernames(id: str = None):

    if id:
        sql = select(competitors.c.id).where(competitors.c.id == id)
    else:
        sql = select(competitors.c.id)

    results = conn.execute(sql) .fetchall()
    results = [r[0] for r in results]

    return results


def list_pretrained(id: str = None):
    if id:
        sql = select(pretrained).where(pretrained.c.id == id)
    else:
        sql = select(pretrained)

    results = conn.execute(sql).fetchall()

    return results

print('\n'.join(list_usernames()))

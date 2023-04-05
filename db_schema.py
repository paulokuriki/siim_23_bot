from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import DateTime as TimeStamp, SmallInteger as smallint, Text as text, REAL as real, BOOLEAN as boolean

metadata_obj = MetaData()

tb_competitors = Table("competitors", metadata_obj,
                       Column("username", text, primary_key=True),
                       Column("fullname", text))

tb_pretrained = Table("pretrained_results", metadata_obj,
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

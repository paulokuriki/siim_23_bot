import os

from sqlalchemy import DateTime as TimeStamp, SmallInteger as smallint, Text as text, REAL as real, BOOLEAN as boolean
from sqlalchemy import Table, Column
from sqlalchemy import create_engine, MetaData, ForeignKey

# get the database URL from an environment variable or use a default value
# The URI should start with postgresql:// instead of postgres://. SQLAlchemy used to accept both, but has removed support for the postgres name.
DATABASE_URL = os.environ.get('DATABASE_URL',
                              'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres').replace("postgres://",
                                                                                                         "postgresql://")

# create a SQLAlchemy engine object using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# create a SQLAlchemy metadata object
metadata_obj = MetaData()

# create a SQLAlchemy Table object for the competitors table with columns for the username and fullname
tb_competitors = Table("competitors", metadata_obj,
                       Column("user_id", text, primary_key=True),
                       Column("username", text),
                       Column("fullname", text))

# create a SQLAlchemy Table object for the pretrained_results table with columns for various model training parameters
# and performance metrics, as well as URLs for figures generated during training and the ID of who trained the model
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
                      Column("metrics_test_set", real),
                      Column("loss_fig_url", text),
                      Column("metrics_fig_url", text),
                      Column("sample_figs_urls", text),
                      )

# create a SQLAlchemy Table object for the submissions table with columns for various model training parameters
# and performance metrics, as well as URLs for figures generated during training and the ID of the competitor who
# submitted the model, as well as a datetime column indicating when the results of the model are available and a
# boolean column indicating whether a Telegram message has been sent to the competitor indicating the availability of
# the results
tb_submissions = Table("submissions", metadata_obj,
                       Column("id", smallint, primary_key=True),
                       Column("datetime_submission", TimeStamp),
                       Column("user_id", text, ForeignKey("competitors.user_id"), nullable=False),
                       Column("batch_size", smallint),
                       Column("epochs", smallint),
                       Column("learning_rate", real),
                       Column("batch_norm", boolean),
                       Column("filters", smallint),
                       Column("dropout", real),
                       Column("image_size", smallint),
                       Column("metrics_train_set", real),
                       Column("metrics_val_set", real),
                       Column("metrics_test_set", real),
                       Column("datetime_results_available", TimeStamp),
                       Column("telegram_sent", boolean),
                       Column("loss_fig_url", text),
                       Column("metrics_fig_url", text),
                       Column("sample_figs_urls", text),
                       Column("training_status", text),
                       )

# creates the tables in case they don't exist
metadata_obj.create_all(engine)

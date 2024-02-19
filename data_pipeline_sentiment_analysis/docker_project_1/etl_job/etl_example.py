"""
Example file to simulate an ETL process within a docker pipeline
- Extracts from a mongo db
- Transforms the collections
- Loads the transformed collections to postgres db

To be started by docker (see ../docker-compose.yml)

For inspecting that ETL worked out: docker exec -it pipeline_example_my_postgres_1 psql
"""


import pymongo
import sqlalchemy  # use a version prior to 2.0.0 or adjust creating the engine and df.to_sql()
import psycopg2
import time
import logging
import pandas


# mongo db definitions
client = pymongo.MongoClient(
    "mongodb", port=27017
)  # my_mongo is the hostname (= service in yml file)
db = client.reddit  # change this to what your mongodb database is called
coll = db.my_collection  # change this to whatever your collection in that db is called


# postgres db definitions. HEADS UP: outsource these credentials and don't push to github.
USERNAME_PG = "postgres"
PASSWORD_PG = "postgres"
HOST_PG = "my_postgres"  # my_postgres is the hostname (= service in yml file)
PORT_PG = 5432
DATABASE_NAME_PG = "reddits_pgdb"

conn_string_pg = (
    f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"
)
time.sleep(3)  # safety margine to ensure running postgres server
pg = sqlalchemy.create_engine(conn_string_pg)
pg_connect = pg.connect()


# Create the table
create_table_string = sqlalchemy.text(
    """CREATE TABLE IF NOT EXISTS reddits (
                                         time TEXT,
                                         reddit TEXT,
                                         sentiment NUMERIC
                                         );
                                      """
)

pg_connect.execute(create_table_string)
pg_connect.commit()


def extract(limit=5):
    # We are loading only the last 5 entries for speed/debugging
    extracted_reddits = list(coll.find(limit=limit))
    logging.critical(f"\n---- {limit} reddits extracted ----\n")
    return extracted_reddits


def regex_clean(reddit):
    # placeholder function for removing things from your reddit text, e.g. links
    pass


def sentiment_analysis(text):
    # placeholder for real sentiment analysis function
    return 1


def transform(extracted_reddits):
    transformed_reddits = []
    for post in extracted_reddits:
        # optional just to see what is going on:
        logging.critical(f"{post}")

        # here we select the 'text' key from the dictoinary
        text = post["text"]

        # ... clean it using the regex cleaning function (which currently does nothing)
        text = regex_clean(text)

        # ...perform sentiment analysis (currently returns 1 for all text - yours will be different)
        sentiment = sentiment_analysis(text)

        # ... add a field to the post dictionary called "sentiment" that contains this value
        post["sentiment"] = sentiment

        # ... and finally append the post to our list of transformed reddits
        transformed_reddits.append(post)

        # can also optionally add a logging statement
        # (-think about if you want this inside or outside the for-loop)
        logging.critical("\n---- new reddit post successfully transformed ----\n")

    return transformed_reddits


def load(transformed_reddits):
    pg_connect = pg.connect()
    for post in transformed_reddits:
        insert_query = sqlalchemy.text(
            """
            INSERT INTO reddits (time, reddit, sentiment) 
            VALUES (:time, :text, :sentiment) ON CONFLICT DO NOTHING;
            """
        )
        pg_connect.execute(
            insert_query,
            {
                "time": post["date"],
                "text": post["text"],
                "sentiment": post["sentiment"],
            },
        )
        pg_connect.commit()
        logging.critical(
            f"New reddit post incoming: {post['text']} with sentiment score {post['sentiment']}"
        )
        logging.critical("\n---- new reddit post loaded to postgres db ----\n")
    return None


if __name__ == "__main__":
    extracted_reddits = extract()
    transformed_reddits = transform(extracted_reddits)
    load(transformed_reddits)
    # new_query = sqlalchemy.text(
    #         """
    #         INSERT INTO reddits (time, reddit, sentiment) 
    #         VALUES ('2021-01-01', 'xxx', 1) ON CONFLICT DO NOTHING;
    #         """
    #     )
    # pg_connect.execute(new_query)
    # pg_connect.commit()
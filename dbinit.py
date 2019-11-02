import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (42)",
]


def initialize(url):
    print ("test debug")
    print("test debug muhammed")
    with dbapi2.connect(url , sslmode='require') as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://lwgysxzadqznqz:1d99ac08fda0c54c8e686f0057d88e65b9171c5bc3684551980e9b75ace378b9@ec2-54-217-235-87.eu-west-1.compute.amazonaws.com:5432/dfpj1pes2t0cba"
    if url is None:
        print("Usage: DATABASE_URL=url python dbtest.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
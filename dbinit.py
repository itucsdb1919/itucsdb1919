import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
    CREATE TABLE "Brand" (
      "brand_name" text PRIMARY KEY,
      "web_site" text,
      "logo_url" text,
      "year_founded" int,
      "segment" text,
      "net_worth" float,
      "country" text,
      "city" text
    );

    CREATE TABLE "Model" (
      "model_id" SERIAL PRIMARY KEY,
      "model_name" text,
      "year" int,
      "bike_type" text,
      "frame_material" text,
      "target_customer" text,
      "brand" text,
      "country" text
    );
    
    CREATE TABLE "Parts" (
      "parts_id" SERIAL PRIMARY KEY,
      "gidon" text,
      "aktarici" text,
      "sele" text,
      "jant" text,
      "lastik" text,
      "pedal" text
    );
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)

import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS "Brand" (
      "brand_name" text PRIMARY KEY,
      "web_site" text,
      "logo_url" text,
      "year_founded" int,
      "segment" text,
      "net_worth" float,
      "country" text,
      "city" text
    );

    CREATE TABLE IF NOT EXISTS "Model" (
      "model_id" SERIAL PRIMARY KEY,
      "model_name" text,
      "year" int,
      "bike_type" text,
      "frame_material" text,
      "target_customer" text,
      "brand" text,
      "country" text
    );
    
    CREATE TABLE IF NOT EXISTS "Parts" (
      "parts_id" SERIAL PRIMARY KEY,
      "gidon" text,
      "aktarici" text,
      "sele" text,
      "jant" text,
      "lastik" text,
      "pedal" text
    );

      CREATE TABLE IF NOT EXISTS Contact (
    contact_id SERIAL PRIMARY KEY,
    phone_num char(10),
    e_mail text,
    is_active boolean,
    instagram_url text,
    facebook_url text,
    twitter_url text,
    country text,
    profil int,
    city text
  );

  CREATE TABLE IF NOT EXISTS SupportTickets (
    support_tickets_id SERIAL PRIMARY KEY,
    writer_nickname text,
    writen_date timestamp,
    support_text text,
    topic text,
    satisfaction_score int,
    is_answered boolean,
    support_worker_id int
  );

  CREATE TABLE IF NOT EXISTS City (
    city_name text PRIMARY KEY,
    rank_between_cities int,
    overallscore int,
    number_of_user int,
    number_of_bikes int,
    country text
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

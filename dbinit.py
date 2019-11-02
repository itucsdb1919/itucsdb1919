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

    CREATE TABLE IF NOT EXISTS "Contact" (
    contact_id SERIAL PRIMARY KEY,
    phone_num char(10) UNIQUE,
    e_mail text,
    is_active boolean,
    instagram_url text,
    facebook_url text,
    twitter_url text,
    country text,
    profil int,
    city text
  );

  CREATE TABLE IF NOT EXISTS "SupportTickets" (
    support_tickets_id SERIAL PRIMARY KEY,
    writer_nickname text,
    writen_date timestamp,
    support_text text,
    topic text,
    satisfaction_score int,
    is_answered boolean,
    support_worker_id int
  );

  CREATE TABLE IF NOT EXISTS "City" (
    city_name text PRIMARY KEY,
    rank_between_cities int,
    overallscore int,
    number_of_user int,
    number_of_bikes int,
    country text
  );
  CREATE TABLE IF NOT EXISTS "Country" (
    country_name text PRIMARY KEY,
    rank_between_countries int,
    overallscore int,
    number_of_bikes int,
    number_of_user int,
    total_money_spent int,
    number_of_cities int
  );

  CREATE TABLE IF NOT EXISTS "Bikes" (
    bike_id SERIAL PRIMARY KEY,
    title text,
    color text,
    frame_size int,
    price float,
    is_active boolean,
    parts_id int,
    owner_nickname text,
    city text,
    country text,
    model_id int
  );

  CREATE TABLE IF NOT EXISTS "SupportWorker" (
    support_worker_id SERIAL PRIMARY KEY,
    worker_name text,
    worker_surname text,
    working_status text,
    scorepoints int,
    average_respond_time float,
    contact int
  );

  CREATE TABLE IF NOT EXISTS "Profil" (
  "profil_id" int PRIMARY KEY,
  "name" text,
  "surname" text,
  "profil_nickname" text UNIQUE,
  "profil_image" text,
  "number_of_bikes" int,
  "number_of_deals" int,
  "comments" int,
  "contact" int
);

CREATE TABLE IF NOT EXISTS "Deals" (
  "deal_id" int PRIMARY KEY,
  "price" float,
  "payment_method" text,
  "date_taken" timestamp,
  "date_return" timestamp,
  "duration_as_hour" int,
  "is_active" boolean,
  "owner_nickname" text,
  "renter_nickname" text,
  "owner_phone" int,
  "renter_phone" int,
  "bike_id" int,
  "city" text,
  "Country" text
);

CREATE TABLE IF NOT EXISTS "Comments" (
  "comment_id" SERIAL PRIMARY KEY,
  "comment" text,
  "title" text,
  "image_url" text,
  "writen_date" timestamp,
  "up_vote" int,
  "down_vote" int,
  "writer_nickname" text,
  "bike_id" int
);

CREATE TABLE "Bike_Comment" (
  "bike_id" int,
  "comment_id" int,
  PRIMARY KEY ("bike_id", "comment_id")
);

CREATE TABLE "Bike_images" (
  "bike_id" int PRIMARY KEY,
  "image_url" text
);

ALTER TABLE "Contact" ADD FOREIGN KEY ("country") REFERENCES "Country" ("country_name");

ALTER TABLE "Contact" ADD FOREIGN KEY ("profil") REFERENCES "Profil" ("profil_id");

ALTER TABLE "Contact" ADD FOREIGN KEY ("city") REFERENCES "City" ("city_name");

ALTER TABLE "Brand" ADD FOREIGN KEY ("country") REFERENCES "Country" ("country_name");

ALTER TABLE "Brand" ADD FOREIGN KEY ("city") REFERENCES "City" ("city_name");

ALTER TABLE "Model" ADD FOREIGN KEY ("brand") REFERENCES "Brand" ("brand_name");

ALTER TABLE "Model" ADD FOREIGN KEY ("country") REFERENCES "Country" ("country_name");

ALTER TABLE "City" ADD FOREIGN KEY ("country") REFERENCES "Country" ("country_name");

ALTER TABLE "Bikes" ADD FOREIGN KEY ("parts_id") REFERENCES "Parts" ("parts_id");

ALTER TABLE "Bikes" ADD FOREIGN KEY ("owner_nickname") REFERENCES "Profil" ("profil_nickname");

ALTER TABLE "Bikes" ADD FOREIGN KEY ("city") REFERENCES "City" ("city_name");

ALTER TABLE "Bikes" ADD FOREIGN KEY ("country") REFERENCES "Country" ("country_name");

ALTER TABLE "Bikes" ADD FOREIGN KEY ("model_id") REFERENCES "Model" ("model_id");

ALTER TABLE "Bike_Comment" ADD FOREIGN KEY ("bike_id") REFERENCES "Bikes" ("bike_id");

ALTER TABLE "Bike_Comment" ADD FOREIGN KEY ("comment_id") REFERENCES "Comments" ("comment_id");

ALTER TABLE "Bike_images" ADD FOREIGN KEY ("bike_id") REFERENCES "Bikes" ("bike_id");

ALTER TABLE "Comments" ADD FOREIGN KEY ("writer_nickname") REFERENCES "Profil" ("profil_nickname");

ALTER TABLE "Comments" ADD FOREIGN KEY ("bike_id") REFERENCES "Bikes" ("bike_id");

ALTER TABLE "SupportTickets" ADD FOREIGN KEY ("writer_nickname") REFERENCES "Profil" ("profil_nickname");

ALTER TABLE "SupportTickets" ADD FOREIGN KEY ("support_worker_id") REFERENCES "SupportWorker" ("support_worker_id");

ALTER TABLE "SupportWorker" ADD FOREIGN KEY ("contact") REFERENCES "Contact" ("contact_id");

ALTER TABLE "Profil" ADD FOREIGN KEY ("comments") REFERENCES "Comments" ("comment_id");

ALTER TABLE "Profil" ADD FOREIGN KEY ("contact") REFERENCES "Contact" ("contact_id");

ALTER TABLE "Deals" ADD FOREIGN KEY ("owner_nickname") REFERENCES "Profil" ("profil_nickname");

ALTER TABLE "Deals" ADD FOREIGN KEY ("renter_nickname") REFERENCES "Profil" ("profil_nickname");

ALTER TABLE "Deals" ADD FOREIGN KEY ("owner_phone") REFERENCES "Contact" ("phone_num");

ALTER TABLE "Deals" ADD FOREIGN KEY ("renter_phone") REFERENCES "Contact" ("phone_num");

ALTER TABLE "Deals" ADD FOREIGN KEY ("bike_id") REFERENCES "Bikes" ("bike_id");

ALTER TABLE "Deals" ADD FOREIGN KEY ("city") REFERENCES "City" ("city_name");

ALTER TABLE "Deals" ADD FOREIGN KEY ("Country") REFERENCES "Country" ("country_name");

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

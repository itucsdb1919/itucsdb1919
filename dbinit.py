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
ALTER TABLE "Bikes" ADD FOREIGN KEY ("model") REFERENCES "Model" ("model_id");
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

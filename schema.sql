CREATE TABLE "Music"."Podcasts"
(
    uid serial,
    name text NOT NULL,
    url text NOT NULL,
    amount integer NOT NULL,
    folder_name text NOT NULL,
    "offset" integer NOT NULL,
    from_start boolean NOT NULL,
    last_updated date NOT NULL,
    PRIMARY KEY (uid)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE "Music"."Podcasts"
    OWNER to hrs;
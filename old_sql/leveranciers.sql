--
-- File generated with SQLiteStudio v3.3.3 on Thu Nov 10 20:43:44 2022
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: leveranciers
DROP TABLE IF EXISTS leveranciers;

CREATE TABLE leveranciers (
    leverancier STRING,
    kind        STRING (2),
    fromdate    STRING (10),
    price       DOUBLE,
    country     STRING (10),
    PRIMARY KEY (
        leverancier,
        kind,
        fromdate,
        country
    )
);

INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Budget energie', 'e', '2022-11-10', 1.364, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Budget energie', 'g', '2022-11-10', 4.257, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Coolblue energie', 'e', '2022-11-10', 0.765, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Coolblue energie', 'g', '2022-11-10', 2.943, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Delta energie', 'e', '2022-11-10', 0.567, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Delta energie', 'g', '2022-11-10', 2.463, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Eneco', 'e', '2022-11-10', 0.958, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Eneco', 'g', '2022-11-10', 4.63, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Energiedirect.nl', 'e', '2022-11-10', 0.667, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Energiedirect.nl', 'g', '2022-11-10', 2.714, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Engie', 'e', '2022-11-10', 0.693, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Engie', 'g', '2022-11-10', 2.733, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Essent', 'e', '2022-11-10', 0.734, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Essent', 'g', '2022-11-10', 2.719, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Gewoon energie', 'e', '2022-11-10', 0.768, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Gewoon energie', 'g', '2022-11-10', 2.693, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Greenchoice', 'e', '2022-11-10', 0.89, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Greenchoice', 'g', '2022-11-10', 3.441, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Innova energie', 'e', '2022-11-10', 0.768, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Innova energie', 'g', '2022-11-10', 2.693, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Mega energie', 'e', '2022-11-10', 0.685, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Mega energie', 'g', '2022-11-10', 2.66, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('OM | Nieuwe energie', 'e', '2022-11-10', 0.555, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('OM | Nieuwe energie', 'g', '2022-11-10', 2.504, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Oxxio', 'e', '2022-11-10', 0.958, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Oxxio', 'g', '2022-11-10', 4.63, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Powerpeers', 'e', '2022-11-10', 0.713, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Powerpeers', 'g', '2022-11-10', 3.374, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Pure energie', 'e', '2022-11-10', 0.882, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Pure energie', 'g', '2022-11-10', 3.874, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Shell Energy', 'e', '2022-11-10', 0.651, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Shell Energy', 'g', '2022-11-10', 2.503, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vandebron', 'e', '2022-11-10', 0.829, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vandebron', 'g', '2022-11-10', 3.332, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vattenfall', 'e', '2022-11-10', 0.695, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vattenfall', 'g', '2022-11-10', 2.817, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vrijopnaam', 'e', '2022-11-10', 0.783, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('Vrijopnaam', 'g', '2022-11-10', 3.482, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('United Consumers', 'e', '2022-11-10', 0.879, 'NL');
INSERT INTO leveranciers (leverancier, kind, fromdate, price, country) VALUES ('United Consumers', 'g', '2022-11-10', 2.302, 'NL');

-- Index: sqlite_autoindex_leveranciers_1
DROP INDEX IF EXISTS sqlite_autoindex_leveranciers_1;

CREATE INDEX sqlite_autoindex_leveranciers_1 ON leveranciers (
    leverancier COLLATE BINARY,
    kind COLLATE BINARY,
    fromdate COLLATE BINARY,
    country COLLATE BINARY
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

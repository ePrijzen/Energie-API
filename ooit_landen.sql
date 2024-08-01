--
-- File generated with SQLiteStudio v3.3.3 on wo aug. 24 19:53:08 2022
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: countries
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    country_id  VARCHAR (6)  PRIMARY KEY,
    country_iso VARCHAR (2),
    country     VARCHAR (20)
);

INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_50HZ', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('AL', 'AL', 'Albanië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_AMPRION', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('AT', 'AT', 'Oostenrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('BE', 'BE', 'België');
INSERT INTO countries (country_id, country_iso, country) VALUES ('BA', 'BA', 'Bosnië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('BG', 'BG', 'Bulgarije');
INSERT INTO countries (country_id, country_iso, country) VALUES ('HR', 'HR', 'Kroatië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('CY', 'CY', 'Cyprus');
INSERT INTO countries (country_id, country_iso, country) VALUES ('CZ', 'CK', 'Tsjechië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('CZ_DE_SK', 'CK', 'Tsjechië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_AT_LU', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_LU', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DK', 'DK', 'Denemarken');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DK_1', 'DK', 'Denemarken');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DK_2', 'DK', 'Denemarken');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DK_CA', 'DK', 'Denemarken');
INSERT INTO countries (country_id, country_iso, country) VALUES ('EE', 'EE', 'Estland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('FI', 'FI', 'Finland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('MK', 'MK', 'Macedonië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('FR', 'FR', 'Frankrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GR', 'GR', 'Griekenland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('HU', 'HU', 'Hongarije');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IS', 'IS', 'IJsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IE_SEM', 'IE', 'Ierland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IE', 'IE', 'Ierland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_SACO_AC', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_CALA', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_SACO_DC', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_BRNN', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_CNOR', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_CSUD', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_FOGN', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_GR', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_MACRO_NORTH', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_MACRO_SOUTH', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_MALTA', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_NORD', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_NORD_AT', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_NORD_CH', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_NORD_FR', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_NORD_SI', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_PRGP', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_ROSN', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_SARD', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_SICI', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('IT_SUD', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('RU_KGD', 'IT', 'Italië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('LV', 'LV', 'Letland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('LT', 'LT', 'Litouwen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('LU', 'LU', 'Luxenburg');
INSERT INTO countries (country_id, country_iso, country) VALUES ('MT', 'MT', 'Malta');
INSERT INTO countries (country_id, country_iso, country) VALUES ('ME', 'ME', 'Montenegro');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GB', 'UK', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GB_IFA', 'UK', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GB_IFA2', 'UK', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GB_ELECLINK', 'UK', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('UK', 'UK', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NL', 'NL', 'Nederland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_1', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_2', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_2_NSL', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_3', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_4', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO_5', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('NO', 'NO', 'Noorwegen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('PL_CZ', 'PL', 'Polen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('PL', 'PL', 'Polen');
INSERT INTO countries (country_id, country_iso, country) VALUES ('PT', 'PT', 'Portugal');
INSERT INTO countries (country_id, country_iso, country) VALUES ('MD', 'MD', 'Moldavië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('RO', 'RO', 'Roemenië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SE_1', 'SE', 'Zweden');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SE_2', 'SE', 'Zweden');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SE_3', 'SE', 'Zweden');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SE_4', 'SE', 'Zweden');
INSERT INTO countries (country_id, country_iso, country) VALUES ('RS', 'RS', 'Servië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SK', 'SK', 'Slowakije');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SI', 'SI', 'Slovenië');
INSERT INTO countries (country_id, country_iso, country) VALUES ('GB_NIR', 'GB', 'Verenigd Koninkrijk');
INSERT INTO countries (country_id, country_iso, country) VALUES ('ES', 'ES', 'Spanje');
INSERT INTO countries (country_id, country_iso, country) VALUES ('SE', 'SE', 'Zweden');
INSERT INTO countries (country_id, country_iso, country) VALUES ('CH', 'CH', 'Zwitserland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_TENNET', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('DE_TRANSNET', 'DE', 'Duitsland');
INSERT INTO countries (country_id, country_iso, country) VALUES ('TR', 'TR', 'Turkije');
INSERT INTO countries (country_id, country_iso, country) VALUES ('UA', 'UA', 'Oekraïne');
INSERT INTO countries (country_id, country_iso, country) VALUES ('UA_DOBTPP', 'UA', 'Oekraïne');
INSERT INTO countries (country_id, country_iso, country) VALUES ('UA_BEI', 'UA', 'Oekraïne');
INSERT INTO countries (country_id, country_iso, country) VALUES ('UA_IPS', 'UA', 'Oekraïne');
INSERT INTO countries (country_id, country_iso, country) VALUES ('XK', 'XK', 'Kosovo');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

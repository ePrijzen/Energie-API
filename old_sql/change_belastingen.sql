--
-- File generated with SQLiteStudio v3.3.3 on Sun Oct 30 10:48:21 2022
--
-- Text encoding used: UTF-8
--

-- Table: belasting_regels
DROP TABLE IF EXISTS belasting_regels;

CREATE TABLE belasting_regels (
    kind       VARCHAR (1),
    btw        DOUBLE,
    opslag     DOUBLE,
    ode        DOUBLE,
    eb         DOUBLE,
    start_date VARCHAR (10),
    end_date   VARCHAR (10),
    PRIMARY KEY (
        kind,
        start_date
    )
);

INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.0023, 0.1862, '2013-01-01', '2013-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.0046, 0.1894, '2014-01-01', '2014-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.0074, 0.1911, '2015-01-01', '2015-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.0113, 0.25168, '2016-01-01', '2016-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.01590082644628, 0.25243801652893, '2017-01-01', '2017-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.02850413223141, 0.26000826446281, '2018-01-01', '2018-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.05239669421488, 0.29313223140496, '2019-01-01', '2019-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.0775041322314, 0.33306611570248, '2020-01-01', '2020-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.08, 0.08509917355372, 0.34856198347107, '2021-01-01', '2021-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0011, 0.1165, '2013-01-01', '2013-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0023, 0.1185, '2014-01-01', '2014-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0036, 0.1196, '2015-01-01', '2015-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0056, 0.1007, '2016-01-01', '2016-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0074, 0.1013, '2017-01-01', '2017-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0132, 0.10458, '2018-01-01', '2018-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0189, 0.09863, '2019-01-01', '2019-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0273, 0.0977, '2020-01-01', '2020-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.03, 0.09428, '2021-01-01', '2021-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.014, 0.0305, 0.03679, '2022-01-01', '2022-06-30');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 9.0, 0.014, 0.0305, 0.03679, '2022-07-01', '2022-08-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 9.0, 0.021, 0.0305, 0.03679, '2022-09-01', '2022-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.0135, 0.08650413223141, 0.36322314049587, '2022-01-01', '2022-06-30');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 9.0, 0.0135, 0.08650413223141, 0.36322314049587, '2022-07-01', '2022-08-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 9.0, 0.04798, 0.08650413223141, 0.36322314049587, '2022-09-01', '2022-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.0175, 0.0, 0.1260 , '2023-01-01', '2023-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.0683, 0.0, 0.4898, '2023-01-01', '2023-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('g', 21.0, 0.06838842975, 0.0, 0.5829752066, '2024-01-01', '2024-12-31');
INSERT INTO belasting_regels (kind, btw, opslag, ode, eb, start_date, end_date) VALUES ('e', 21.0, 0.01750413223, 0.0, 0.1088429752, '2024-01-01', '2024-12-31');

DROP TABLE IF EXISTS belastingen;

CREATE TABLE belastingen (
    kind   VARCHAR (1),
    datum  VARCHAR (10),
    btw    INTEGER,
    opslag DOUBLE,
    eb     DOUBLE,
    ode    DOUBLE,
    primary key (kind, datum)
);

DROP TABLE IF EXISTS dates;

create table dates as
with cte as (
      select date('2013-01-01') as dte union all
      select date(dte, '+1 day')
      from cte
      where dte < '2030-12-31'
     )
select *
from cte;

INSERT INTO belastingen
(datum,kind,btw,ode,eb,opslag)
SELECT dates.dte, br.kind, br.btw, br.ode, br.eb, br.opslag
FROM dates
LEFT JOIN belasting_regels as br
WHERE br.kind = "g"
AND dates.dte BETWEEN br.start_date AND br.end_date;

INSERT INTO belastingen
(datum,kind,btw,ode,eb,opslag)
SELECT dates.dte, br.kind, br.btw, br.ode, br.eb, br.opslag
FROM dates
LEFT JOIN belasting_regels as br
WHERE br.kind = "e"
AND dates.dte BETWEEN br.start_date AND br.end_date;
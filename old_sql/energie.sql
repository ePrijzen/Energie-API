PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM energy;

DROP TABLE energy;

CREATE TABLE energy (
    fromdate VARCHAR (10) NOT NULL,
    fromtime VARCHAR (5)  NOT NULL,
    kind     VARCHAR (10) NOT NULL,
    price    DOUBLE       NOT NULL,
    country  VARCHAR (3)  DEFAULT NL,
    btw      INTEGER (2),
    ode      DOUBLE,
    eb       DOUBLE,
    opslag   DOUBLE,
    PRIMARY KEY (
        fromdate,
        fromtime,
        kind,
        country
    )
);

INSERT INTO energy (
                       fromdate,
                       fromtime,
                       kind,
                       price,
                       country
                   )
                   SELECT fromdate,
                          fromtime,
                          kind,
                          price,
                          country
                     FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;


UPDATE energy
SET btw = (SELECT b.btw
             FROM belastingen as b
             WHERE b.kind = energy.kind
             AND energy.fromdate between b.start_date and b.end_date) 
WHERE EXISTS (SELECT b.btw
              FROM belastingen as b
              WHERE b.kind = energy.kind
              AND energy.fromdate between b.start_date and b.end_date);
              

UPDATE energy
SET eb = (SELECT b.eb
             FROM belastingen as b
             WHERE b.kind = energy.kind
             AND energy.fromdate between b.start_date and b.end_date) 
WHERE EXISTS (SELECT b.eb
              FROM belastingen as b
              WHERE b.kind = energy.kind
              AND energy.fromdate between b.start_date and b.end_date);
              
UPDATE energy
SET ode = (SELECT b.ode
             FROM belastingen as b
             WHERE b.kind = energy.kind
             AND energy.fromdate between b.start_date and b.end_date) 
WHERE EXISTS (SELECT b.ode
              FROM belastingen as b
              WHERE b.kind = energy.kind
              AND energy.fromdate between b.start_date and b.end_date);
              
UPDATE energy
SET opslag = (SELECT b.opslag
             FROM belastingen as b
             WHERE b.kind = energy.kind
             AND energy.fromdate between b.start_date and b.end_date) 
WHERE EXISTS (SELECT b.opslag
              FROM belastingen as b
              WHERE b.kind = energy.kind
              AND energy.fromdate between b.start_date and b.end_date);
              
SELECT e.fromdate, e.fromtime, e.kind, e.price, e.country, b.btw, b.opslag, b.ode, b.eb 
FROM energy as e
LEFT JOIN belastingen as b
WHERE b.kind = e.kind
AND e.fromdate between b.start_date and b.end_date;
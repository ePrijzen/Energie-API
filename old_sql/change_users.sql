PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM users;

DROP TABLE users;

CREATE TABLE users (
    user_id           INTEGER     PRIMARY KEY,
    datetime          INTEGER,
    kaal_opslag_allin CHAR        DEFAULT ('k'),
    ochtend           INTEGER     DEFAULT (8),
    middag            INTEGER     DEFAULT (16),
    opslag_electra    DOUBLE,
    opslag_gas        DOUBLE,
    melding_lager_dan DOUBLE      DEFAULT (0.001),
    ode_gas           DOUBLE,
    ode_electra       DOUBLE,
    eb_electra        DOUBLE,
    eb_gas            DOUBLE,
    country           VARCHAR (5) DEFAULT ('NL'),
    locale            CHAR (5)    DEFAULT ('de_DE')
);

INSERT INTO users (
                      user_id,
                      datetime,
                      kaal_opslag_allin,
                      ochtend,
                      middag,
                      opslag_electra,
                      opslag_gas,
                      melding_lager_dan,
                      ode_gas,
                      ode_electra,
                      eb_electra,
                      eb_gas,
                      country
                  )
                  SELECT user_id,
                         datetime,
                         kaal_opslag_allin,
                         ochtend,
                         middag,
                         opslag_electra,
                         opslag_gas,
                         melding_lager_dan,
                         ode_gas,
                         ode_electra,
                         eb_electra,
                         eb_gas,
                         country
                    FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

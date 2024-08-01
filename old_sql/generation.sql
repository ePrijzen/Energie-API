create table
  `generation` (
    `fromdate` varchar(10) null,
    `fromtime` varchar(5) null,
    `mw` int null,
    `kind` varchar(10) null,
    `country` varchar(3) null default NL,
    primary key (`fromdate`, `fromtime`, `kind`, `country`)
  )
;

DELETE FROM `countries` WHERE `country_id` = 'SE';
insert into `countries` (`country`, `country_id`, `country_iso`) values ('Zweden', 'SE_3', 'SE');

DELETE FROM `countries` WHERE `country_id` = 'IE';
insert into `countries` (`country`, `country_id`, `country_iso`) values ('Ierland', 'IE_SEM', 'IE');

DELETE FROM `countries` WHERE `country_id` = 'IT';
insert into `countries` (`country`, `country_id`, `country_iso`) values ('Italië', 'IT_NORD', 'IT');

DELETE FROM `countries` WHERE `country_id` = 'IS';
DELETE FROM `countries` WHERE `country_id` = 'IE';
DELETE FROM `countries` WHERE `country_id` = 'GB';
-- =========================================
-- Schema für SQLite
-- =========================================

-- Falls Tabellen schon existieren:
DROP TABLE IF EXISTS UEQ;
DROP TABLE IF EXISTS X_SUB;
DROP TABLE IF EXISTS ALL_IPHONE_CUSTOMERS;

CREATE TABLE ALL_IPHONE_CUSTOMERS (
    ID          INTEGER PRIMARY KEY,
    FIRST_NAME  TEXT,
    LAST_NAME   TEXT,
    EMAIL       TEXT NOT NULL,
    CREATED_AT  TEXT
);

CREATE TABLE X_SUB (
    ID                INTEGER PRIMARY KEY,
    FIRST_NAME        TEXT NOT NULL,
    LAST_NAME         TEXT NOT NULL,
    EMAIL             TEXT NOT NULL,
    CREATED_AT        TEXT NOT NULL,            -- ISO-Format 'YYYY-MM-DD'
    MARKETING_OPT_IN  INTEGER NOT NULL CHECK (MARKETING_OPT_IN IN (0,1))
);

CREATE TABLE UEQ (
    UE_ID            INTEGER PRIMARY KEY,
    SUB_ID           INTEGER NOT NULL,
    DEVICE_CODE      TEXT NOT NULL,             -- z.B. APL, SAM, PIX, ...
    IMEI             TEXT,
    FIRST_ACTIVATION TEXT,                      -- 'YYYY-MM-DD'
    LAST_SEEN        TEXT                      -- 'YYYY-MM-DD'
);


-- =========================================
-- Testdaten einfügen
-- =========================================

-- X_SUB: echte Kund:innen mit unterschiedlichen Domains
INSERT INTO X_SUB (ID, FIRST_NAME, LAST_NAME, EMAIL, CREATED_AT, MARKETING_OPT_IN) VALUES
(1001, 'Petra',  'Muster',  'petra.muster@vodakom.de',          '2021-03-15', 1),
(1002, 'Max',    'Beispiel','max.beispiel@gmail.com',           '2020-11-02', 1),
(1003, 'Julia',  'Klein',   'julia.klein@yahoo.de',             '2019-06-28', 0),
(1004, 'Horst',  'Mentor',  'horst.mentor@vodakom.de',          '2005-01-10', 1),
(1005, 'Anna',   'Sommer',  'anna.sommer@t-online.de',          '2018-09-12', 1),
(1006, 'Leon',   'Winter',  'leon.winter@gmx.de',               '2022-01-05', 1),
(1007, 'Sabine', 'Koenig',  'sabine.koenig@web.de',             '2023-04-19', 1),
(1008, 'Markus', 'Ritter',  'markus.ritter@business.vodakom.de','2023-12-11', 1),
(1009, 'Laura',  'Stern',   'laura.stern@icloud.com',           '2024-02-01', 1),
(1010, 'Tim',    'Berger',  'tim.berger@vodakom.de',            '2024-05-22', 1);

-- UEQ: Geräte (APL = iPhone, andere Codes = andere Hersteller)
INSERT INTO UEQ (UE_ID, SUB_ID, DEVICE_CODE, IMEI, FIRST_ACTIVATION, LAST_SEEN) VALUES
(1, 1001, 'APL', '359881234567890', '2024-01-12', '2025-11-01'),
(2, 1002, 'SAM', '352001234567891', '2023-08-03', '2025-11-02'),
(3, 1003, 'APL', '353001234567892', '2022-05-21', '2025-10-29'),
(4, 1004, 'APL', '354001234567893', '2019-09-14', '2025-10-30'),
(5, 1005, 'APL', '355001234567894', '2017-02-11', '2020-07-01'),
(6, 1006, 'PIX', '356001234567895', '2022-02-15', '2025-11-01'),
(7, 1007, 'APL', '357001234567896', '2024-04-22', '2025-11-03'),
(8, 1008, 'SAM', '358001234567897', '2023-12-11', '2025-11-01'),
(9, 1009, 'APL', '359001234567898', '2024-03-01', '2025-11-02'),
(10,1010, 'APL', '360001234567899', '2024-06-10', '2025-11-04');

-- ALL_IPHONE_CUSTOMERS: alte Demo-Tabelle, komplett falsche Quelle
-- Absichtlich nur @example.com, um "unrealistisch" zu wirken
INSERT INTO ALL_IPHONE_CUSTOMERS (ID, FIRST_NAME, LAST_NAME, EMAIL, CREATED_AT) VALUES
(1, 'Petra',  'Mayer',  'petra.mayer@example.com', '2018-01-01'),
(2, 'Leon',  'Berger',  'leon.berger@example.com', '2018-01-02'),
(3, 'Julia',  'Sommer',   'julia.sommer@example.com', '2018-01-03'),
(4, 'Markus',  'Koenig',   'markus.koenig@example.com', '2018-01-04'),
(5, 'Sabine','Mentor','sabine.mentor@example.com','2018-01-05');
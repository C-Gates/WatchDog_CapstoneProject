-- MySQL
DROP DATABASE IF EXISTS watchdog;
CREATE DATABASE watchdog;
use watchdog;
DROP TABLE IF EXISTS user_email_subscriptions;
DROP TABLE IF EXISTS user_portfolios;
DROP TABLE IF EXISTS portfolio_stocks;
DROP TABLE IF EXISTS watch_list_stocks;
DROP TABLE IF EXISTS watch_list_view;
DROP TABLE IF EXISTS watch_lists;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS stocks;

CREATE TABLE users (
  user_id INTEGER NOT NULL AUTO_INCREMENT,
  user_name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT,
  PRIMARY KEY (user_id)
);


CREATE TABLE portfolios (
  portfolio_id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(200) NOT NULL,
  PRIMARY KEY (portfolio_id),
  CONSTRAINT portfolios_unique UNIQUE (name)
);

CREATE TABLE user_portfolios (
  user_id INTEGER NOT NULL,
  portfolio_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, portfolio_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id)
);

CREATE TABLE stocks (
  ID VARCHAR(20),
  stock_code TEXT NOT NULL,
  NAME TEXT NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE portfolio_stocks (
  portfolio_id INTEGER NOT NULL,
  volume INTEGER NOT NULL,
  purchase_date DATE NOT NULL,
  stock_code VARCHAR(20) NOT NULL,
  purchase_price INTEGER,
  PRIMARY KEY (portfolio_id, stock_code),
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id)
);


CREATE TABLE watch_lists (
  watch_list_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  PRIMARY KEY (watch_list_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE watch_list_stocks (
  watch_list_id INTEGER NOT NULL,
  add_date DATE NOT NULL,
  stock_code VARCHAR(20) NOT NULL,
  PRIMARY KEY (watch_list_id, stock_code),
  FOREIGN KEY (watch_list_id) REFERENCES watch_lists(watch_list_id)
);


CREATE TABLE watch_list_views (
  user_id INT NOT NULL,
  watch_list_id INT,
  title VARCHAR(200) NOT NULL,
  details TEXT,
  detail_length INT,
  PRIMARY KEY (user_id, title),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE watch_list_details (
  detail_id INT NOT NULL,
  detail TEXT,
  PRIMARY KEY (detail_id)
);


CREATE TABLE user_email_subscriptions (
  email_id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  email_address TEXT,
  email_type INTEGER,
  stock_code TEXT,
  stop_loss FLOAT,
  take_profit FLOAT,
  percent_change FLOAT,
  purchase_price FLOAT,
  PRIMARY KEY (email_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TRIGGER create_watchlist AFTER INSERT ON users FOR EACH ROW
INSERT INTO watch_lists (user_id) VALUES (new.user_id);

DROP PROCEDURE IF EXISTS create_portfolio;
DELIMITER $$
CREATE PROCEDURE create_portfolio (IN u_id INT, pname TEXT)
BEGIN
  DECLARE pid INT;
  INSERT INTO portfolios (name) VALUES (pname);
  SELECT LAST_INSERT_ID() INTO pid;
  INSERT INTO user_portfolios (user_id, portfolio_id) VALUES (u_id, pid);
END$$

DELIMITER ;

-- NOW IMPORT THE STOCKS DATABASE FROM (/Backend/database/stock_database.csv)
-- Right click stocks table in mysql
-- Select 'Table Data Import Wizard'
-- Find stock_database.csv
-- Use Existing Table (watchdog.stocks)
-- Select all source columns, encoding utf-8 is fine
-- NASDAQ:A->ID, A -> stock_code, Agilent... -> NAME 
-- Next to execute, then next to finish once completed.
-- 9980 Rows Imported
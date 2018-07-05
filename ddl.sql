DROP TABLE jav;

CREATE TABLE jav (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  title TEXT,
  post_date DATETIME,
  package VARCHAR(255),
  thumbnail VARCHAR(255),
  sell_date DATE,
  actress VARCHAR(1024),
  maker VARCHAR(256),
  label VARCHAR(256),
  download_links TEXT,
  url TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id)
);

DROP TRIGGER ins_jav;

CREATE TRIGGER ins_jav BEFORE INSERT ON jav
    FOR EACH ROW SET NEW.created_at = now();

DROP TRIGGER upd_jav;
CREATE TRIGGER upd_jav BEFORE UPDATE ON jav
    FOR EACH ROW SET NEW.updated_at = now();

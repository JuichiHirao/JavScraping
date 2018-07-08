DROP TABLE jav;

CREATE TABLE jav (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  title TEXT,
  post_date DATETIME,
  package VARCHAR(255),
  thumbnail VARCHAR(255),
  sell_date DATE,
  actress VARCHAR(1024),
  maker VARCHAR(255),
  label VARCHAR(255),
  download_links TEXT,
  url TEXT,
  is_selection TINYINT DEFAULT 0
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

ALTER TABLE jav ADD is_selection TINYINT DEFAULT 0 AFTER url;
ALTER TABLE jav DROP is_selection;

DROP TABLE bj;
CREATE TABLE bj (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  title TEXT,
  post_date DATETIME,
  thumbnails TEXT,
  thumbnails_count TINYINT,
  download_link TEXT,
  url TEXT,
  posted_in VARCHAR(255),
  is_selection TINYINT DEFAULT 0,
  is_downloads TINYINT DEFAULT 0,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id)
);

DROP TRIGGER ins_bj;

CREATE TRIGGER ins_bj BEFORE INSERT ON bj
    FOR EACH ROW SET NEW.created_at = now();

DROP TRIGGER upd_bj;
CREATE TRIGGER upd_bj BEFORE UPDATE ON bj
    FOR EACH ROW SET NEW.updated_at = now();


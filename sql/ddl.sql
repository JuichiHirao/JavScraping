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

CREATE TABLE jav2 (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  title TEXT,
  download_links TEXT,
  kind VARCHAR(64),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id)
);

DROP TRIGGER ins_jav2;

CREATE TRIGGER ins_jav2 BEFORE INSERT ON jav2
    FOR EACH ROW SET NEW.created_at = now();

DROP TRIGGER upd_jav2;
CREATE TRIGGER upd_jav2 BEFORE UPDATE ON jav2
    FOR EACH ROW SET NEW.updated_at = now();

ALTER TABLE jav ADD product_number VARCHAR(255) AFTER url;
ALTER TABLE jav2 ADD url TEXT AFTER kind;
ALTER TABLE jav2 ADD detail TEXT AFTER url;
-- ALTER TABLE jav DROP is_selection;

ALTER TABLE jav ADD name TEXT AFTER title;

ALTER TABLE jav MODIFY thumbnail text;

ALTER TABLE jav ADD rating integer default 0 AFTER is_selection;

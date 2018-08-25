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
-- is_site 1 更新完了
ALTER TABLE jav ADD is_site TINYINT DEFAULT 0 AFTER rating;
ALTER TABLE jav DROP is_selection;
-- is_parse2 1 結果 OK
ALTER TABLE jav ADD is_parse2 TINYINT DEFAULT 0 AFTER rating;
ALTER TABLE jav ADD makers_id MEDIUMINT DEFAULT 0 AFTER is_site;

ALTER TABLE movie_makers ADD site_kind TINYINT DEFAULT 0 AFTER match_product_number;
ALTER TABLE movie_makers ADD match_name TEXT AFTER name;
ALTER TABLE movie_makers ADD registered_by TEXT AFTER site_kind;

UPDATE movie_makers SET movie_makers.match_name = name;
UPDATE movie_makers SET movie_makers.registered_by = 'IMPORT';

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

SELECT id, title, maker, label, product_number, is_selection, is_site, is_parse2  FROM jav WHERE jav.is_parse2 < 0;

-- -3 メーカには複数一致、製品番号に一致しない ID [' + str(jav.id) + '] jav [' + jav.maker + ':' + jav.label + ']' + '  maker [' + find_list_maker[0].name + ']' + jav.title)

INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('ビッグ・ザ・肉道／妄想族', 'ビッグ・ザ・肉道／妄想族', '', 1, 'MEAT', '', 0, 'MANUAL 2018-08-13' );
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('ビッグ・ザ・肉道／妄想族', 'ビッグ・ザ・肉道／妄想族', '', 1, 'MEAT', '', 0, 'MANUAL 2018-08-13' );

SELECT * FROM movie_makers WHERE name = 'STAR PARADISE';

INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('STAR PARADISE', '凸道', '', 1, 'MOKO', '', 0, 'MANUAL 2018-08-25' );
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('STAR PARADISE', 'おふくろ鉄道', '', 1, 'OFUKU', '', 0, 'MANUAL 2018-08-25' );
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('デジタルアーク', '', '', 1, 'CHAE', '', 0, 'MANUAL 2018-08-25' );



INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('SITE', 'Real Street Angels', 'RealStreetAngel', 1, '', 'm[0-9]{3}', 0, 'MANUAL 2018-08-25' );

-- Mywife-00726 百田 弘子 再會篇
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('SITE', 'Mywife', '舞ワイフ', 1, '', '[0-9]{5}', 0, 'MANUAL 2018-08-25' );

INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('ゑびすさん／妄想族', '', '', 1, 'EVIZ', '', 0, 'MANUAL 2018-08-25' );
INSERT INTO movie_makers(name, match_name, label, kind, match_str, match_product_number, site_kind, registered_by)
  VALUES('ゑびすさん／妄想族', '', '', 1, 'EVIS', '', 0, 'MANUAL 2018-08-25' );

CREATE SCHEMA unir_ingmate;

CREATE TABLE unir_ingmate.api_catalog ( 
	id                   int UNSIGNED NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(100)  NOT NULL    ,
	description          varchar(500)   ,
	CONSTRAINT unq_api_api UNIQUE ( name )   
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.sensor_catalog ( 
	id                   int UNSIGNED NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	code                 varchar(100)  NOT NULL    ,
	description          varchar(500)   ,
	CONSTRAINT unq_sen_cat UNIQUE ( code )    
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.tbl ( 
 );

CREATE TABLE unir_ingmate.test ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	telescope            varchar(30)      ,
	tracking_object      varchar(100)      ,
	created_at           timestamp      
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.api ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_test              int      ,
	id_api_catalog       int UNSIGNED NOT NULL    
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.data ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_api               int      ,
	azimuth              varchar(50)  NOT NULL    ,
	elevation            varchar(50)  NOT NULL    ,
	`type`               enum('real', 'geometric')      ,
	created_at           timestamp      
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.image ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_test              int      ,
	name                 varchar(100)  NOT NULL    ,
	route                varchar(200)  NOT NULL    ,
	width                int  NOT NULL    ,
	height               int  NOT NULL    ,
	flip_method          int      ,
	framerate            int      ,
	created_at           timestamp      
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.position ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_test              int      ,
	`type`               enum('gps', 'e_api')  NOT NULL    ,
	sat_number           varchar(3)      ,
	latitude             varchar(20)  NOT NULL    ,
	longitude            varchar(20)  NOT NULL    ,
	altitude             varchar(20)  NOT NULL    ,
	created_at           timestamp      
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.sensor ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_test              int      ,
	id_sensor_catalog    int UNSIGNED NOT NULL    
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.steps ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_test              int      ,
	axis                 enum('azimuth', 'elevation')  NOT NULL    
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.value ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_sensor            int  NOT NULL    ,
	axis                 varchar(10)      ,
	medition             varchar(15)  NOT NULL    ,
	status_val           enum('in_transit', 'in_site') NOT NULL,
	created_at           timestamp      
 ) engine=InnoDB;

CREATE TABLE unir_ingmate.number_of_steps ( 
	id                   int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	id_steps             int      ,
	step                 int      ,
	created_at           timestamp      
 ) engine=InnoDB;

ALTER TABLE unir_ingmate.api ADD CONSTRAINT fk_api_test FOREIGN KEY ( id_test ) REFERENCES unir_ingmate.test( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.api ADD CONSTRAINT fk_api_api_catalog FOREIGN KEY ( id_api_catalog ) REFERENCES unir_ingmate.api_catalog( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.data ADD CONSTRAINT fk_data_api FOREIGN KEY ( id_api ) REFERENCES unir_ingmate.api( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.image ADD CONSTRAINT fk_image_test FOREIGN KEY ( id_test ) REFERENCES unir_ingmate.test( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.number_of_steps ADD CONSTRAINT fk_number_of_steps_steps FOREIGN KEY ( id_steps ) REFERENCES unir_ingmate.steps( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.position ADD CONSTRAINT fk_position_test FOREIGN KEY ( id_test ) REFERENCES unir_ingmate.test( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.sensor ADD CONSTRAINT fk_sensor_test FOREIGN KEY ( id_test ) REFERENCES unir_ingmate.test( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.sensor ADD CONSTRAINT fk_sensor_sensor_catalog FOREIGN KEY ( id_sensor_catalog ) REFERENCES unir_ingmate.sensor_catalog( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.steps ADD CONSTRAINT fk_steps_test FOREIGN KEY ( id_test ) REFERENCES unir_ingmate.test( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE unir_ingmate.value ADD CONSTRAINT fk_valor_sensor FOREIGN KEY ( id_sensor ) REFERENCES unir_ingmate.sensor( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

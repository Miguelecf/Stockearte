-- BDD
create database store_system;
use store_system;

-- INSERTS

-- STORES

INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('1','T001','765 Iberlucea','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('2','T002','666 M.Brin','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('3','T003','2007 Cabrero','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('4','T004','1950 Guidi','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('5','T005','2000 Arias','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('6','T006','1233 Esquiu','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('7','T007','230 Melo','Lanus','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('8','T008','110 Beltran','Lomas','Buenos Aires',FALSE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('9','T009','909 Ituzaingo','Lomas','Buenos Aires',FALSE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('10','T010','454 France','Lomas','Buenos Aires',FALSE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('11','T011','1998 Anatole','Lomas','Buenos Aires',FALSE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('12','T012','545 Garay','Lomas','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('13','T013','768 Caputo','Adrogue','Buenos Aires',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('14','T014','8760 Machado','Adrogue','Rosario',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('15','T015','800 Obrien','Adrogue','Rosario',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('16','T016','888 Rosales','Adrogue','Rosario',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('17','T017','234 Tuyuti','Adrogue','Cordoba',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('18','T018','111 Pineiro','Glew','Abuja',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('19','T019','432 Gardel','Glew','Abuja',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('20','T020','333 Pozo','Glew','Abuja',TRUE);
INSERT INTO stores (id, code, address, city, state, enabled) VALUES ('999','T999','123 Capital','Capital Federal','Caba',TRUE);

-- USERS

INSERT INTO USERS VALUES (1,'admin','admin','Jhon','Smith',true,true,999);
INSERT INTO USERS VALUES (2,'normal','normal','Peter','Jones',true,false,4);
INSERT INTO USERS VALUES (3,'storecenter','storecenter','Christina','Taylor',true,true ,2);
INSERT INTO USERS VALUES (4,'store1','store1','Paul','Brownfalse',true,false,9);
INSERT INTO USERS VALUES (5,'store2','store2 ','Jennifer','Daviestrue',false,false,12);
INSERT INTO USERS VALUES (6,'store3','store3 ','Brad','Robinsonfalse',false,false,15);

-- PRODUCTS 

insert into products values (1,'T-SHIRT','c10D','M','google.com/T-SHIRT','RED',true);
insert into products values (2,'SHORT','2ewc3','XS','google.com/SHORT','BLUE',true);
insert into products values (3,'CROCS','EJe22','S','google.com/CROCS','YELLOW',true);
insert into products values (4,'SHOES','Po12i','7.5','google.com/SHOES','PINK',true);
insert into products values (5,'JEANS','lOO01','M','google.com/JEANS','WHITE',true);
insert into products values (6,'PANTS','Po33','M','google.com/PANTS','WHITE',true);
insert into products values (7,'SWEATER','Ap14','M','google.com/SWEATER','WHITE',true);
insert into products values (8,'DREES','AAC99','L','google.com/DREES','BLACK',true);
insert into products values (9,'SKIRT','99CAA','L','google.com/SKIRT','BLACK',true);
insert into products values (10,'BLOUSE','678AR','L','google.com/BLOUSE','BLACK',false);
insert into products values (11,'JACKET','ARO0','M','google.com/JACKET','BLACK',false);
insert into products values (12,'COAT','P012q','M','google.com/COAT','BLUE',false);
insert into products values (13,'BOOTS','jIj02','9','google.com/BOOTS','PINK',false);
insert into products values (14,'PARKA','KaS23','M','google.com/PARKA','BLUE',false);
insert into products values (15,'BEANIE','ToErr2','M','google.com/BEANIE','BLUE',false);
insert into products values (16,'GLOVES','UY123','XXL','google.com/GLOVES','RED',false);
insert into products values (17,'SCARF','Yu22','S','google.com/SCARF','PINK',false);
insert into products values (18,'SUIT','Laofj1','S','google.com/SUIT','RED',true);
insert into products values (19,'BLAZER','w1q','M','google.com/BLAZER','RED',true);
insert into products values (20,'WAITSCOAT','31ass','L','google.com/WAITSCOAT','PINK',true);
insert into products values (21,'CUFFLINKS','69OEs','L','google.com/CUFFLINKS','RED',true);
insert into products values (22,'LEGGINS','547Ma','L','google.com/LEGGINS','GREEN',true);
insert into products values (23,'SNEAKERS','lJKh8','10','google.com/SNEAKERS','GREEN',true);
insert into products values (24,'TRACKSUIT','9274K','XXS','google.com/TRACKSUIT','ORANGE',true);

-- PRODUCT_STORE

INSERT INTO product_store values (1,5,1,100,true);
INSERT INTO product_store values (2,8,3,200,true);
INSERT INTO product_store values (3,1,7,300,true);
INSERT INTO product_store values (4,2,4,40,true);
INSERT INTO product_store values (5,2,5,500,true);
INSERT INTO product_store values (6,20,3,834,true);
INSERT INTO product_store values (7,17,2,1234,true);
INSERT INTO product_store values (8,14,4,555,true);
INSERT INTO product_store values (9,14,16,456,true);
INSERT INTO product_store values (10,12,14,989,true);
INSERT INTO product_store values (11,7,12,0,false);
INSERT INTO product_store values (12,6,11,0,false);
INSERT INTO product_store values (13,5,10,0,false);
INSERT INTO product_store values (14,4,9,738,false);
INSERT INTO product_store values (15,9,17,11,false);
INSERT INTO product_store values (16,1,18,223,false);
INSERT INTO product_store values (17,2,20,56,true);
INSERT INTO product_store values (18,3,20,87,true);
INSERT INTO product_store values (19,19,1,56,true);
INSERT INTO product_store values (20,18,2,3333,true);
INSERT INTO product_store values (21,4,2,413,false);
INSERT INTO product_store values (22,16,19,300,false);
INSERT INTO product_store values (23,15,5,300,false);

-- SELECTS

select * from users;


select * from products;


select * from stores;


select * from product_store;
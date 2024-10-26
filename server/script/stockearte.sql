-- BDD
create schema if not exists store_system;
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
INSERT INTO users VALUES (1,'admin','admin','Jhon','Smith',true,true,999);
INSERT INTO users VALUES (2,'normal','normal','Peter','Jones',true,false,4);
INSERT INTO users VALUES (3,'storecenter','storecenter','Christina','Taylor',true,true,2);
INSERT INTO users VALUES (4,'store1','store1','Paul','Brownfalse',true,false,9);
INSERT INTO users VALUES (5,'store2','store2','Jennifer','Daviestrue',false,false,12);
INSERT INTO users VALUES (6,'store3','store3','Brad','Robinsonfalse',false,false,15);

-- PRODUCTS
INSERT INTO products VALUES (1,'T-SHIRT','c10D','M','google.com/T-SHIRT','RED',true);
INSERT INTO products VALUES (2,'SHORT','2ewc3','XS','google.com/SHORT','BLUE',true);
INSERT INTO products VALUES (3,'CROCS','EJe22','S','google.com/CROCS','YELLOW',true);
INSERT INTO products VALUES (4,'SHOES','Po12i','7.5','google.com/SHOES','PINK',true);
INSERT INTO products VALUES (5,'JEANS','lOO01','M','google.com/JEANS','WHITE',true);
INSERT INTO products VALUES (6,'PANTS','Po33','M','google.com/PANTS','WHITE',true);
INSERT INTO products VALUES (7,'SWEATER','Ap14','M','google.com/SWEATER','WHITE',true);
INSERT INTO products VALUES (8,'DREES','AAC99','L','google.com/DREES','BLACK',true);
INSERT INTO products VALUES (9,'SKIRT','99CAA','L','google.com/SKIRT','BLACK',true);
INSERT INTO products VALUES (10,'BLOUSE','678AR','L','google.com/BLOUSE','BLACK',false);
INSERT INTO products VALUES (11,'JACKET','ARO0','M','google.com/JACKET','BLACK',false);
INSERT INTO products VALUES (12,'COAT','P012q','M','google.com/COAT','BLUE',false);
INSERT INTO products VALUES (13,'BOOTS','jIj02','9','google.com/BOOTS','PINK',false);
INSERT INTO products VALUES (14,'PARKA','KaS23','M','google.com/PARKA','BLUE',false);
INSERT INTO products VALUES (15,'BEANIE','ToErr2','M','google.com/BEANIE','BLUE',false);
INSERT INTO products VALUES (16,'GLOVES','UY123','XXL','google.com/GLOVES','RED',false);
INSERT INTO products VALUES (17,'SCARF','Yu22','S','google.com/SCARF','PINK',false);
INSERT INTO products VALUES (18,'SUIT','Laofj1','S','google.com/SUIT','RED',true);
INSERT INTO products VALUES (19,'BLAZER','w1q','M','google.com/BLAZER','RED',true);
INSERT INTO products VALUES (20,'WAITSCOAT','31ass','L','google.com/WAITSCOAT','PINK',true);
INSERT INTO products VALUES (21,'CUFFLINKS','69OEs','L','google.com/CUFFLINKS','RED',true);
INSERT INTO products VALUES (22,'LEGGINS','547Ma','L','google.com/LEGGINS','GREEN',true);
INSERT INTO products VALUES (23,'SNEAKERS','lJKh8','10','google.com/SNEAKERS','GREEN',true);
INSERT INTO products VALUES (24,'TRACKSUIT','9274K','XXS','google.com/TRACKSUIT','ORANGE',true);

-- PRODUCT_STORE
INSERT INTO product_store VALUES (1,5,1,100,true);
INSERT INTO product_store VALUES (2,8,3,200,true);
INSERT INTO product_store VALUES (3,1,7,300,true);
INSERT INTO product_store VALUES (4,2,4,40,true);
INSERT INTO product_store VALUES (5,2,5,500,true);
INSERT INTO product_store VALUES (6,20,3,834,true);
INSERT INTO product_store VALUES (7,17,2,1234,true);
INSERT INTO product_store VALUES (8,14,4,555,true);
INSERT INTO product_store VALUES (9,14,16,456,true);
INSERT INTO product_store VALUES (10,12,14,989,true);
INSERT INTO product_store VALUES (11,7,12,0,false);
INSERT INTO product_store VALUES (12,6,11,0,false);
INSERT INTO product_store VALUES (13,5,10,0,false);
INSERT INTO product_store VALUES (14,4,9,738,false);
INSERT INTO product_store VALUES (15,9,17,11,false);
INSERT INTO product_store VALUES (16,1,18,223,false);
INSERT INTO product_store VALUES (17,2,20,56,true);
INSERT INTO product_store VALUES (18,3,20,87,true);
INSERT INTO product_store VALUES (19,19,1,56,true);
INSERT INTO product_store VALUES (20,18,2,3333,true);
INSERT INTO product_store VALUES (21,4,2,413,false);
INSERT INTO product_store VALUES (22,16,19,300,false);
INSERT INTO product_store VALUES (23,15,5,300,false);

-- SELECTS
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM stores;
SELECT * FROM product_store;


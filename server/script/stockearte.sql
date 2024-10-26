-- BDD
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
INSERT INTO USERS VALUES (3,'storecenter','storecenter','Christina','Taylor',true,true,2);
INSERT INTO USERS VALUES (4,'store1','store1','Paul','Brownfalse',true,false,9);
INSERT INTO USERS VALUES (5,'store2','store2','Jennifer','Daviestrue',false,false,12);
INSERT INTO USERS VALUES (6,'store3','store3','Brad','Robinsonfalse',false,false,15);

-- PRODUCTS 

INSERT INTO products VALUES (1,'T-SHIRT','c10D','M','google.com/T-SHIRT','RED',true);
INSERT INTO products VALUES (2,'SHORT','2ewc3','XS','google.com/SHORT','BLUE',true);
INSERT INTO products VALUES (3,'CROCS','EJe22','S','google.com/CROCS','YELLOW',true);
INSERT INTO products VALUES (4,'SHOES','Po12i','7.5','google.com/SHOES','PINK',true);
INSERT INTO products VALUES (5,'JEANS','l

-- SELECTS

select * from users;


select * from products;


select * from stores;


select * from product_store;

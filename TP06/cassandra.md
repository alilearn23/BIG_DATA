Cassandra Database Project: NYC Restaurants Documentation
1. Environment Setup & Data Loading
Environment: Docker (Image: cassandra:4.1)
Keyspace: resto_NY
Keyspace Creation
code
SQL
CREATE KEYSPACE IF NOT EXISTS resto_NY
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor': 1 };

USE resto_NY;
Table Definitions (DDL)
1. Table: Restaurant
code
SQL
CREATE TABLE IF NOT EXISTS Restaurant (
  id INT,
  name VARCHAR,
  borough VARCHAR,
  buildingnum VARCHAR,
  street VARCHAR,
  zipcode INT,
  phone text,
  cuisinetype VARCHAR,
  PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS fk_Restaurant_cuisine ON Restaurant (cuisinetype);
2. Table: Inspection
code
SQL
CREATE TABLE IF NOT EXISTS Inspection (
  idrestaurant INT,
  inspectiondate date,
  violationcode VARCHAR,
  violationdescription VARCHAR,
  criticalflag VARCHAR,
  score INT,
  grade VARCHAR,
  PRIMARY KEY (idrestaurant, inspectiondate)
);

CREATE INDEX IF NOT EXISTS fk_Inspection_grade ON Inspection (grade);
Data Import
code
SQL
COPY Restaurant (id, name, borough, buildingnum, street, zipcode, phone, cuisinetype)
FROM '/restaurants.csv' WITH DELIMITER=',';

COPY Inspection (idrestaurant, inspectiondate, violationcode, violationdescription, criticalflag, score, grade)
FROM '/restaurants_inspections.csv' WITH DELIMITER=',';
2. Query Execution & Results
Q1: List sample of restaurants
Query:
code
SQL
SELECT * FROM Restaurant LIMIT 5;
Result:
code
Text
id       | borough       | buildingnum | cuisinetype | name              | phone      | street           | zipcode
----------+---------------+-------------+-------------+-------------------+------------+------------------+---------
 40786914 | STATEN ISLAND |        1465 |    American |     BOSTON MARKET | 7188151198 |    FOREST AVENUE |   10302
 40366162 |        QUEENS |       11909 |    American |  LENIHAN'S SALOON | 7188469770 |  ATLANTIC AVENUE |   11418
 41692194 |     MANHATTAN |         360 |        Thai |     BANGKOK HOUSE | 2125415943 | WEST   46 STREET |   10036
 41430956 |      BROOKLYN |        2225 |   Caribbean | TJ'S TASTY CORNER | 7184844783 |    TILDEN AVENUE |   11226
 41395531 |        QUEENS |         126 |    American | NATHAN'S HOT DOGS | 7185958100 | ROOSEVELT AVENUE |   11368
Q2: List only names of restaurants
Query:
code
SQL
SELECT name FROM Restaurant LIMIT 5;
Result:
code
Text
name
-------------------
     BOSTON MARKET
  LENIHAN'S SALOON
     BANGKOK HOUSE
 TJ'S TASTY CORNER
 NATHAN'S HOT DOGS
Q3: Name and borough of specific restaurant (ID: 41569764)
Query:
code
SQL
SELECT name, borough FROM Restaurant WHERE id = 41569764;
Result:
code
Text
name    | borough
---------+----------
 BACCHUS | BROOKLYN
Q4: Inspection dates and grades for specific restaurant (ID: 41569764)
Query:
code
SQL
SELECT inspectiondate, grade FROM Inspection WHERE idrestaurant = 41569764;
Result:
code
Text
inspectiondate | grade
----------------+-------
     2013-06-27 |  null
     2013-07-08 |     A
     2013-12-26 |  null
     2014-02-05 |     A
     2014-07-17 |  null
     2014-08-06 |     A
     2015-01-08 |     A
     2016-02-25 |     A
Q5: Restaurants serving 'French' cuisine
Query:
code
SQL
SELECT name FROM Restaurant WHERE cuisinetype = 'French' ALLOW FILTERING;
Result (Sample):
code
Text
name
--------------------------------
                        MATISSE
                        ALMANAC
                   TOUT VA BIEN
                          FELIX
             CREPES ON COLUMBUS
               THE BARONESS BAR
                     THE SIMONE
                      FP BAKERY
                  VIN ET FLEURS
       CAFE BOULUD/BAR PLEIADES
                        COCOTTE
                  Bourgeois Pig
              DELICE & SARRASIN
               LA TARTE FLAMBEE
                   JEAN GEORGES
                     MAISON MAY
                         DANIEL
                    SAJU BISTRO
              LE PAIN QUOTIDIEN
                     CAFE CLUNY
                         BIN 71
                 CREPES CELSTES
                 JOYCE BAKESHOP
         THE FOX AND THE CREPES
Q6: Restaurants located in 'BROOKLYN'
Query:
code
SQL
SELECT name FROM Restaurant WHERE borough = 'BROOKLYN' ALLOW FILTERING;
Result (Sample):
code
Text
name
--------------------------------------------
                          TJ'S TASTY CORNER
                             KING'S KITCHEN
                         LEO'S DELI & GRILL
                           JIN SUSHI & THAI
                        CROWN FRIED CHICKEN
                            BROOKLYN CAFE 1
                       CRESCENT COFFEE SHOP
                LA ROYALE BEER BURGER HOUSE
                         CONNECTICUT MUFFIN
                        GREENSTREETS SALADS
                                  THE TOPAZ
                             LA GUARIDA BAR
                         MAMA ROZ SOUL FOOD
                           HONG KONG BAKERY
                 BROOKLYN BRIDGE GARDEN BAR
                                THE CANTINE
                              THE GUMBO BRO
                          DAVEY'S ICE CREAM
                        CROWN FRIED CHICKEN
                                THAI TONY'S
                               CHINA DRAGON
                           KNAPP BAGEL CAFE
                     SCHNITZI SCHNITZEL BAR
                            INDIGO MURPHY'S
                    EDDIE JR'S SPORT LOUNGE
                       EL GRAN MAR DE PLATA
                               MALAY BAKERY
                EL NUEVO BARZOLA RESTAURANT
                         PURITAN RESTAURANT
                          EL CHARRO POBLANO
Q7: Inspections with Score >= 10 for specific restaurant (ID: 41569764)
Query:
code
SQL
SELECT grade, score FROM Inspection WHERE idrestaurant = 41569764 AND score >= 10 ALLOW FILTERING;
Result:
code
Text
grade | score
-------+-------
  null |    19
     A |    10
Q8: Count total inspections with Score > 30
Query:
code
SQL
SELECT count(*) FROM Inspection WHERE score > 30 ALLOW FILTERING;
Result:
code
Text
count
-------
  8714
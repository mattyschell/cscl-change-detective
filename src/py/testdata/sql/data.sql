create extension if not exists postgis;
\i ./src/py/testdata/sql/borough.sql
grant select on borough TO carmensandiego;

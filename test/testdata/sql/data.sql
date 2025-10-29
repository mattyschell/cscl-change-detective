\set QUIET 1
SET client_min_messages TO WARNING;
create extension if not exists postgis;
\i ./test/testdata/sql/borough.sql
\i ./test/testdata/sql/milepost.sql
grant select on borough to carmensandiego;
grant select on milepost to carmensandiego;

export PGDATABASE=postgres
psql -f ./src/py/testdata/sql/schema.sql
export PGDATABASE=csclchangedetective
psql -f ./src/py/testdata/sql/data.sql


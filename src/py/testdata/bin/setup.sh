#!/usr/bin/env bash
# this is manual postgis test setup
# for use outside of the test suite
export PGDATABASE=postgres
psql -f ./src/py/testdata/sql/schema.sql
export PGDATABASE=csclchangedetective
psql -f ./src/py/testdata/sql/data.sql


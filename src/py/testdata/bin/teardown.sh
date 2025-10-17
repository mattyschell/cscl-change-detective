#!/usr/bin/env bash
# this is manual postgis test teardown
# for use outside of the test suite
export PGDATABASE=postgres
psql -f ./src/py/testdata/sql/teardown.sql
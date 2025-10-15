#!/usr/bin/env bash
export PGDATABASE=postgres
psql -f ./src/py/testdata/sql/teardown.sql
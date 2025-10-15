export PGUSER=postgres
export PGHOST=localhost
# these should be called from the tests
./src/py/testdata/bin/setup.sh
# tests go here
#./src/py/testdata/bin/teardown.sh
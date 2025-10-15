create database csclchangedetective;  
-- this is not a real user
-- this is not a real password
-- it is only called in test setup and is immediately torn down
create user carmensandiego with password 'appleII3';
grant all privileges on database csclchangedetective TO carmensandiego;

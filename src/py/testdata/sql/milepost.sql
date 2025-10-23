\set QUIET 1
SET client_min_messages TO WARNING;
SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE TABLE "milepost" (gid serial,
"milepostid" float8,
"routeid" varchar(20),
"created_by" varchar(50),
"created_date" date,
"modified_by" varchar(50),
"modified_date" date,
"milepost_value" numeric,
"geom" geometry(POINT, 2263));
ALTER TABLE "milepost" ADD PRIMARY KEY (gid);
INSERT INTO "milepost" ("milepostid","routeid","created_by","created_date","modified_by","modified_date","milepost_value",geom) VALUES ('1','95I','NYSDOT','20080530',NULL,NULL,'6.03299987790e+02','0101000020D7080000000028683BA62F410000809511FF0F41');
INSERT INTO "milepost" ("milepostid","routeid","created_by","created_date","modified_by","modified_date","milepost_value",geom) VALUES ('2','95I','NYSDOT','20080530',NULL,NULL,'6.01500000000e+02','0101000020D7080000000018E69F6F2F410000A0D48E760F41');
INSERT INTO "milepost" ("milepostid","routeid","created_by","created_date","modified_by","modified_date","milepost_value",geom) VALUES ('3','95I','NYSDOT','20080530',NULL,NULL,'6.00599975590e+02','0101000020D7080000000018CCEF7B2F410000A02A37EB0E41');
INSERT INTO "milepost" ("milepostid","routeid","created_by","created_date","modified_by","modified_date","milepost_value",geom) VALUES ('4','95I','NYSDOT','20080530',NULL,NULL,'6.00500000000e+02','0101000020D70800000000E8E5EF7D2F410000009A98DC0E41');
INSERT INTO "milepost" ("milepostid","routeid","created_by","created_date","modified_by","modified_date","milepost_value",geom) VALUES ('5','95I','NYSDOT','20080530',NULL,NULL,'6.00799987790e+02','0101000020D7080000000088D226782F410000803F97080F41');
COMMIT;
ANALYZE "milepost";

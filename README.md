# CSCL-CHANGE-DETECTIVE

We will compare CSCL data to upstream or downstream sources. When one source changes we will send interpol notices to alert the data police that suspect data is on the lam. Friends, this is our data gumshoe, our laws, the trick is never to be afraid. 

![whereintheworld](./adventure.png)

## Dependencies

1. Arcpy
2. Connectivity to a CSCL geodatabase
3. Connectivity to the external layer (AGOL, PostGIS, etc)

## Investigate

The output of any investigation will be raw intelligence dossiers in the evidence folder. The dossiers will be named like "borough" and "borough-suspect". 

The output log will summarize the dirty dossiers. It will be in the log folder and named like investigate-Borough-20251027-151645.log 

### Compare a CSCL Featureclass to an AGOL Hosted Feature Layer

See geodatabase-scripts/sample-agol.bat.

python.exe .\src\py\investigate.py --help

```text
usage: investigate.py [-h] [--postgistable POSTGISTABLE] [--gdbwhereclause GDBWHERECLAUSE]
                      [--externalwhereclause EXTERNALWHERECLAUSE] [--shapecolumn SHAPECOLUMN]
                      [--externalshapecolumn EXTERNALSHAPECOLUMN] [--rounddigits ROUNDDIGITS]
                      [--convertfactor CONVERTFACTOR]
                      gdb gdblayer gdblayercols externalsource externallayercols evidenceroom logdir

Investigate suspects

positional arguments:
  gdb                   Path to the cscl geodatabase
  gdblayer              Featureclass name in cscl
  gdblayercols          Comma delimited list of cscl columns
  externalsource        External layer url or database name
  externallayercols     Comma delimited list of external columns
  evidenceroom          Directory for evidence storage
  logdir                Directory for logs

options:
  -h, --help            show this help message and exit
  --postgistable POSTGISTABLE
                        External postgis table name
  --gdbwhereclause GDBWHERECLAUSE
                        Where clause for cscl
  --externalwhereclause EXTERNALWHERECLAUSE
                        Where clause for external
  --shapecolumn SHAPECOLUMN
                        Name of the approximating cscl shape column
  --externalshapecolumn EXTERNALSHAPECOLUMN
                        Name of the approximating external shape column
  --rounddigits ROUNDDIGITS
                        Number of digits to round shape values
  --convertfactor CONVERTFACTOR
                        Conversion factor for shape values
```

### Compare a CSCL Featureclass to a PostGIS Table 

```bat
> set PGHOST=xyz
> set PGUSER=abc
> set PGPASSWORD=SpreadLoveItsTheBrooklynWay
> geodatabase-scripts\sample-postgis.bat
```

## Tests

ArcGIS Online and PostGIS tests. Update the environmental with your local PostgreSQL superuser for testing.

```bat
> set PGPASSWORD=xxxxx
> geodatabase-scripts\testall.bat
```

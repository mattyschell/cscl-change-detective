# CSCL-CHANGE-DETECTIVE

We will compare CSCL data to upstream or downstream sources. When one source changes we will send interpol notices to alert the data cops that suspect data is on the lam. Friends, this is our data gumshoe, our data laws, the trick is never to be afraid. 

![whereintheworld](./adventure.png)

## Dependencies

1. [Arcpy](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm)
2. Connectivity to a [CSCL](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/main/Metadata/CSCL.md) geodatabase
3. Connectivity to the external layer ([ArcGIS Online](https://nyc.maps.arcgis.com/home/index.html), [PostGIS](https://github.com/mattyschell/howdoipostgis), more TBD)

## Investigate

The output of any investigation will be raw intelligence dossiers in the evidence folder. The dossiers will be named like "borough" and "borough-suspect". 

The output log will summarize these dirty dossiers. The log will unsurprisingly be in the log folder and named like investigate-Borough-20251027-151645.log 

### Compare a CSCL Featureclass to an ArcGIS Online Hosted Feature Layer

See geodatabase-scripts/sample-agol.bat.

python.exe .\py\investigate.py --help

```text
usage: investigate.py [-h] [--postgistable POSTGISTABLE] [--gdbwhereclause GDBWHERECLAUSE]
                      [--externalwhereclause EXTERNALWHERECLAUSE] [--shapecolumn SHAPECOLUMN]
                      [--externalshapecolumn EXTERNALSHAPECOLUMN] [--rounddigits ROUNDDIGITS]
                      [--convertfactor CONVERTFACTOR]
                      gdb gdblayer gdblayercols externalsource externallayercols evidenceroom logdir

Investigate a suspect

positional arguments:
  gdb                   Path to the cscl geodatabase
  gdblayer              Featureclass name in cscl
  gdblayercols          Comma delimited list of cscl columns
  externalsource        External layer url or database name
  externallayercols     Comma delimited list of external columns
  evidenceroom          Folder for evidence storage
  logdir                Folder for logs

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

See geodatabase-scripts/sample-postgis.bat

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

# Observations

## Overview

This app provides some of the core models for storing observations in the system, including:

* __DataCube__ - Describing basic information about a single FITS file in the system
* __Instrument__ - Describing an instrument with which the FITS file was captured
* __Tag__ - A keyword that can be attached as a classifier to one or more DataCube

## Comments on Ingestion

### Tags

While tags can be assigned arbitrarily in the database model and admin site, the source for what tags should be applied
to a data cube should ideally come from data within that same cube, or data stored wihtin close proximity to the cube.

Having the tags present in the material ingested into the database would make it easy to re-ingest data in the case of
data being re-reduced, or database corruption that cannot be easily solved by restoring from backups.

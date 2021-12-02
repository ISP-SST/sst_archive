# Observations

## Overview

This app provides some of the core models for storing observations in the system, including:

* __Observation__ - Parent Observation model that can group one or more DataCube
* __DataCube__ - Describing basic information about a single FITS file in the system
* __Instrument__ - Describing an instrument with which the FITS file was captured
* __Tag__ - A keyword that can be attached as a classifier to one or more DataCube


## Ingestion

This section provides more details about how data is ingested into the data models contained in this app.

### Tags (Features & Events)

While tags can be assigned arbitrarily in the database model and admin site, the source for what tags should be applied
to a data cube comes from data within that same cube – the `FEATURES` and `EVENTS` keywords in the FITS files.

Having these tags present in the material ingested into the database would make it easy to re-ingest data in the case
the data needs to be re-reduced, or if database corruption affects the database and backups are not recent enough.

A master list of valid features exists (currently deployed on [dubshen](dubshen.astro.su.se/sst_tags/events.txt). These
lists should be used both when the tags are assigned to the data cubes, and when the tags are read during the ingestion
phase. Any tag values that are not present in those lists will not be accepted when ingesting the tags into the
database. 

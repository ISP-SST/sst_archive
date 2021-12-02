# Metadata

## Overview

The Metadata app is the app that most closely matches the corresponding app in the SVO. It primarily hosts the database
model for the entire set of FITS keywords present in the primary header of the data cube (`Metadata`).

Having this kind of data in the database allows end-users to at least view all the keywords present in the FITS file.
Although all of this information is not likely to be useful to end-users, keeping all this information available still
serves a few of purposes:

* It's hard to foresee what data will be interesting to each user. By providing everything it's likely that some users
  will be able to locate information that they otherwise wouldn't have been able to
* Free-form searches can be implemented that, while possibly not optimal in terms of performance, will still allow a
  search feature to be quickly implemented
* If the data needs to be restructured, e.g. extracted into a separate data model, that operation can be performed very
  easily, since the source data is already present in the database

## Ingestion

This section provides more details about how data is ingested into the data models contained in this app.

### Metadata

Metadata is ingested in full in order to allow for complex searches or scenarios where we haven't found a need to create
dedicated database tables for the attributes in question.

Metadata is ingested by transforming the name of each keyword in the FITS header to a format compatible Python member
names. Every transformed keyword is checked to see if it exists in the Metadata model class. If it does it is assigned
to the metadata. Dates are handled as a special case, since they need to be explicitly interpreted as UTC
dates/datetimes.

### FITS header

The FITS header is ingested as text in order to easily extract even more information from the metadata in the future
without needing to reprocess the FITS cubes. This FITS header text is also used to 

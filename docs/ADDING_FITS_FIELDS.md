# Adding fields to FITS headers

## Adding new FITS metadata fields to local database

### 1. Add field to the Metadata model

Update `metadata/models/metadata.py` and add a field with an appropriate
name to model class. FITS header keywords are mapped to model member names
in the following manner:

    DATE-BEG  ->  date_beg
    DW3.CWERR -> dw3_cwerr

All text is transformed to lowercase and characters like ` `, `-`, `.` are
transformed to `_`.

The following field types are supported:

 * `models.DateTimeField`
 * `models.TextField`
 * `models.BigIntegerField`
 * `models.FloatField`

Support for additional field types can be added as need arises.

### 2. Generate the migration scripts

Locally:

    ./manage.py --settings sst_archive.settings.dev makemigrations

On production server:

    sudo -u www-data ./manage.py --settings sst_archive.settings.prod makemigrations

### 3. Migrate the database

Locally:

    ./manage.py --settings sst_archive.settings.dev migrate

On production server:

    sudo -u www-data ./manage.py --settings sst_archive.settings.prod migrate

### 4. Ingest new data (and possibly re-ingest old data)

## Updating the SOLARNET SVO

### 1. Update master lists for keywords

Included in this repo are master lists for each instrument for the 
keywords that the SOLARNET SVO knows about:  

    ingestion/svo/solarnet_metadata_crisp_keywords.json
    ingestion/svo/solarnet_metadata_chromis_keywords.json

These keyword lists need to be updated in order to update the production
database. In the SOLARNET SVO there are two scripts that are used to update
the keywords in the database from a JSON file, and then writing updating
model files from the keywords in the database.

### 2. TBD...
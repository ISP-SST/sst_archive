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

## Updating the SOLARNET Virtual Observatory

### 1. Update master lists for keywords

Included in this repo are master lists for each instrument for the 
keywords that the SVO knows about:  

    ingestion/svo/solarnet_metadata_crisp_keywords.json
    ingestion/svo/solarnet_metadata_chromis_keywords.json

There are two approaches to updating these lists:

 1. Use the script for extracting keywords from one or more FITS files:
    https://github.com/bmampaey/SOLARNET-provider-tools/blob/main/extra/extract_keywords_from_fits.py. Note that just 
    extracting the fields from one FITS file may not yield the exact same field descriptors as what's currently in the
    list. In order to make as small changes as possible to the list you are instead encouraged to merge in the
    descriptors for the new Keywords into the right keywords JSON file in the repo.
 2. You can also manually enter the descriptor for the new field. This is pretty trivial if only a couple of fields were
    added and you know of a similar field of the same type that you can use as the template.

### 2. Submit the new keyword JSON files to the SVO admin

To update the SVO both the Keywords and the Metadata fields will need to be updated in the database. The most
straight forward way of achieving this is by sending the updated Keyword descriptors JSON file to the administrator of 
the SVO, [Benjamin Mampaey](mailto:benjamin.mampaey@oma.be).

# Ingestion

## Overview

This Django app is responsible for bringing the data in the FITS cubes into the database.

### Ingestion endpoints - HTTP and script

The endpoints provided by this app both serve the same purpose - they allow the importing of data contained in a FITS
cube into the database. This app can be seen as the conductor of the ingestion symphony. Most of the ingestion steps are
actually performed in other apps that know more about the data structures that they populate during the ingestion, but
this app ensures that everything is performed in the right order.

To learn more about how a specific ingestion step is performed, see the documentation for that particular app.

Ingestion can be performed with both new data and data that already exists in the database. A full ingestion is executed
in either case, and if data already exists it will just be updated.

The ingestion flow is synchronous, i.e. upon making a request the response will not be sent until the full ingestion has
completed. This is a deliberate decision to keep the code simpler, at least until a more sofisticated solution is
required.

### SVO Synchronization

The building blocks for SVO synchronization are the following management commands:

 * `submit_to_svo` – Submits a single data cube to SVO, possibly updating an existing cube if it already exists in 
                     the SVO.
 * `sync_with_svo` – Performs a full synchronization with the SVO. It uses the local database as the source of truth
                     and...
   - Removes any items in the SVO that don't exist in the local database
   - Adds any items that don't exist in the SVO that do exist in the local database
   - (Optionally updates items that exist both locally and in the SVO)

The `submit_to_svo` steps should be executed as part of the normal ingestion process.

`sync_with_svo` should be performed periodically to pick up on any files that have been removed. It usually makes sense
to not do a full update of all the data in the SVO except for when a major update has been made to local data.  

## Future Work

### Suggested Flow for Asynchronous Ingestion

Assumptions: CHECKSUM is sufficiently unlikely to create collisions that it can be used to detect changes in the file.
This may also be unnecessary if files are always renamed when they are reprocessed. If that's the case, simply checking
the file name for the DataCube with the same OID should be sufficient for gathering finding out if the data has changed.

1. Add ingestion work order to database. Must include all information needed to perform the ingestion asynchronously:
    * DateTime when the order was added
    * Path to FITS file
        * Work order should probably be unique per path. If a new work order comes in for the same file, update the
          existing work order with any new information. (Keep the date though?)
    * Possibly also locations of image/video previews
    * Work order will also automatically be assigned a status (Queued, Started, Completed, Failed)

2. Asynchronously execute the ingestion:
    1. Fetch the oldest non-completed ingestion work order
    2. Fetch the last completed ingestion work order for this DataCube
        1. If flag "force-re-ingest" has been specified this item will be ignored. This will force any future checksum
           comparisons to fail and trigger re-ingestion
    3. First, create or update the basic DataCube in a single transaction (WHY?):
        2. Create/update DataCube
        3. If data access model instances exist:
            1. Check if the CHECKSUM of the primary HDU has changed compared to last completed work order
            2. If yes, update the data access model instances
            3. Update CHECKSUM in current work order
        4. Else:
            1. Create new data access model instances
    4. Ingest FITS header string:
        1. If last completed work order CHECKSUM for primary HDU is equal to ingested current CHECKSUM, skip ingestion
        2. Update the header string
    5. Ingest metadata:
        1. If last completed work order CHECKSUM for primary HDU is equal to ingested current CHECKSUM, skip ingestion
        2. Update the metadata
    6. Ingest image/video previews:
        1. Process source images and generate thumbnails and previews in suitable sizes.
    7. Update checksums in work order

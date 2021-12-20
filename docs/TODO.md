# TODO List

## Leftover Tasks

### Deploy tags support

 * Update the SST archive Metadata model class with new FEATURES and EVENTS properties
 * Update the SVO with the new keywords FEATURES and EVENTS
 * Re-ingest data already in the database (see the `reingest_all_cubes` management command)
 * Add the search input for Features to the search form again
 * (Optional: Implement synchronization of Feature with SVO)

### Synchronize with SVO

 * Add ingestion of FITS file to SSTRED export step
 * Update the documentation at https://dubshen.astro.su.se/wiki/index.php/Science_data
 * Change defaults to enable uploading to SVO by default when ingesting
 * Set up periodical SST Archive --> SVO sync
 * Document periodical synchronization job

### Move to own subdomain?

 * Configure the new subdomain
 * Start serving the existing service over the new subdomain
 * Ensure that new subdomain has a proper TLS certificate
 * Update the Site information in the Django admin interface
 * Add re-directs from the old site location to the new location
 * Re-synchronize SVO with the database (update all data locations to point to the new site)

## Possible Future Work

 * Move to JS-based SPA?
   - Expanded backend API
   - "Pure" JavaScript frontend
 * Add secondary image + video preview (wings)
 * Search by region in solar disk
 * Show region in solar disk in observation details
 
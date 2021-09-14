# SST Archive Prototype

## Overview

This is a repo containing a prototype of a searchable database of the science data produced using the SST.

The idea behind this prototype is to:
 
 * Get a better understanding for what this kind of searchable database entails
 * Clarify the features this kind of system should provide
 * Learn more about the technical aspects around science data from observations (what FITS cubes contain, etc.)

## Getting Started

NB: These instructions haven't yet been validated.

The quickest way to get the system up and running:

    # Create a Python3 virtual environment and activate it
    python3 -m venv venv
    . ./venv/bin/activate
    
    # Install Python dependencies into the virtual environment
    pip install -r requirements.txt

    # Create the database
    ./manage.py makemigrations
    ./manage.py migrate

    # Create your own super user to access the admin portal
    ./manage.py createsuperuser --username <YOUR-USERNAME> --email <YOUR-EMAIL>
    
    # Run the server
    ./manage.py runserver --insecure

That should get the service up and running. But you won't see any data since it hasn't yet
been ingested into the database. To do that, you need to have access to some FITS cubes.

If you only have access to a couple of FITS cubes you can use the `ingest_fits_cube` Django
management command:

    ./manage.py ingest_fits_cube -f <PATH-TO-FITS-CUBE> [--generate-image-previews --generate-animated-previews]

If you happen to have access to the entire `/storage/science_data` folder on `dubshen` mounted on your local drive then
you can use the `ingest_test_data.sh` script. Just make sure to change the BASE_DIR defined in the beginning of that
file to the location of the root of the `science_data` folder. Ingesting all of it and generating all the previews will
take quite some time. If you skip the previews the ingestion should only take a minute or so.

# Local Development

## Getting Started

### Requirements

The service requires:

 * Python >= 3.7
 * ffmpeg
 * libmariadbclient-dev

Have a look a `apt-dependencies.txt` to see the system dependencies that are required in order to get the database up
and running. On a Debian-like system you should be able to install the dependencies listed therein using:

    apt-get install < apt-dependencies.txt

### Setting Up the Service

The quickest way to get the service up and running is by using the development configuration. The dev config uses SQLite
as the database backend and is therefore quicker to get started with:

    # Create a Python3 virtual environment and activate it
    python3 -m venv venv
    . ./venv/bin/activate
    
    # Install Python dependencies into the virtual environment
    pip install -r requirements.txt

    # Create the database
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py collectstatic --noinput
    ./manage.py createcachetable

    # Create your own super user to access the admin portal
    ./manage.py createsuperuser --username <YOUR-USERNAME> --email <YOUR-EMAIL>
    
    # Run the server
    ./manage.py runserver --settings sst_archive.settings.dev --insecure

That should get the service up and running. But you won't see any data since it hasn't yet been ingested into the
database. To do that, you need to have access to some FITS cubes.

If you only have access to a couple of FITS cubes you can use the `ingest_fits_cube` Django management command:

    ./manage.py ingest_fits_cube -f <PATH-TO-FITS-CUBE> [--generate-image-previews --generate-animated-previews]

If you happen to have access to the entire `/storage/science_data` folder on `dubshen` mounted on your local drive then
you can use the `ingest_test_data.sh` script. Just point the script to the `science_data/` root directory. Ingesting all
of it and generating all the previews usually takes a few minutes.
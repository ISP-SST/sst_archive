# Deployment

## Deploying changes to the service

    # Commit or merge your changes into master.

    # SSH into the server.
    ssh dubshen.astro.su.se`

    # Navigate to where the service is hosted.
    cd /srv/www/dubshen/sst_archive/`

    # master branch is checked out on the server.
    # Feth the latest changes.
    git pull

    # If changes have been made to the database schemas,
    # migrate the database.
    sudo -u www-data ./scripts/manage_prod.sh migrate

    # If changes have been made to the static files, collect
    # them as well.
    sudo -u www-data ./scripts/manage_prod.sh collectstatic

    # Restart the Apache configuration to ensure that the latest
    # code is picked up correctly.
    sudo apachectl graceful

## Secrets

Secrets such as API keys, passwords, etc. are not stored in the settings file. Instead, these secrets must be stored in
a file called `secrets.json` in the project root. A template for this JSON file can be found in
[secrets.template.json](../secrets.template.json). Note that this file must exist and contain the specified secrets in
order for the service to run.  

For security reasons the `secrets.json` file should have reduced permissions, only granting read permissions to the 
owner and group.

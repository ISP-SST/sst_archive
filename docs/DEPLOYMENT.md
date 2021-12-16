# Deployment

## Deployment Configuration

### Django Settings Files

Base configuration is provided in the [settings/\_\_init\_\_.py](../sst_archive/settings/__init__.py), and can be
overridden in the active environment's settings file (i.e. [prod.py](../sst_archive/settings/prod.py) or
[dev.py](../sst_archive/settings/dev.py)).

### Database Configuration

The Stockholm SST Archive relies on the existence of a SQL database to store information about observational data. The
database needs to be supported by one of the Django database backends. So far only two databases have been tested –
MariaDB (MySQL) and SQLite.

The database is configured in standard Django fashion in the [settings files](../sst_archive/settings/). Sensitive
information such as the database password is being fetched from the [secrets.json file](#secrets).

### Outgoing Email Server Configuration

In order to send email verification messages the archive needs to be able to send e-mails. The archive uses Django's
built-in facilities to do just that, and also a properly configured e-mail backend. The backend is usually an SMTP
server that is accessible from the server hosting the archive. Username and password for the e-mail server are kept in
the [secrets.json file](#secrets).

### reCAPTCHA

Signups in the archive are guarded by the Google reCAPTCHA service. Integrating reCAPTCHA into a site requires
a corresponding site configuration to be created in the reCAPTCHA developer portal. A site key and a secret key needs
to be copied from the developer portal into the [secrets.json file](#secrets).

### Deployment Path

If the service needs to be deployed in a sub path of the host, the `PATH_ROOT` setting needs to be set properly. For
example, if the service is deployed at `www.myhost.com/sst_archive/` then the settings file should contain
`PATH_ROOT = '/sst_archive'`.

### SVO Sync Configuration

The archive can perform synchronization with the SOLARNET Virtual Observatory to ensure that its contents are kept in
up-to-date with the archive. Required configuration keys are `SVO_API_URL`, `SVO_USERNAME` and `SVO_API_KEY`.
`SVO_USERNAME` and `SVO_API_KEY` are in turn fetched from the [secrets file](#secrets).

### Science Data Location

For security reasons all science data needs to located somewhere inside single top level directory. The location of
this directory is specified in the `SCIENCE_DATA_ROOT` setting.

## Secrets

Secrets such as API keys, passwords, etc. are not stored in the settings file. Instead, these secrets must be stored in
a file called `secrets.json` in the project root. A template for this JSON file can be found in
[secrets.template.json](../secrets.template.json). Note that this file must exist and contain the specified secrets in
order for the service to run.  

For security reasons the `secrets.json` file should have reduced permissions, only granting read permissions to the 
owner and group.

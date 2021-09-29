# Ingestion

This Django app is responsible for bringing the data in the FITS cubes into the database.

It also does some processing of the data, such as generating static and animated image previews.

## Plans

### Ingestion endpoint

The actual ingestion endpoint can be exposed as either an executable admin script (like right now) or be made into an
HTTP endpoint.

Pros and cons of the different solutions

#### Script

Pros:

* Access control is simple (user with script execution permissions).

Cons:

* Harder to perform, requires SSH:ing into the machine and then calling the script.
* Passing arguments becomes trickier if the payload is more than just the name of the FITS cube.

#### HTTP

Pros:

* Format offers simple passing of arbitrary payloads
* Easily callable from any host

Cons:

* Needs additional access control. At least IP whitelisting, possibly also an API key.
* Requires pure API endpoints

#### Decision

Go with HTTP endpoint in the long run.

### Ingestion Architecture

The practical implementation should be implemented in a modular fashion where it's easy to introduce additional content. 

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

Go with HTTP endpoint in the long run, but use the script during prototype phase. 

### Ingestion Architecture

The implementation should be modular in a fashion where it's easy to introduce additional content. 

Some of the known items we need to ingest:

#### Metadata

Metadata is ingested in full in order to allow for complex searches or scenarios where we haven't found a need to
create dedicated database tables for the attributes in question.

Metadata can be ingested by transforming the name of each keyword in the FITS header to a format compatible Python
member names. Every transformed keyword is checked to see if it exists in the Metadata model class. If it does it is
assigned to the metadata. Dates are handled as a special case, since they need to be explicitly interpreted as UTC. 

#### Preview images/animations

TBD

#### Features (tags)

A list of valid features likely needs to be available before the ingestion process is started so that the user can
choose from this list (or create a new tag) rather than opening things up for users to inventing their own terminology
and variations on spelling.

#### FITS header

The FITS header is ingested as text in order to easily extract even more information from the metadata in the future
without needing to reprocess the FITS cubes. 

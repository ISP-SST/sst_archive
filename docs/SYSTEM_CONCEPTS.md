# System Concepts

## Administration Interface and User Statuses

An admin interface is available at `${SITE_ROOT}/admin`. This is where almost all administrative tasks will be
performed. Any manual updates to the database should go through this interface rather than through manual SQL queries.
The system has additional checks and balances in place to ensure data validity and consistency that are not bypassed
when using the admin interface.

To be able to access the admin interface a user must be given the `Staff` status. Only users with this
flag can sign in to the admin interface. In addition to the `Staff` status, the user can also be given `Superuser`
status. With this status the user automatically has all permissions in the system and can make any changes in the admin
interface. This status should only be assigned to people who actively work closely with developing or administrating
the system.

## Observation Data

Observation data is stored in the database in a tree like structure. The following list describes the relationships
between the different data models stored in the database:

```
- Observation #1
   |- Data Cube #1
   |   |- Tags
   |   |- Image Preview
   |   |- Video Preview
   |   |- R0 Data
   |   |- Spectral Line Data
   |- Data Cube #2
       |- Tags
       |- Image Preview
       |- Video Preview
       |- ...
- Observation #2
   |- ...
```

As you can see this hierarchy places `Observations` on the top that groups together Data Cubes, and then as the leaves
of the Data Cubes we find individual pieces of data tied to that data cube. Thanks to the relational structure of the
database models the removal of a Data Cube will also remove any of the pieces of data tied to it.

If you need to make changes to a Data Cube the preferred way is to ensure that the correct data exists in the source
FITS file and then re-ingest that file into the database.

## Permissions and Groups

Users in the system can be assigned to any number of groups. A group can in turn give certain permissions to its
members.

Out of the box the system knows about one specific group: `Swedish User`. This is a special group into which users are
sorted when they are registered as Swedish users. Members of this group  automatically gain access to all data tagged
as Swedish data before it has been released to the public. Under the hood this is achieved by making sure that all data
cubes tagged as Swedish data are also given a `Data cube group grant` that gives the `Swedish User` group access to that
data cube.

It's therefore also possible to create other groups that can access a certain set of data cubes. There is also a
specific permission that can be granted to a user or a group: 
`data_access | data cube user grant | Can access protected data`. Assigning this permission to a group gives the entire
group access to all restricted data.

## Data Cube Access Grants

In addition to the permissions and groups described in the section above, the system can provide users and groups
access to data cubes using grants.

### Data Cube User Grant

Gives a certain user access to a specific data cube.

User grants are given from a specific data cube to a user e-mail.
Since the grant does not reference a "User object" in the database, you will unfortunately not get auto-completion and
the ability to search for the user when entering that field. To upside is, however, that the grant can be specified
even before a user has been created in the system. This makes the following work flow possible:

 1. User exports FITS cube from SSTRED pipeline and submits it to the Archive. User lists their e-mail as the owner of 
    the data
 2. User creates an account in the Archive using the same e-mail address
 3. When the user signs in they will automatically have access to the exported data cube
 
### Data Cube Group Grant

Gives an entire group access to a specific data cube.

These grants can be assigned in one of three ways:

 1. Go to the Group you would like to grant access and add a data cube to that group
 2. Go to the data cube in question and place it inside the Group
 3. Go the `Data cube group grants´ and add a new grant

Either way you do it you will end up with a new entry in the `Data cube group grants´ section.

## Data Ingestion

### Overview

In order to introduce new data into the database, or update existing data, the data needs to got through the ingestion
process. The ingestion process takes a reduced science data FITS cube produced by the SSTRED pipeline and imports
salient data and metadata into the appropriate data models in the database, performing the necessary pre-processing if 
necessary. All data ingested into the database must reside somewhere inside the `${SCIENCE_DATA_ROOT}/` directory. This
directory is specified in the settings file. 

### Ingestion steps

The following data will be ingested:

 * Metadata (FITS headers)
 * Video and image previews
 * Plots and data for plots
 * Data access information

### Ingestion end-points

There are a couple of ways to initiate ingestion of a FITS cube into the database:

 * Posting information about the file location to an HTTP end-point
 * Running the `ingest_fits_cube` management command and providing the same type of information

See more information about this in the corresponding `Tasks` subsections.
 
## SVO Synchronization

The Stockholm SST Archive is responsible for ensuring that the SOLARNET Virtual Observatory contains the same data.

There are two primary primitives that ensure synchronization with the SVO:

### Submit to SVO

_[TODO: SUBMISSION TO SVO IS NOT YET ENABLED BY DEFAULT, REMOVE THIS NOTE WHEN IT IS]_

The `submit_to_svo` management command uploads a specific data cube to the SVO, updating the metadata in the SVO if it
already exists. This runs every time a data cube is ingested into the archive to ensure that new data is immediately
made available in the SVO.

### Sync with SVO

_[TODO: RECURRING SVO SYNCHRONIZATION JOB NOT RUNNING, REMOVE THIS NOTE WHEN IT IS]_

The `sync_with_svo` management ensures that the contents of the SVO matches that of the local archive. The archive is
always seen as the master blueprint:

 * Any data added to the archive that for some reason does not exist in the SVO 
   will be uploaded to the SVO
 * Any data present in the SVO that doesn't exist in archive will be assumed to have been removed from the archive and
   will therefore be removed from the SVO as well

This script is meant to be run recurringly to ensure consistency between local archive and SVO.    
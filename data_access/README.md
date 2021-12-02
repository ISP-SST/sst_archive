# Data Access

## Overview

This application is responsible for:

### Providing download URLs for data cubes
These may require a user to be logged in depending on the release information encoded in the data cube
 * Enabling access control to said data cubes by
 
### Ingesting the release information present in the data cube headers

Information about access control present in the FITS headers (`RELEASE`, `RELEASEC`) is ingested into a
`DataCubeAccessControl` data model instance. This is to enable faster lookup of the information in question and also to enable extending and possibly editing of this information without having to touch the original Metadata

### Defining different types of access grants that can be used to control which users can access the data
 * Data cube group grant – gives any member of a group access to a particular data cube
 * Data cube user grant – gives a specific user access to a particular data cube
 
### Special case for Swedish users
This app introduces a SwedishUserValidationRequest that allows users to request Swedish user status. When such a request
is approved the user will be placed in the Swedish User group. Any DataCubes that have a corresponding
`DataCubeGroupGrant` that links the data cube and the Swedish User group will then be accessible to all users that are
members of the Swedish user group.

# Data Access

## Overview

This application is responsible for:

 * Providing download URLs for data cubes. These may require a user to be logged in depending on the release information encoded in the data cube
 * Enabling access control to said data cubes by:
   * Ingesting the release information present in the data cube headers (`RELEASE`, `RELEASEC`) into `DataCubeAccessControl` structure
   * Defining different types of access grants that can be used to control which users can access the data:
     * Data cube group grant – gives any member of a group access to a particular data cube
     * Data cube user grant – gives a specific user access to a particular data cube
   * Introducing a SwedishUserValdiationRequest that allows users to request Swedish user status. When such a request is approved the user will be placed in the Swedish User group

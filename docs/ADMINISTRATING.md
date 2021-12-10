# Administrating the Stockholm SST Archive

## System Concepts

### Administration Interface

An admin interface is available at `${SITE_ROOT}/admin`. This is where almost all administrative tasks will be
performed. Any manual updates to the database should go through this interface rather than through manual SQL queries.
The system has additional checks and balances in place to ensure data validity and consistency that are not bypassed
when using the admin interface.

### Observation Data

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
       |- ...
- Observation #2
   |- ...
```

As you can see this hierarchy places `Observations` on the top that groups together Data Cubes, and then as the leaves
of the Data Cubes we find individual pieces of data tied to that data cube. Thanks to the relational structure of the
database models the removal of a Data Cube will also remove any of the pieces of data tied to it.

If you need to make changes to a Data Cube the preferred way is to ensure that the correct data exists in the source
FITS file and then re-ingest that file into the database.

### Permissions and Groups

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

### Data cube grants

In addition to the permissions and groups described in the section above, the system can provide users and groups
access to data cubes using grants.

#### Data cube user grant

Gives a certain user access to a specific data cube.

User grants are given from a specific data cube to a user e-mail.
Since the grant does not reference a "User object" in the database, you will unfortunately not get auto-completion and
the ability to search for the user when entering that field. To upside is, however, that the grant can be specified
even before a user has been created in the system. This makes the following work flow possible:

 1. User exports FITS cube from SSTRED pipeline and submits it to the Archive. User lists their e-mail as the owner of 
    the data
 2. User creates an account in the Archive using the same e-mail address
 3. When the user signs in they will automatically have access to the exported data cube
 
#### Data cube group grant

Gives an entire group access to a specific data cube.

These grants can be assigned in one of three ways:

 1. Go to the Group you would like to grant access and add a data cube to that group
 2. Go to the data cube in question and place it inside the Group
 3. Go the `Data cube group grants´ and add a new grant

Either way you do it you will end up with a new entry in the `Data cube group grants´ section.

### Ingesting Data



## Tasks

### Creating a user account

 * Sign in to the admin interface with an admin user
 * Go to the `Users` section
 * Click `Add User +`
 * Enter the following information:
   * _E-mail address_ – Affiliation (University) e-mail address for the user in question.
   * `First name`, `Last name` – Set to user's real first and last name.
   * _Password_ – Generate a new one.
   * _Affiliation_ - Set to the name of the University in question.
   * _Account purpose_ – Get this information from the user or set to empty.
 * Click `Save`

### Creating a University Account

A University Account will be shared between multiple users that belong to that university.

 * Sign in to the admin interface with an admin user
 * Go to the `Users` section
 * Click `Add User +`
 * Enter the following information:
   * _E-mail address_ – Use an organization e-mail address for that university. The e-mail address does not have to be
                        an active account that can receive e-mails if it's supposed to be used by multiple users.
   * _Password_ – Generate a new one.
   * _Affiliation_ - set to the name of the University in question
   * _Account purpose_ – set to "University Account". If the e-mail address is not a personal e-mail, also add contact
                         information to someone who administers this account in the university.
   * Check `Verify e-mail` to ensure that the users of the account don't have to verify the e-mail.
   * Check `E-mail re-verification disabled` so that e-mail re-verification doesn't kick in at a later point in time.
 * Click `Save`

### Manually give access to data cube to an account

 * Sign in to the admin interface with an admin user
 * Go to the `Data cube user grants` section
 * Click `Add data cube user grant +`
 * Enter the following information:
   * `E-mail address` – Provide the e-mail address of the user that will receive access to the Cube.
   * `Data Cube` – Select the cube that you want to grant access to.
 * Click `Save`

### Manually add user to the Swedish User group

 * Sign in to the admin interface with an admin user
 * Go to the `Users` section
 * Find the user in question in the list (using the search feature can be helpful) and click on the username
 * Go to `Permissions -> Groups` 
 * Select the `Swedish User` group in the list and click the right arrow button to move the group over to the
   list of `Chosen groups`
 * Click `Save`
 
## Advanced Tasks


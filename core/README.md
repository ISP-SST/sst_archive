# Core

## Overview

The Core application lays down some fundamental extensions on top of Django and other 3rd party modules:

### Extends the User model with a UserProfile

This model contains additional information about each user in the system.

### Introduces some core auth concepts

Extends the `django-allauth` app, the app responsible for providing a mature sign in solution with e-mail verification,
with an understanding of the concept of e-mail verification expiration. This concept forces any user that is subject to
the re-verification scheme to have to periodically re-verify their e-mail address to check that they still have access
to the e-mail account. The re-verification scheme can be seen as a simplified version of a 2-factor auth system that
leverages the existing e-mail verification system and only requires e-mail verification once every 3 months or so (this
is a setting that can be changed).

### Flexible admin interface extension utility

Allows any inline admin class to easily be added to an existing model admin. This is used to extend the DataCube admin
class with inline admin interfaces for many of the other models that have a One-To-One relationship with a DataCube. The
end result is that editing a DataCube in the admin interface gives immediate editing access to database fields that
aren't part of the DataCube table.

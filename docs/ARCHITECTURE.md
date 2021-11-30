# Stockholm SST Archive - Architecture

## Overview

The architecture has been inspired by the work done on the
[SOLARNET Virtual Observatory](https://github.com/bmampaey/SOLARNET-service). Some of the data modelling ideas are
shared between them, but the code bases are also quite different due to the differences in requirements and purposes of
the services.

The archive is built on top of [Django](https://www.djangoproject.com/) which provides a mature web framework.

## Service Layout

The service is broken up into multiple apps, which is a well-recognized building block of Django-based services. Each
app aims to have a distinct responsibility and can own database models, admin interfaces, views or any callable
functionality that belongs to said feature

Here's a current list of the apps in the system and what their responsibilities are:

| App         | Purpose                      |
|-------------|------------------------------|
| [api](../api/README.md)                   | Provides the basis for an web based API. Currently the API only powers the ingestion end-point, but this can be extended in the future to provide a more feature rich API that would enable, for example, JavaScript SPAs. |
| [core](../core/README.md)                 | This app is responsible for laying some of the ground-work for the rest of the service. This includes extending the User model with additional profile information and integrating the django-allauth auth framework into the service. |
| [data_access](../data_access/README.md)   | The `data_access` app controls user access to download the FITS data cubes that have been ingested by the archive. All downloads must go through this module. |
| [frontend](../frontend/README.md)         | This is the main UI for the application: searching, viewing observation details, sign in/sign out, It's based on the fundamental Django framework primitives of templates and views and provides URL routes for these different views. |
| [ingestion](../ingestion/README.md)       | As implied by the name, this app serves as the main entry-point for ingesting new data into the database. However, it's important to note that the ingestion steps for individual data types is hosted by the app that also owns the data models into which the data will be ingested. |
| [metadata](../metadata/README.md)         | This app hosts the database models for all FITS keywords that are stored in a data cube. |
| [observations](../observations/README.md) | `observations` provides integral database models for representing data cubes: Observation, DataCube, Instrument, Tag. A DataCube belongs to a single Observation and Instrument, and can have any number of Tags assigned to it. |
| [previews](../previews/README.md)         | Provides database models and ingestion scripts for image and video previews of observations, as well as data and preview images of certain plots that can be displayed in the frontend. |
| [search](../search/README.md)             | Small app that exposes a more well-defined search interface that can be used by the frontend app to search and display paginated search results. |

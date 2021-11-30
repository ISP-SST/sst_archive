# Frontend

## Overview

This Django app hosts the majority of the stuff that you see on screen when you use the service.

It uses old-school Django templates to generate static HTML views from queries to the database. This
is not a very modern type of web development and in the future a JavaScript-based frontend together with
a web API could replace this app.

Quick summary of the views provided by the app:
 * Landing page
 * Sign in, sign out, and other account related views. Many of the account related views are only modified in terms of their templates, the underlying functionality is provided by the `django_allauth`
 * Search view with paginated search results
 * Observation details (with plots using the ApexCharts JS library)

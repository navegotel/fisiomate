==================================
Development patterns for fisiomate
==================================

The following views need to be implemented for each data

- list view
- view
- create 
- edit
- delete


1. Create stub handlers in `views.py`
=====================================

The handler name starts with the action, i.e. 

- list
- view (optional)
- add
- edit 
- delete

All views must have at least the following items:

- 'title': "some title string"
- 'main_menu_items': MAIN_MENU_ITEMS
- parent id

2. Create the urls in `urls.py`
===============================

3. Create model in `models.py`
==============================

After model creation `manage.py makemigrations`
and `manage.py migrate needs to be run`

4. Create form in `forms.py`
============================

5. Create form template in templates folder
============================================

6. Create template
==================

list
----

A list or some type of collection of all records related to 
one parent entity, for instance the patient.

The template includes the following link buttons

- **Parent** (optional): There must always be a way to return to the parent. 
- **Add**: Link button that point to the *Create* view 



   
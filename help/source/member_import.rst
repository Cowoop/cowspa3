======================================
Importing member data from CSV files
======================================

Introduction
============
|PRODUCT| can bulk import members data from a CSV (Comma Separated Values) file. 

CSV Specifications
===================
 * Delimiter used is comma "," character.
 * First line is header and describes fields used by rest of lines in the file.
 * Fields with embedded commas must be quoted.

Example CSV file content
-------------------------

::
    
    first_name, last_name, email, short_description, work
    Clark, Kent, kent@example.com, About Clark, +1 11 54321 
    Peter, Parker, pepa@example.com, "He likes web, photography and tall buildings", +1 11 12345


Field details
=============

Here is the list of various fields that can be included in CSV file. Most are self explanatory.

Mandatory fields
----------------


 - first_name
 - last_name
 - email

.. Note ::
    
    Except above three fields all other information below is optional

Contact fields
----------------
 - address
 - city
 - province
     province / state
 - country
 - work
     work phone number
 - home
     home phone number
 - mobile
     mobile number
 - fax
 - skype
 - language

Profile fields
--------------
- short_description
- organization
    Name of Organizarion/Project member is involved in


Optional user account fields
----------------------------
If these are not provided member will receive email with activation instructions

 - username
 - password



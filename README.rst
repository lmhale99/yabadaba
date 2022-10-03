========
yabadaba
========

The yabadaba package (short for "Yay, a base database!") provides a mid-level
abstraction layer for interacting with databases containing JSON/XML equivalent
data records.  The primary purpose of the yabadaba package is to make it easy
to design user-friendly Python packages that can access and store content in a
variety of database types.

In design, the yabadaba package consists of five major components:

1. Database classes that provide pythonic APIs to interact with databases.  A
   base Database class defines common method calls for interacting with the 
   records in a database, such as querying, adding, modifying, and deleting
   entries.   Child classes of Database are then defined that implement the
   universal interaction methods for a given type of database. 

2. A base Record class provides a template for interpreting single database
   entries.  Developers are meant to specify unique Record classes for each
   unique schema that is part of their project.  In this way, users can
   interface with the data both in its raw format and using class-specific
   methods and attributes.  Each Record class also allows for database query
   operations to be defined that allow for filtering of any hosted records
   based on meaningful fields of the Record's schema.

3. A ModuleManager class is defined that helps treat the child classes of
   the Database and Record classes in a modular fashion.  In particular, the
   ModuleManagers allow for the code to work even if there are issues with any 
   of the child classes, and make it possible for packages that import the 
   managers to append their own child classes.

4. Generic query methods are also provided that support the construction of the
   record-specific query operations.  In short, these are meant to allow for
   queries to operate efficiently across all of the database types and ideally
   return identical responses despite the underlying infrastructure
   differences.

5. A Settings class is provided that makes it possible for users to save
   access parameters for a database under a simple name that can then be
   reloaded in a later session.

Package developers that want to provide APIs to any associated databases can
simply import the various components of yabadaba and define their own Record
classes that are specific to their own data.  Users of the resulting packages
can then easily explore the data, make their own copies, etc.


Installation
------------

The yabadaba package can easily be installed using pip or conda-forge

    pip install yabadaba

or 
    conda install -c conda-forge yabadaba

Documentation
-------------

Documentation can be found in the doc folder in the github repository.

For support, post a issue to github or email lucas.hale@nist.gov.
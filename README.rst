========
yabadaba
========

The yabadaba package (short for "Yay, a base database!") is meant to make it
easy to design user-friendly Python packages that can access and store content
in a variety of database types.  This is accomplished by defining mid-level
abstractions of databases and database records.

The conceptual ideas behind yabadaba and what it intends to accomplish are

- FAIR data exists in a variety of open access databases.  While the FAIR
  data principles provide guidelines for how to make the data more accessible
  in general, there are no specifics about standardizing database
  infrastructure, query APIs, or data schemas. This results in a complex
  ecosystem where anyone wishing to access data from such a database must
  become familiar with the data and database infrastructure used.
- Developing, implementing and enforcing standardization of data and databases
  is a complex task that requires agreement with a large number of separate
  entities even within the same community.  Additionally, it may place too
  many limitations on further data evolution and/or be difficult for smaller
  groups to adhere to.
- Alternatively, the problem can be solved at a higher level.  Rather than
  force uniformity at the data level, tools can be developed that are
  capable of transforming data between different representations.  This is
  what yabadaba aims to do.
- By managing database interactions and data transformations, yabadaba makes it
  possible to interact with data from multiple databases and database
  infrastructures in similar ways.  This increases the accessibility of the
  data as users of the data do not need to become experts in every database
  infrastructure and every data schema.

Package design
--------------

The yabadaba package itself is not meant to be an end-user package per-se, but
a toolset for data generators and maintainers to easily create their own
packages that serve as user-friendly APIs to their own data.  To this end,
yabadaba defines a number of base and utility classes that allow those
yadabada-based packages to build upon yabadaba in a modular fashion.

The core base classes defined by yabadaba are

- **Database** defines common method calls for interacting with the 
  records in a database, such as querying, adding, modifying, and deleting
  entries.  Child classes of Database are then defined that implement the
  universal interaction methods for a given database infrastructure.

- **Record** defines methods that allow for the interpretation and
  transformation of a single database entry of a given schema to/from different
  data representations.  Notably, the record interprets the data into python
  values and objects that are easy for users to interact with while also making
  the data accessible in and convertible to different raw storage formats.
  At the bare minimum, child classes of Record specify the data values
  contained within a specific schema so the methods in the base Record class
  can properly work.  One way to think about this is that you create a
  python object to represent and allow users to interact with some of your
  data and you simply allow it to inherit from the base Record class to
  provide the framework for saving and loading the content.

- **Value** defines methods that allow for the interpretation and
  transformation of the component values contained within a record.  Child
  classes of Value specify how to perform those operations for different
  data types and structures, and can specify one or more default query
  operations to build for the value.  Each Record subclass defines a dict of
  Value objects providing a schema for the data and the basis for performing
  the data transformations.

- **Query** defines methods that build database query operations for the
  different database infrastructures.  The child classes of Query focus on one
  specific query operation and define different methods to efficiently perform
  that operation in the different database infrastructures.  Query objects are
  typically associated with Value objects to specify how to query based on the
  values of specific elements in a Record.

- **ModuleManager** provides a common interface for managing the various
  subclasses of Database, Record, Value, and Query in a modular way.  The
  ModuleManager objects dynamically import the subclasses such that they are
  fully integrated with each other and the features of yabadaba.  Packages that
  build on yabadaba can then add their own subclasses to the managers and take
  advantage of yabadaba's capabilities.

- **Settings** provides a means of saving and loading settings across different
  python settings.  Primarily, this is used to store database access and
  authentication information for databases that are frequently used.  This
  class can easily be extended to manage other settings for yadabada-based
  projects.

- **UnitConverter** provides simple tools for managing unit conversions.

Installation
------------

The yabadaba package can easily be installed using pip or conda-forge

    pip install yabadaba

or

    conda install -c conda-forge yabadaba

Documentation
-------------

Documentation and demonstration Notebooks for yabadaba can be found in the
doc folder in the github repository.

For support, post a issue to github or email lucas.hale@nist.gov.
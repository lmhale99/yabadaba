Updates
=======

0.2.1
-----

- Query objects now have a "parameter_type" attribute to indicate what type
  of value should be given to the associated Python method parameter.  The
  query doc string methods now include this information.
- A database parameter has been added to the Records allowing for any record
  object to have a default database to fetch additional content from.  This
  allows for more interactive methods to be developed.  The database value
  is automatically set to a record when using database.get_record operations.
  NOTE: This may require Record subclasses to add database to their init
  methods.
- Base Record now has a tar attribute that provides an open TarFile object for
  the record's associated tar archive.  When first accessed, this will use the
  database to retrieve the tar contents.  Subsequent calls then interact with
  the already downloaded content.
- Base Record also has a new get_file() method that retrieves a file from the
  record's associated tar file simply by giving the file name.  This builds on
  the tar attribute above, so getting files in this way is both convenient and
  efficient.

0.2.0
-----

- UnitConverter class added in as part of the project. Necessary to handle
  unit conversions from records that store values with units.
- Query operations now fully managed by Query objects rather than functions.
- Mongo query builders should work for more general cases now.
- FloatMatchQuery added for comparing float values with/without units and
  within a tolerance.
- Methods added to both record and database objects to view query docs.

0.1.3
-----

- This version fixes a critical bug associated with function parameter order
  with calls to load_record.
- tqdm progress bars now added to certain methods.
- Starting to add more utility methods to the Database classes to help with
  large numbers of records. Unfortunately, this is also resulting in some
  divergence as these useful methods are not implemented in all database styles
  yet.

0.1.2
-----

- Minor updates, plus some typing hints added to the code.
- Tests have been added for some parts but not all.

0.1.1
-----

- Bug fix

0.1.0
-----

- Initial release. Code branched off from the potentials package and Query objects created.
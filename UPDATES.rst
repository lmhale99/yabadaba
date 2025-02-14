Updates
=======

0.3.0
-----
- Value objects have been added that greatly reduce the amount of coding needed
  to define a record as data transformation and interaction methods can now be
  auto-built using the defined Values.  Extensive code updates integrating
  the Value objects into the package and defining all the fancy magical stuff
  that happens.
- DummyQuery added that returns True or False by comparing a given value to a
  set constant value rather than performing a query.  Useful if the same query
  operations are allowed on multiple schemas where the term being queried is
  not a variable in all schemas.
- Record.display_image() added that will access an image file from the record's
  tar and display it.
- The code in yabadaba.demo has been moved from yabadaba into doc to avoid code
  pollution in the main package.
- All docs have been created and updated describing the new version of the
  package.
- Probably other changes and bug fixes, but not sure which are fixes to the old
  code and what are associated with the major Value object overhaul. 

0.2.2
-----

- A count_records() method added to all Database styles that gives a count of
  all matching records.
- CDCSDatabase add_record() and update_record() have additional parameter
  auto_set_pid_off that turns off the auto_set_pid setting when uploading new
  record contents to avoid URL assignment issues.
- Bug fix with UnitConverter when setting working units with an energy value.
- Bug fix with get_tar() that now correctly returns tar contents.
- Depreciation fixes for IPython and pandas.
- Typing should be added to all method headers.

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
- CDCSDatabase - bug fix for get_records() with no matches.
- Compatibility updates for python 3.11 

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
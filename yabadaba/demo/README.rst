----------
Demo files
----------

The files in this directory are meant to provide a demonstration of how to
build Record objects and link them to the recordmanager.

- FAQ.py defines an example FAQ Record class.  It is meant to serve as a simple
  example as the data model itself only has two fields: a question and an answer.

- FAQ.xsd provides a XML schema for the FAQ Record's data model.

- FAQ.xsl gives an example transformation of the XML to HTML.

- BadRecord.py defines an example BadRecord that is used by the demo to show
  how the recordmanager (and other ModuleManager objects) handles modules that
  fail to import. 
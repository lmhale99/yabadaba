# Standard Python libraries
import sys
from importlib import import_module, resources
from typing import Any

class ModuleManager():
    """
    Base class for managing module subclasses
    """
    def __init__(self,
                 parentname: str):
        """
        Creates a ModuleManager object

        Parameters
        ----------
        parentname : str
            Name of the parent class.  Used solely for messages.
        """
        
        self.__parentname = parentname
        self.__loaded_styles = {}
        self.__failed_styles = {}

    def import_style(self,
                     style: str,
                     modulename: str,
                     package: str | None = None,
                     classname: str | None = None):
        """
        Tries to import a modular class and appends the results to loaded_styles or
        failed_styles accordingly.

        Parameters
        ----------
        style : str
            The style name to associate with the modular class.
        modulename : str
            The name of the module to try to import.
        package : str, optional
            The name of the package which is to act as the anchor for resolving
            relative package names.
        classname : str, optional
            The name of the class in the imported module to associate with
            the style.  If not given, will use either the first value in the
            module's __all__ if it exists, or the final name of the modulename
            path if it does not.
        """ 
        try:
            # Load module
            module = import_module(modulename, package=package)

            if classname is None:
                if hasattr(module, '__all__') and len(module.__all__) > 0:
                    # Get class name from __all__
                    classname = str(module.__all__[0])
                else:
                    # Get class name from module name
                    classname = modulename.split('.')[-1]
            
            # Load object
            obj = getattr(module, classname)
        
        except Exception as e:
            self.failed_styles[style] = '%s: %s' % sys.exc_info()[:2]
        else:
            self.loaded_styles[style] = obj

    def dynamic_import(self,
                       package: str,
                       ignorelist: list | None = None,
                       styleprefix: str = ''):
        """
        Automatically finds all submodules of a given package and calls
        import_style() on the submodule and the primary class within it.
        The style name is taken as the submodule's name.  The primary class
        should be indicated by defining the __all__ list in the submodule and
        making the first term the class's name.

        Parameters
        ----------
        package : str
            The root package where the submodules to import are located.
        ignorelist : list or None, optional
            A list of content (without file extensions) inside the module that
            should be ignored.  Default value of None will ignore only
            __pycache__ and __init__.
        styleprefix : str, optional
            An optional prefix to add to the style name. 
        """
        if ignorelist is None:
            ignorelist = ['__pycache__', '__init__']
        
        for resource in resources.files(package).iterdir():
            # Check that resource is a folder, .py file or .pyc file
            if resource.is_dir():
                modulename = resource.name
            elif resource.is_file():
                if resource.name.endswith('.py'):
                    modulename = resource.name[:-3]
                elif resource.name.endswith('.pyc'):
                    modulename = resource.name[:-4]
                else:
                    continue
            
            # Skip anything in the ignore_list
            if modulename in ignorelist:
                continue

            # Add style prefix
            style = f'{styleprefix}{modulename}'

            # Attempt to import the submodule
            self.import_style(style, f'.{modulename}', package)

    @property
    def parentname(self) -> str:
        """str : The name of the parent class (used for messages)"""
        return self.__parentname

    @property
    def loaded_styles(self) -> dict:
        """dict : The styles that were successfully imported.  Values are the loaded modules"""
        return self.__loaded_styles
    
    @property
    def failed_styles(self) -> dict:
        """dict : The styles that were unsuccessfully imported.  Values are the error messages"""
        return self.__failed_styles
    
    @property
    def loaded_style_names(self) -> list:
        """list : The names of the loaded styles"""
        return list(self.loaded_styles.keys())

    @property
    def failed_style_names(self) -> list:
        """list : The names of the loaded styles"""
        return list(self.failed_styles.keys())
    
    def check_styles(self):
        """
        Prints the list of styles that were successfully and
        unsuccessfully loaded.
        """
        print(f'{self.parentname} styles that passed import:')
        for style in self.loaded_style_names:
            print(f'- {style}: {self.loaded_styles[style]}')

        print(f'{self.parentname} styles that failed import:')
        for style in self.failed_style_names:
            print(f'- {style}: {self.failed_styles[style]}')
        print()

    def assert_style(self,
                     style: str):
        """
        Checks if the style successfully loaded, throws an error otherwise.
        
        Parameters
        ----------
        style : str
            The style name to check.

        Raises
        ------
        ImportError
            If the style is found in failed_styles
        KeyError
            If the style is not found in either loaded_styles or failed_styles
        """
        if style in self.failed_style_names:
            raise ImportError(f'{self.parentname} style {style} failed import: {self.failed_styles[style]}')
        elif style not in self.loaded_style_names:
            raise KeyError(f'Unknown {self.parentname} style {style}')

    def get_class(self,
                  style: str) -> type[Any]:
        """
        Retrieves the class of the given style.

        Parameters
        ----------
        style : str
            The style name.

        Returns
        -------
        class
            The uninitialized class.
        """
        self.assert_style(style)
        return self.loaded_styles[style]

    def init(self,
             style: str,
             *args,
             **kwargs):
        """
        Initializes an object of the given style.

        Parameters
        ----------
        style : str
            The style name.
        *args : any
            Any additional position-based arguments for the subclass being
            created.  RECOMMENDED TO USE KWARGS OVER ARGS!!!
        **kwargs : any
            Any additional keyword arguments for the subclass being created.
        Returns
        -------
        Object
            The initialized object.
        """
        self.assert_style(style)
        return self.loaded_styles[style](*args, **kwargs)
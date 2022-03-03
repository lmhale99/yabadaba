import builtins
from unittest.mock import patch
import shutil
from pathlib import Path

from pytest import raises

import yabadaba


class TestSettings():

    @property
    def directoryname(self):
        """str : The directoryname value used for initialization"""
        return 'yabadaba_testing'
    
    @property
    def fname(self):
        """str : The filename value used for initialization"""
        return 'yabadaba_testing_settings.json'

    @property
    def defaultdirectory(self):
        """Path : What the defaultdirectory value should be"""
        return Path(Path.home(), self.directoryname)

    @property
    def directory(self):
        """Path : What the directory value should be"""
        return self.__directory

    @directory.setter
    def directory(self, value):
        self.__directory = Path(value).resolve()

    @property
    def defaultfilename(self):
        """Path : What the defaultfilename value should be"""
        return Path(self.defaultdirectory, self.fname)

    @property
    def filename(self):
        """Path : What the filename value should be"""
        return Path(self.directory, self.fname)

    @property
    def settings(self):
        """yabadaba.Settings.Settings : A settings object to use for testing"""
        if self.defaultdirectory.exists():
            shutil.rmtree(self.defaultdirectory)
        return yabadaba.Settings.Settings(directoryname=self.directoryname,
                                          filename=self.fname)
        
    def test_initial(self):
        """Initial testing"""

        # Initialize a settings object
        settings = self.settings

        # Check status of settings attributes
        assert settings.directory == self.defaultdirectory
        assert settings.defaultdirectory == self.defaultdirectory 
        assert settings.filename == self.defaultfilename
        assert settings.defaultfilename == self.defaultfilename
        assert settings.list_databases == []
        assert settings.databases == {}

        # Cleanup
        if self.defaultdirectory.exists():
            shutil.rmtree(self.defaultdirectory)

    def test_databases(self):
        """Test setting and unsetting databases"""

        # Initialize a settings object
        settings = self.settings

        # Build content dict for comparison
        content = {}

        # Set a database with required terms
        settings.set_database('pytest1', 'local', 'nowhere', key='no')
        
        # Update the comparison content
        content['database'] = {}
        content['database']['pytest1'] = {'style': 'local', 'host': 'nowhere', 'key': 'no'}

        # Check status of settings attributes
        assert settings.list_databases == ['pytest1']
        assert settings.databases['pytest1'] == content['database']['pytest1']

        # Check set database with missing name
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'pytest2'
            settings.set_database(style='local', host='somewhere', key='yes')
        
        # Update the comparison content
        content['database']['pytest2'] = {'style': 'local', 'host': 'somewhere', 'key': 'yes'}
        
        # Check status of settings attributes
        assert settings.list_databases == ['pytest1', 'pytest2']
        assert settings.databases['pytest2'] == content['database']['pytest2']

        # Check set database with missing style
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'mongo'
            settings.set_database(name='pytest3', host='everywhere', key='maybe')

        # Update the comparison content
        content['database']['pytest3'] = {'style': 'mongo', 'host': 'everywhere', 'key': 'maybe'}

        # Check status of settings attributes
        assert settings.list_databases == ['pytest1', 'pytest2', "pytest3"]
        assert settings.databases['pytest3'] == content['database']['pytest3']

        # Check set database with missing host
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'elsewhere'
            settings.set_database(name='pytest4', style='cdcs', key='maybe')

        # Update the comparison content
        content['database']['pytest4'] = {'style': 'cdcs', 'host': 'elsewhere', 'key': 'maybe'}

        # Check status of settings attributes
        assert settings.list_databases == ['pytest1', 'pytest2', 'pytest3', 'pytest4']
        assert settings.databases['pytest4'] == content['database']['pytest4']

        # Check set database with missing key
        with patch('builtins.input') as mock_input:
            mock_input.return_value = ''
            settings.set_database(name='pytest5', style='cdcs', host='here')
        settings.set_database(name='pytest6', style='local', host='there', prompt=False)

        # Update the comparison content
        content['database']['pytest5'] = {'style': 'cdcs', 'host': 'here'}
        content['database']['pytest6'] = {'style': 'local', 'host': 'there'}

        # Check status of settings attributes
        assert settings.list_databases == ['pytest1', 'pytest2', 'pytest3', 'pytest4', 'pytest5', 'pytest6']
        assert settings.databases['pytest5'] == content['database']['pytest5']
        assert settings.databases['pytest6'] == content['database']['pytest6']

        # Test that prompt = False fails for missing values
        with raises(TypeError):
            settings.set_database(style='local', host='nowhere', key='no', prompt=False)
        with raises(TypeError):
            settings.set_database(name='asf', host='nowhere', key='no', prompt=False)
        with raises(TypeError):
            settings.set_database(name='asf', style='local', key='no', prompt=False)
        
        # Test updating existing settings with negative confirmation
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'no'
            settings.set_database('pytest1', 'mongo', 'nowhere', key='no')
        assert settings.databases['pytest1'] == content['database']['pytest1']
        
        # Test updating existing settings with invalid confirmation
        with raises(ValueError):
            with patch('builtins.input') as mock_input:
                mock_input.return_value = 'ag'
                settings.set_database('pytest1', 'mongo', 'nowhere', key='no')

        # Test updating existing settings with positive confirmation
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'yes'
            settings.set_database('pytest1', 'mongo', 'nowhere', key='no')
        content['database']['pytest1'] = {'style': 'mongo', 'host': 'nowhere', 'key': 'no'}
        assert settings.databases['pytest1'] == content['database']['pytest1']

        # Test updating existing settings without prompt confirmation
        settings.set_database('pytest1', 'cdcs', 'nowhere', key='no', prompt=False)
        content['database']['pytest1'] = {'style': 'cdcs', 'host': 'nowhere', 'key': 'no'}
        assert settings.databases['pytest1'] == content['database']['pytest1']

        # Test unsetting databases
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'yes'
            settings.unset_database('pytest1')
        assert settings.list_databases == ['pytest2', 'pytest3', 'pytest4', 'pytest5', 'pytest6']

        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'no'
            settings.unset_database('pytest2')
        assert settings.list_databases == ['pytest2', 'pytest3', 'pytest4', 'pytest5', 'pytest6']

        settings.unset_database('pytest4', prompt=False)
        assert settings.list_databases == ['pytest2', 'pytest3', 'pytest5', 'pytest6']

        with raises(ValueError):
            settings.unset_database('badname')

        settings.unset_database('pytest2', prompt=False)
        settings.unset_database('pytest3', prompt=False)
        settings.unset_database('pytest5', prompt=False)
        settings.unset_database('pytest6', prompt=False)
        assert settings.content == {}

        # Cleanup
        if self.defaultdirectory.exists():
            shutil.rmtree(self.defaultdirectory)

    def test_directory(self, tmpdir):
        
        # Initialize a settings object
        settings = self.settings
        self.directory = tmpdir

        # Set a database for testing purposes
        settings.set_database('pytest1', 'local', 'nowhere', key='no')
        assert settings.list_databases == ['pytest1']

        # Set directory and move
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'yes'
            settings.set_directory(tmpdir, move=True)

        # Check status of settings attributes
        assert settings.directory == self.directory
        assert settings.defaultdirectory == self.defaultdirectory 
        assert settings.filename == self.filename
        assert settings.defaultfilename == self.defaultfilename
        assert settings.list_databases == ['pytest1']
        
        # Set a database for testing purposes
        settings.set_database('pytest2', 'local', 'nowhere', key='no')
        assert settings.list_databases == ['pytest1', 'pytest2']

        # unset directory and move
        with patch('builtins.input') as mock_input:
            mock_input.return_value = 'yes'
            settings.unset_directory(move=True)

        # Check status of settings attributes
        assert settings.directory == self.defaultdirectory
        assert settings.defaultdirectory == self.defaultdirectory 
        assert settings.filename == self.defaultfilename
        assert settings.defaultfilename == self.defaultfilename
        assert settings.list_databases == ['pytest1', 'pytest2']
        assert not self.filename.is_file()

        # Set directory without move
        settings.set_directory(tmpdir, move=False, prompt=False)
        
        settings.set_database('pytest3', 'local', 'nowhere', key='no')

        # Check status of settings attributes
        assert settings.directory == self.directory
        assert settings.defaultdirectory == self.defaultdirectory 
        assert settings.filename == self.filename
        assert settings.defaultfilename == self.defaultfilename
        assert settings.list_databases == ['pytest3']

        # Error for unset+move when default location contains settings 
        with raises(ValueError):
            settings.unset_directory(move=True, prompt=False)

        # Unset without move
        settings.unset_directory(move=False, prompt=False)

        # Check status of settings attributes
        assert settings.directory == self.defaultdirectory
        assert settings.defaultdirectory == self.defaultdirectory 
        assert settings.filename == self.defaultfilename
        assert settings.defaultfilename == self.defaultfilename
        assert settings.list_databases == ['pytest1', 'pytest2']

        # Error for set+move when new location contains settings
        with raises(ValueError):
            settings.set_directory(tmpdir, move=True, prompt=False)

        # Cleanup
        if self.defaultdirectory.exists():
            shutil.rmtree(self.defaultdirectory)
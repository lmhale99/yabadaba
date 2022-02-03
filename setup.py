from setuptools import setup, find_packages

def getreadme():
    with open('README.rst') as readme_file:
        return readme_file.read()

def getversion():
    """Fetches version information from VERSION file"""
    with open('yabadaba/VERSION') as version_file:
        return version_file.read().strip()

setup(name = 'yabadaba',
      version = getversion(),
      description = 'Yay, a base database! An abstraction layer allowing for common interactions with Mongo, CDCS and local directory databases and records.',
      long_description = getreadme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      keywords = [
        'database', 
        'mongodb', 
        'CDCS',
      ], 
      url = 'https://github.com/usnistgov/yabadaba',
      author = 'Lucas Hale',
      author_email = 'lucas.hale@nist.gov',
      packages = find_packages(),
      install_requires = [
        'lxml',
        'DataModelDict',
        'IPython',
        'numpy', 
        'pandas',
        'cdcs>=0.1.5',
        'pymongo'
      ],
      package_data={'': ['*']},
      zip_safe = False)
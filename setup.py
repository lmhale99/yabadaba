from setuptools import setup, find_packages

def getreadme():
    """Fetches long description from the README file"""
    with open('README.rst', encoding='utf-8') as readme_file:
        return readme_file.read()

def getversion():
    """Fetches version information from VERSION file"""
    with open('yabadaba/VERSION', encoding='utf-8') as version_file:
        return version_file.read().strip()

setup(name = 'yabadaba',
      version = getversion(),
      description = 'Yay, a base database! An abstraction layer allowing for common interactions with Mongo, CDCS and local directory databases and records.',
      long_description = getreadme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
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
        'cdcs>=0.2.4',
        'pymongo',
        'tqdm',
        'pillow'
      ],
      package_data={'': ['*']},
      zip_safe = False)

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


DESCRIPTION = "Activity Timer: Help manage your day"

LONG_DESCRIPTION = read("README.md")
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

DISTNAME = 'activity-timer'
MAINTAINER = 'Sean Martin'
MAINTAINER_EMAIL = 'martins7@tcd.ie'
URL = 'https://github.com/seankmartin/ActivityTimer'
DOWNLOAD_URL = 'https://github.com/seankmartin/ActivityTimer/archive/0.12.tar.gz'
VERSION = '0.12'

INSTALL_REQUIRES = [
    'pandas',
    'pyqt5 >= 5.9.2'
    'openpyxl'
]

PACKAGES = [
    'code_time',
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

]

from setuptools import setup

if __name__ == "__main__":

    setup(name=DISTNAME,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          install_requires=INSTALL_REQUIRES,
          include_package_data=True,
          packages=PACKAGES,
          classifiers=CLASSIFIERS,
          )

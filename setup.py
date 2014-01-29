from setuptools import setup, find_packages
import os

version = '0.1.1'

try:
    readme = open('README.rst').read()
    readme = readme.replace('.. image:: _static', '.. figure:: https://github.com/collective/eea.facetednavigationtaxonomiccheckbox/raw/master/docs/_static')
except:
    readme = ''

try:
    changelog = open('CHANGES.txt').read()
except:
    changelog = ''

long_description = (
    readme
    + '\n' +
    #'Contributors\n'
    #'============\n'
    #+ '\n' +
    #open('CONTRIBUTORS.txt').read()
    #+ '\n' +
    changelog
+ '\n')

setup(
    name = 'eea.facetednavigationtaxonomiccheckbox',
    version = version,
    description = "Taxonomic tags in EEA Faceted Navigation.",
    long_description = long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords = 'taxonomic tags, nested tags, eea.facetednavigation',
    author = 'Goldmund, Wyldebeast & Wunderliebe',
    author_email = 'info@gw20e.com',
    url = 'https://github.com/collective/eea.facetednavigationtaxonomiccheckbox',
    license = 'GPL 2.0',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['eea',],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        # -*- Extra requirements: -*-
        'redomino.advancedkeyword>=1.4',
        'eea.facetednavigation>=6.7',
    ],
    extras_require = {'test': ['plone.api', 'plone.app.testing', 'robotsuite', 'Products.PloneTestCase',]},
    entry_points = """
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
    """,
)

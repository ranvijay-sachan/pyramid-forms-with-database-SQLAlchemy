from setuptools import setup

requires = [
    'pyramid',
    'pyramid_chameleon',
    'deform',
    'sqlalchemy',
    'pyramid_tm',
    'zope.sqlalchemy'
]

setup(name='test',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = test:main
      [console_scripts]
      initialize_test_db = test.initialize_db:main
      """,
)
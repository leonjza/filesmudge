from setuptools import setup

setup(
    name='filesmudge',
    version='0.1',
    py_modules=['smudge'],
    install_requires=[
        'Click', 'python-magic'
    ],
    entry_points='''
        [console_scripts]
        filesmudge=smudge:cli
    '''
)

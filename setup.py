from setuptools import setup

setup(
    name='filesmudge',
    description='A silly file \'smudger\'',
    author='Leon Jacobs',
    author_email='leonja511@gmail.com',
    url='https://github.com/leonjza/filesmudge',
    download_url = 'https://github.com/leonjza/filesmudge/tarball/0.1',
    keywords=['file', 'magic', 'bytes', 'edit', 'smudge'],
    version='0.1',
    py_modules=['smudge'],
    install_requires=[
        'Click', 'python-magic'
    ],
    entry_points='''
        [console_scripts]
        filesmudge=filesmudge.smudge:cli
    '''
)

import shelve

import click
import magic
import os


class SmudgeDB(object):
    """
        A Small shelve interface to get a DB
    """
    db_path = os.path.join(
        os.path.dirname(__file__), 'smudge')

    db = None

    def get(self):
        if not self.db:
            self.db = shelve.open(self.db_path)

        return self.db

    def __del__(self):
        if self.db:
            self.db.close()


smudge_db = SmudgeDB()


class SmudgeParamType(click.ParamType):
    """
        A click validator to ensure a known type is
        provided as an option
    """
    name = 'Smudge Type'

    def convert(self, value, param, ctx):
        db = smudge_db.get()

        if value not in db:
            self.fail('%s is not an implemented smudge' % value, param, ctx)

        return value


SMUDGE_TYPE = SmudgeParamType()


@click.group()
def cli():
    """
        Filesmudge.
        Smudge file magic bytes to look like other files.
    """
    pass


@cli.command()
@click.argument('source', type=click.File('r'))
def typedetect(source):
    """
        Determine a file type based on magic bytes
    """
    click.echo(magic.from_buffer(source.read(1024)))


def _backup_bytes(target, offset, length):
    """
        Read bytes from one file and write it to a
        backup file with the .bytes_backup suffix
    """
    click.echo('Backup {l} byes at position {offset} on file {file} to .bytes_backup'.format(
        l=length, offset=offset, file=target))

    with open(target, 'r+b') as f:
        f.seek(offset)

        with open(target + '.bytes_backup', 'w+b') as b:
            for _ in xrange(length):
                byte = f.read(1)
                b.write(byte)
            b.flush()

        f.flush()


def _smudge_bytes(target, offset, magic_bytes):
    """
        Write magic bytes to a file relative from
        offset
    """
    click.echo('Writing {c} magic byes at position {offset} on file {file}'.format(
        c=len(magic_bytes), offset=offset, file=target))

    with open(target, 'r+b') as f:
        f.seek(offset)
        f.write(magic_bytes)
        f.flush()

    click.echo('Changed written')


@cli.command()
@click.option('--newtype', type=SMUDGE_TYPE, prompt=True)
@click.option('--target', prompt=True, help='The file targetted for smudging')
def smudge(newtype, target):
    """
        Smudge magic bytes with a known type
    """

    db = smudge_db.get()

    magic_bytes = db[newtype]['magic']
    magic_offset = db[newtype]['offset']

    _backup_bytes(target, magic_offset, len(magic_bytes))
    _smudge_bytes(target, magic_offset, magic_bytes)


@cli.command()
@click.option('--target', prompt=True, help='The file targetted for smudging')
@click.option('--offset', default=0, help='The offset for the byte write')
@click.option('--magicbytes', help='The magic bytes to write relative to the offset')
def smudgeraw(target, offset, magicbytes):
    """
        Smudge magic bytes with raw bytes
    """
    magicbytes = magicbytes.replace('\\x', '').decode('hex')

    _backup_bytes(target, offset, len(magicbytes))
    _smudge_bytes(target, offset, magicbytes)


@cli.command()
@click.option('--source', help='The source file to attempt to restore from backup')
@click.option('--offset', default=0, help='The offset to restore bytes from')
def restore(source, offset):
    """
        Restore a smudged file from .bytes_backup
    """
    backup_location = os.path.join(
        os.path.dirname(os.path.abspath(source)), source + '.bytes_backup')
    click.echo('Reading backup from: {location}'.format(location=backup_location))

    if not os.path.isfile(backup_location):
        click.echo('No backup found for: {source}'.format(source=source))
        return

    with open(backup_location, 'r+b') as b:
        data = b.read()

    with open(source, 'r+b') as f:
        f.seek(offset)
        f.write(data)
        f.flush()


@cli.command()
def available():
    """
        List available types for 'smudge'
    """

    db = smudge_db.get()

    click.echo('{:<6} {:<6} {:<50}'.format('Type', 'Offset', 'Magic'))
    for k, v in db.items():
        click.echo('{type:<6} {offset:<6} {magic}'.format(
            type=k, magic=v['magic'].encode('hex'), offset=v['offset']))


if __name__ == '__main__':
    cli()

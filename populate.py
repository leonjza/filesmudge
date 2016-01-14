import shelve

import os

# Many more at:
#   http://www.garykessler.net/library/file_sigs.html
#   http://www.garykessler.net/library/magic.html
smudges = {
    'jpg': {
        'offset': 0,
        'magic': '\xFF\xD8\xFF'
    },
    'png': {
        'offset': 0,
        'magic': '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    },
    'gif': {
        'offset': 0,
        'magic': '\x47\x49\x46\x38\x39\x61'
    },
    'pdf': {
        'offset': 0,
        'magic': '\x25\x50\x44\x46'
    },
    'exe': {
        'offset': 0,
        'magic': '\x4D\x5A'
    },
    'tar': {
        'offset': 257,
        'magic': '\x75\x73\x74\x61\x72\x20\x20\x00'
    },
    '3gp': {
        'offset': 4,
        'magic': '\x66\x74\x79\x70\x33\x67'
    }
}


def populate_smudge_db():
    db_path = os.path.join(
        os.path.dirname(__file__), 'smudge')

    db = shelve.open(db_path)
    db.clear()
    db.update(smudges)
    db.close()

    print('Smudge DB Populated')


if __name__ == '__main__':
    populate_smudge_db()

# filesmudge
![thing](http://i.imgur.com/5yMsISd.png)  
Smudge (actually break) a file so that it is detected as another type of file.

## examples
### _smudging_ a file
This example takes a Mach-O executable, and writes the 8 magic bytes to make it look like a `png`. The 8 bytes that orinally were in the file is backed up to a `test.bytes_backup` file.
![thing](http://i.imgur.com/xqFFeBF.png)

### _restoring_ a file
It is possible to restore the file using _filesmudge_ too (assuming the `.bytes_backup` file is available)
![thing](http://i.imgur.com/VKa9N56.png)

## install
`pip install filesmudge`  
After installation, you should have the `filesmudge` commandline tool available to use.

## usage & help
`filesmudge` accepts the `--help` parameter to get help.

```text
~ » filesmudge --help
Usage: filesmudge [OPTIONS] COMMAND [ARGS]...

  Filesmudge. Smudge file magic bytes to look like other files.

Options:
  --help  Show this message and exit.

Commands:
  available   List available types for 'smudge'
  restore     Restore a smudged file from .bytes_backup
  smudge      Smudge magic bytes with a known type
  smudgeraw   Smudge magic bytes with raw bytes
  typedetect  Determine a file type based on magic bytes
```

All of the commands have their own help too and will explain the required parameters


# assignment2 

## Task 2.1

### Prerequisites

Should work on any Unix system.

### Functionality

Move all files in one directory to another.

### Limitations

The optional exercises for IN3110 are not implemented.

### Usage

```
usage: move <src> <dst>
```

Either make it executable with `chmod +x move.sh`, or run it with `bash`. Example:

```bash
./move.sh my-src-directory my-dst-directory
```

## Task 2.2 & 2.3

### Prerequisites

Works only with the GNU version of the `date` command, which is standard on most Linux systems (like `login.ifi.uio.no`), but not on macOS or other BSD derivatives.

### Functionality

All functionality described in the assignment text should work fine.

### Usage

```
usage: track start [label]
       track stop
       track status
       track log
```

Either make it executable with `chmod +x track.sh`, or run it with `bash`. Example:

```bash
$ bash track.sh start "My creative label name"
START Fri Sep 10 17:40:32 CEST 2021
LABEL My creative label name
$ bash track.sh status
Currently tracking:
START Fri Sep 10 17:40:32 CEST 2021
LABEL My creative label name
$ bash track.sh stop
END Fri Sep 10 17:40:52 CEST 2021
$ bash track.sh log
My creative label name: 00:00:20
```

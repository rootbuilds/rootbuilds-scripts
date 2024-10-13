'''
Parses database header for a sqlite3 file. See documentation here:https://sqlite.org/fileformat2.html
Usage:
> python3 parse_db_header.py --file {db file path}

offset|size|description
0   16  header string, "SQLite format 3\000"
16	2	The database page size in bytes. Must be a power of two between 512 and 32768 inclusive, or the value 1 representing a page size of 65536.
18	1	File format write version. 1 for legacy; 2 for WAL.
19	1	File format read version. 1 for legacy; 2 for WAL.
20	1	Bytes of unused "reserved" space at the end of each page. Usually 0.
21	1	Maximum embedded payload fraction. Must be 64.
22	1	Minimum embedded payload fraction. Must be 32.
23	1	Leaf payload fraction. Must be 32.
24	4	File change counter.
28	4	Size of the database file in pages. The "in-header database size".
32	4	Page number of the first freelist trunk page.
36	4	Total number of freelist pages.
40	4	The schema cookie.
44	4	The schema format number. Supported schema formats are 1, 2, 3, and 4.
48	4	Default page cache size.
52	4	The page number of the largest root b-tree page when in auto-vacuum or incremental-vacuum modes, or zero otherwise.
56	4	The database text encoding. A value of 1 means UTF-8. A value of 2 means UTF-16le. A value of 3 means UTF-16be.
60	4	The "user version" as read and set by the user_version pragma.
64	4	True (non-zero) for incremental-vacuum mode. False (zero) otherwise.
68	4	The "Application ID" set by PRAGMA application_id.
72	20	Reserved for expansion. Must be zero.
92	4	The version-valid-for number.
96	4	SQLITE_VERSION_NUMBER
'''
import argparse
import struct

def parse(file_name: str):
    with open(file_name, 'rb') as f:
        f.read(16) # header string
        print(f"> Page size in bytes: {struct.unpack('>H', f.read(2))[0]}")
        print(f"> File format write version: {int.from_bytes(f.read(1), byteorder='big')}")
        print(f"> File format read version: {int.from_bytes(f.read(1), byteorder='big')}")
        print(f"> Bytes of unused 'reserved' space at the end of each page: {int.from_bytes(f.read(1), byteorder='big')}")
        
        # Max embedded payload fraction. Must be 64
        bs = int.from_bytes(f.read(1), byteorder='big')
        print(f"> Max embedded payload fraction. Must be 64: {bs}")
        assert bs == 64, "Max embedded payload fraction. Must be 64"
        # Min embedded payload fraction. Must be 32
        bs = int.from_bytes(f.read(1), byteorder='big')
        print(f"> Min embedded payload fraction. Must be 32: {bs}")
        assert bs == 32, "Min embedded payload fraction. Must be 32"
        # Leaf payload fraction. Must be 32
        bs = int.from_bytes(f.read(1), byteorder='big')
        print(f"> Leaf payload fraction. Must be 32: {bs}")
        assert bs == 32, "Leaf payload fraction. Must be 32"

        print(f"> File change counter: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> Size of database file in pages: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> Page number of first freelist trunk page: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> Total number of freelist pages: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The schema cookie: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The schema format number: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> Default page cache size: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The page number of the largest root b-tree page when in auto-vacuum or incremental-vacuum modes, or zero otherwise: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The database text encoding. A value of 1 means UTF-8: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The \"user version\" as read and set by the user_version pragma.: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> True (non-zero) for incremental-vacuum mode. False (zero) otherwise.: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> The \"Application ID\" set by PRAGMA application_id.: {struct.unpack('>I', f.read(4))[0]}")
        # Next 20 bytes are reserved for expansion. Must be zero.
        bs = f.read(20)
        assert bs == b'\x00' * 20, "Reserved for expansion. Must be zero."

        print(f"> The version-valid-for number: {struct.unpack('>I', f.read(4))[0]}")
        print(f"> SQLITE_VERSION_NUMBER: {struct.unpack('>I', f.read(4))[0]}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="sqlite3 db file path")
    parser.add_argument('--file', type=str, help='sqlite3 db file path', required=True)
    args = parser.parse_args()
    parse(args.file)
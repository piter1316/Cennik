#!C:\Users\piter\PycharmProjects\Cennik\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ZODB==5.4.0','console_scripts','repozo'
__requires__ = 'ZODB==5.4.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ZODB==5.4.0', 'console_scripts', 'repozo')()
    )

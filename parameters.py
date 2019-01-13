import sys

if sys.platform == 'win32':
    chromedriver_location = 'chromedriver.exe'

if sys.platform == 'linux':
    chromedriver_location = './chromedriver'

vineyard_destination = 'vineyard.csv'

download_folder = './downloads'

download_backup = './download_backup'

biodynamic_archive = 'https://web.archive.org/web/*/http://www.biodynamicfood.org/beyond-organic/a'
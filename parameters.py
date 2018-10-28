import sys

if sys.platform == 'win32':
    chromedriver_location = 'chromedriver.exe'

if sys.platform == 'linux':
    chromedriver_location = './chromedriver'

vineyard_destination = 'vineyard.csv'
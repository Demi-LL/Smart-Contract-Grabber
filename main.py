import re
import cloudscraper
from random import choice
from bs4 import BeautifulSoup

domain = input('Please input the contract domain you want to fetch (default is etherscan): ')

if len(domain.strip()) == 0:
  domain = 'https://etherscan.io/address/'
  
contract_address = input('Contract Address: ')

save_dir = input('Input the condirectory you want to save result: ')

if len(save_dir.strip()) == 0:
  save_dir = './'

user_agent = ['chrome', 'firefox']
platform = ['linux', 'windows', 'darwin']
scraper = cloudscraper.create_scraper(browser={'browser': choice(user_agent), 'platform': choice(platform)})
res = scraper.get('{}{}'.format(domain, contract_address))
html_content = res.text

soup = BeautifulSoup(html_content, 'lxml')

codes_block = soup.find(id='dividcode')

filenames = [block.text for block in codes_block.select('div.justify-content-between > span.text-secondary')]
codes = [block.text for block in codes_block.select('div > pre.editor')]

for filename, code in zip(filenames, codes):
  regex_result = re.compile('.+: (.+)').search(filename)
  if not regex_result:
    print('[{}] occured error.'.format(filename.strip()))
  else:
    pure_filename = regex_result.group(1)
    with open('{}/{}'.format(save_dir.rstrip('/'), pure_filename), 'w+') as file:
      file.write(code)
      file.close()

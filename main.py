import os
import re
import requests
from random import choice
from bs4 import BeautifulSoup
from dotenv import load_dotenv
# 載入環境變數
load_dotenv()

domain = input('Please input the contract domain you want to fetch (default is etherscan): ')
  
contract_address = input('Contract Address: ')

save_dir = input('Input the condirectory you want to save result: ')

if len(domain.strip()) == 0:
  domain = 'https://etherscan.io/address/'

if len(save_dir.strip()) == 0:
  save_dir = './'
elif not os.path.isdir(save_dir):
  os.makedirs(save_dir)

res = requests.post('{}{}'.format(domain, contract_address),
  headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'},
  cookies={'cf_clearance': os.getenv('CLOUD_FLARE_KEY')},
  data={
    'md': '',
    'r': '',
    'cf_ch_verify': '',
  }
)
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

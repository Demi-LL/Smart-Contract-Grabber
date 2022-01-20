import re
import cloudscraper
from random import choice
from bs4 import BeautifulSoup

user_agent = ['chrome', 'firefox']
platform = ['linux', 'windows', 'darwin']
scraper = cloudscraper.create_scraper(browser={'browser': choice(user_agent), 'platform': choice(platform)})
res = scraper.get('https://etherscan.io/address/0x71c4658acc7b53ee814a29ce31100ff85ca23ca7#code')
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
    with open(pure_filename, 'w+') as file:
      file.write(code)
      file.close()

import sys
import ssl
import urllib.request
from bs4 import BeautifulSoup

# print('If you get error "ImportError: No module named \'six\'"' + 'install six:\n$ sudo pip install six')

login = 'brd-customer-hl_ae0246a5-zone-zone1'
password = 'pwykflkoeej2'
host = 'zproxy.lum-superproxy.io:22225'

ctx = ssl.create_default_context()
ctx.verify_flags = ssl.VERIFY_DEFAULT
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {
            # 'https': 'http://127.0.0.1:22225'
            'https': f'https://{login}:{password}@{host}'
        }
    ),
    urllib.request.HTTPSHandler(context=ctx)
)
text = opener.open("http://www.2ip.ru").read().decode()
soup = BeautifulSoup(text, 'html.parser')
ip = soup.find('div', class_='ip').text.strip()
location = soup.find('div', class_='value-country').text.strip()

print(f'IP: {ip} \n Location: {location}')


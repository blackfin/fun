#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from stem.control import Controller
from stem import Signal



lst = ['Firefox','Internet+Explorer','Opera','Safari','Chrome','Edge','Android+Webkit+Browser']


def save(br,ua):
	file = br+'.txt'
	with open(file,'ab') as f:
		f.write(ua+'\n')


def getUa(br):
	url = 'http://www.useragentstring.com/pages/useragentstring.php?name='+br
	r = requests.get(url)
	if r.status_code == 200:
		soup = BeautifulSoup(r.content,'html.parser')
	else:
		soup = False

	if soup:
		div = soup.find('div',{'id':'liste'})
		lnk = div.findAll('a')

		for i in lnk:
			try:
				save(br,i.text)
			except:
				print 'no ua'
	else:
		print 'No soup for '+br

def main():
  count = 0
  start_time = time.time()
  file = open("ua.txt", "r")
  for ua in file:
    with Controller.from_port(port = 9051) as controller:
      controller.authenticate()  # provide the password here if you set one
      controller.signal(Signal.NEWNYM)

      bytes_read = controller.get_info("traffic/read")
      bytes_written = controller.get_info("traffic/written")

      print("My Tor relay has read %s bytes and written %s." % (bytes_read, bytes_written))

      s = requests.session()

      s.proxies = {}
      s.proxies['http'] = 'socks5h://localhost:9050'
      s.proxies['https'] = 'socks5h://localhost:9050'

      checkIp = s.get('http://httpbin.org/ip')

      print(checkIp.text)

      example = """
      <html>
      <body>
      <div class="action-form-box-buttons action-action-footer">
        <span class="action-form-box-button action-form-box-button-first">
          <input name="action" value="Action Name" type="submit"></span>
	      <span class="action-form-box-button action-form-box-button-last">
		      <a name="show_result" href="/?ACTION_ID=2&amp;view_result=Y">Результат</a>
	      </span>
      </div>
      </body>
      </html>
      """

      mainPageTored = s.get('http://www.xyz.ru/')

      cookies = s.cookies.get_dict() # get cookie from response
      #print(cookies)
      #print(mainPageTored.text)
      found = re.search('\'xyz_sessid\':\'(\w+)\'', mainPageTored.text)
      extSessid = found.group(0)

      if (len(found.group(1)) == len('e186d9d04542717392ce439d44d69c52')):
        print("Md5 xyz_sessid is valid %s extracted from %s." % (found.group(1), found.group(0)))


      headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.mzra.ru/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

      headers['User-Agent'] = ua.rstrip("\n\r")

      data = {
        'result': 'Y',
        'PUBLIC_ACTION_ID': '2',
        'action_radio_2': '8',
        'action': '%D0%93%D0%BE%D0%BB%D0%BE%D1%81%D0%BE%D0%B2%D0%B0%D1%82%D1%8C'
        }
      data['sessid'] = found.group(1)

      print(data)
      tored = BeautifulSoup(mainPageTored.content, 'html.parser')
      span = tored.find("span", class_="action-form-box-button action-form-box-button-first")
      spans = tored.find_all('span', {'class' : 'action-form-box-button action-form-box-button-first'})
      #all_scripts = soup.find_all("script")
      if (spans):
        count += 1
        print("The action is actived %s. Total successed %s for time %s" % (spans, count, time.time() - start_time))
        repsonseFrom = s.post(
          'http://www.xyz.ru/', 
          headers=headers, 
          cookies=cookies, 
          data=data
        )
        print(repsonseFrom.status_code)
      print("Total action requests %s" % (count))
      time.sleep(10)

if __name__ == '__main__':
    main()
			

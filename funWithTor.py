import getpass
import requests
from stem.control import Controller
from stem import Signal


with Controller.from_port(port = 9051) as controller:
  s = requests.session()
  controller.authenticate()  # provide the password here if you set one
  controller.signal(Signal.NEWNYM)

  bytes_read = controller.get_info("traffic/read")
  bytes_written = controller.get_info("traffic/written")
  info = controller.get_info("circuit-status")

  checkIp = s.get('http://httpbin.org/ip')
  print(checkIp.text)

  print("My Tor relay has read %s bytes and written %s. info %s" % (bytes_read, bytes_written, info))


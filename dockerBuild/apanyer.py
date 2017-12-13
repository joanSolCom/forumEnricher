import sys

ip = sys.argv[1].strip()

fd = open("/var/www/html/forumEnricher/index.js","r")
js = fd.read()
clean = js.replace("localhost",ip)
fd.close()

fdOut = open("/var/www/html/forumEnricher/index.js","w")
fdOut.write(clean)
fdOut.close()
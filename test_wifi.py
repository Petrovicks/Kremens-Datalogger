import urllib2

def internet_on():
    try:
        urllib2.urlopen('http://172.217.18.238',timeout=1)
        print "Good wifi."
	return True
    except:
	print "Bad wifi."
        return False

                    

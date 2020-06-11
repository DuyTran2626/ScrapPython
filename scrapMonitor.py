import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
#---------------------------------------------------------------------------------------------------------------------------------------------#

mydb = mysql.connector.connect(
	host = "localhost",
	database = "testdb",
	user = "root",
	passwd = "admin",
)
my_cursor = mydb.cursor()
#---------------------------------------------------------------------------------------------------------------------------------------------#


#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#opts = Options()
#opts.set_headless()
#assert opts.headless  # Operating in headless mode
#browser = Firefox(options=opts)
#browser = webdriver.Firefox()




prodNameCurrent = ""
prodLinkCurrent = ""

prodNameindb = ""
prodLinkindb = ""
updatedtime = 0
totalProducts = 0

#---------------------------------------------------------------------------------------------------------------------------------------------#
def getMonitorInfo(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')

 	# Get the list of products in page 1
	products = soup.find('div',class_='row content-product-list')
	# Get Products into a arrays
	plist = products.find_all('div',class_='col-sm-4 col-xs-12 padding-none col-fix20')
	global totalProducts
	totalProducts = len(plist) + totalProducts
	for product in plist:
		productName = product.find(class_='product-row-name')
		productCost = product.find(class_='product-row-sale')
	#	productDis = product.find(class_='new-product-percent')
		Link = product.find('a')['href']
		productLink = "https://gearvn.com"+ Link
		name = productName.text.strip().encode('ascii', 'ignore').decode('ascii').replace('Mn hnh ','').replace('siu mng','sieu mong').replace('vin mng','vien mong').replace('chuyn','chuyen').replace('Mn Hnh','').replace('"','inch').replace('cong','Man hinh cong')

		cost = productCost.text.strip().encode('ascii', 'ignore').decode('ascii')
		link = productLink 
	#	print(productName.text.strip())
		my_cursor.execute("INSERT INTO products (productName,productCost,productLink) VALUES ('"+name+"','"+cost+"','"+link+"')")
		mydb.commit()
	#	print(productCost.text.strip())
	#	if None in (productName,productCost, productDis):
	#		print("Discount: None")
	#		#my_cursor.execute("INSERT INTO products (productCost) VALUES ('None')")
	#	else: print("Discount: "+ productDis.text.strip().encode('ascii', 'ignore').decode('ascii'))
	#	print("Link of Product: "+ productLink)
	#	print("")
#---------------------------------------------------------------------------------------------------------------------------------------------#
def getAllMonitorInfo():
	getMonitorInfo('https://gearvn.com/collections/man-hinh')
	for i in range(2,8):
		url = "https://gearvn.com/collections/man-hinh?page=" + str(i)
		getMonitorInfo(url)

getAllMonitorInfo()
print(str(totalProducts) + " devices is recorded. Continue recording")
time.sleep(20)
while(1):
	getAllMonitorInfo()
	my_cursor.execute("select record_time from products ORDER BY ID DESC LIMIT 1")
	print(my_cursor.fetchone())
	print("Total recorded: "+str(totalProducts))
	time.sleep(20)




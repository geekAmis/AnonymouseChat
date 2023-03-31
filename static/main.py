from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

class Driver(object):
	"""docstring for Driver"""
	def __init__(self, url, executable_path="C:/geckodriver.exe",binary_location=r"C:\Program Files\Mozilla Firefox\firefox.exe"):
		self.url=url
		self.executable_path = executable_path
		self.options = Options()
		#self.options.add_argument("--headless")
		self.binary_location = binary_location
		self.options.binary_location = self.binary_location
		self.driver = webdriver.Firefox(options=self.options, executable_path=self.executable_path)
		self.driver.get(self.url)

	def login(self):
		self.driver.find_element("xpath",'/html/body/div[4]/a/span').click()
		self.driver.find_element('xpath','//*[@id="login_input1"]').click()
		self.driver.find_element('xpath','//*[@id="login_input1"]').send_keys("xgemx1")
		self.driver.find_element('xpath','//*[@id="login_input2"]').click()
		self.driver.find_element('xpath','//*[@id="login_input2"]').send_keys('Test1313!')
		self.driver.find_element('xpath','//*[@id="login_submit"]').click()

	def anime(self):
		self.driver.find_element('xpath','/html/body/div[5]/div[2]/div[1]/ul/li[1]/a').click()

	def scrol_init(self,inits=5):
		y = 500
		for timer in range(0,inits):
			self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
			y += 500 
			sleep(1)

	def anima_first(self):
		self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[2]/a[1]').click()

	def play(self):
		try:
			self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[4]/div/div[1]/div[2]/div[4]/button/span[1]').click()
			return True
		except:
			return False

	def anima(self,url):
		self.driver.get(url)

	def foreva(self):
		if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[4]/div[1]/div[1]/div[2]/div[4]/button'):
			return True
		return False

	def skip(self):
		try:
			self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[4]/div[1]/div[1]/div[2]/div[4]/div[4]').click()
			return True
		except:
			return False
	def next_seria(self):
		try:
			self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[4]/div[1]/div[1]/div[2]/div[4]/div[6]').click()
			return True
		except:
			return False

	def fully(self):
		try:
			self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div[4]/div[1]/div[1]/div[2]/div[4]/div[9]/button[5]/span[1]').click()
		except:
			pass


	def Quit(self):
		sleep(5)
		self.driver.close()
		self.driver.quit()

a = Driver('https://jut.su')
a.login()
a.anime()
a.scrol_init()
a.anima('https://jut.su/full-dive-rpg/episode-1.html')
a.anima_first()
while True:
	try:
		if a.foreva():
			if a.play():
				sleep(2)
				a.fully()


		a.skip()
		a.next_seria()
		

	except:
		print('Except While')
#a.Quit()
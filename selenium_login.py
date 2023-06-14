from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def start_driver():
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--use-gl=desktop')
	chrome_options.add_argument('user-data-dir=/selenium/')
	chrome_options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(options=chrome_options)
	driver.get('https://app.musicleague.com')
	driver.implicitly_wait(10)
	return driver


def main():
	start_driver()


if __name__ == '__main__':
	main()

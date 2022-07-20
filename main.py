from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('user-data-dir=C:/Users/Max/PycharmProjects/extractMusicLeague/selenium/')
chrome_options.add_argument('--use-gl=desktop')
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://www.google.com')

nameList = open("usernames.txt","r",encoding='utf8')
realNames = []
usernames = []
for line in nameList:
	realName = line.split("=")[1].rstrip()
	username = line.split("=")[0]
	realNames.append(realName)
	usernames.append(username)

def parseInfo(info):
	titleraw = info[0]
	artistraw = info[1]
	submitterraw = info[2]
	formattedInfo = []
	formatArtist = artistraw.split("By ")[1]
	formatSubmitter = submitterraw.split("Submitted by ")[1]
	formattedInfo.append(titleraw)
	formattedInfo.append(formatArtist)
	formattedInfo.append(formatSubmitter)
	return formattedInfo


def parseVoterInfo(data):
	scores = data[::2]
	scoresInt = []
	for i in range(0, len(scores)):
		scoresInt.append(int(scores[i]))
	voters = data[1::2]
	votersSetName = []
	for i in range(0, len(voters)):
		if voters[i] in usernames:
			name = parseUsername(voters[i])
			votersSetName.append(name)
	info = [scoresInt, votersSetName]
	return info

def parseUsername(username):
	print(username)
	if username in usernames:
		findIndex = usernames.index(username)
		name = realNames[findIndex]
#		print(name)
		return name
	else:
#		print(username)
		return username


# url = input("url: ")
def main():
	file = open("test.txt", "a",encoding='utf8')
	names = ";".join(realNames)
	file.write("Artist;Spotify;Title;Submitter;{};Total;Voters\n".format(names))
	file.close()
#	url = "https://musicleague.app/l/3812aa9087374a70bb951915a3747656/dfbe477c43324f9387de88193f11a0d2/"
	url = input("url: ")
	if url == "quit":
		exit()
	print("Please wait...", flush=True)
	driver.get("{}".format(url))
	for song in range(0,32):
		testInfo = driver.find_elements_by_class_name("text-info")[song*2].text.splitlines()
		info = parseInfo(testInfo)
		testVoterCount = driver.find_elements_by_class_name("voter-count")[song].text
		if "Person" in testVoterCount:
			realVoterCount = 1
		else:
			realVoterCount = int(testVoterCount.split(" People Voted On This")[0])
		testScore = driver.find_elements_by_class_name("point-count")[song].text
		testVoterScore = driver.find_elements_by_class_name("hidden-xs.col-sm-7")[song].text.splitlines()
		voterInfo = parseVoterInfo(testVoterScore)

		title = info[0]
		artist = info[1]
		submitter = parseUsername(info[2])

		spotifyURLgrab = driver.find_element_by_link_text(title)
		spotifyURL = spotifyURLgrab.get_attribute("href")

		print(title + " - " + artist + " (Submitter: " + submitter + ")")
		print(spotifyURL)
		print(str(realVoterCount) + " voters, " + testScore + " votes.")
		for i in range(0, int(realVoterCount)):
			score = voterInfo[0]
			voter = voterInfo[1]
			print(str(score[i]) + " " + str(voter[i]))

		ezVote = []
		for name in realNames:
			if name in voter:
				findIndex = voter.index(name)
				ezVote.append(score[findIndex])
			elif name == submitter:
				ezVote.append("S")
			else:
				ezVote.append(0)
		songInfo = ("{artist};{url};{title};{submitter};{votes};{total};{votercount}\n".format(title=title,artist=artist,submitter=submitter,url=spotifyURL,votes=";".join(map(str, ezVote)),total=testScore,votercount=realVoterCount))
		file = open("test.txt","a",encoding='utf8')
		file.write(songInfo)
		file.close()
	main()

main()

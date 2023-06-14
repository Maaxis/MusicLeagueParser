from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from file_options import user_ids, real_names, usernames, sep, file_out


def get_name_from_id(this_id):
	if this_id in user_ids:
		i = user_ids.index(this_id)
		return real_names[i]
	else:
		return this_id


def get_id_from_submitted_by(user_text):
	submitter = user_text.split("Submitted by ")[1]
	if submitter in usernames:
		i = usernames.index(submitter)
		return user_ids[i]
	else:
		print("ERROR: Submitter {} has no associated user ID - add in user_ids.txt".format(submitter))
		return submitter


def start_driver():  # do all Selenium setup here
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--use-gl=desktop')
	chrome_options.add_argument('user-data-dir=/selenium/')
	chrome_options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(options=chrome_options)
	driver.get('https://www.google.com')
	driver.implicitly_wait(10)
	return driver


def parse_song_info(driver, i):  # returns data for 1 song and its votes and formats it
	# given the round URL and the song index (where the song is ordered on the page)
	# We mostly find the data to fetch with xpath, which will break if the site updates.
	artist = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div[{}]/div[1]/div[2]/div/div[1]/span[1]/span".format(
		str(i + 2))).text  # returns artist name
	#print(artist)
	title = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div[{}]/div[1]/div[2]/div/div[1]/strong/a".format(
		str(i + 2))).text  # returns song title
	#print(title)
	score = driver.find_element(By.XPATH,
	                            "//*[@id=\"app\"]/div/div[2]/div/div[{}]/div[1]/div[2]/div/div[2]/span[1]".format(
		                            str(i + 2))).text  # returns song's score
	#print(score)
	vote_count = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/div[2]/div/div[{}]/div[1]/div[2]/div/div[2]/span[2]".format(
		str(i + 2))).text  # returns number of voters
	#print(vote_count)
	spotify = driver.find_element(By.LINK_TEXT, title).get_attribute("href")  # returns spotify URL
	#print(spotify)
	submitter_t = driver.find_element(By.XPATH,
	                                  "//*[@id=\"app\"]/div/div[2]/div/div[{}]/div[2]/div[2]/span".format(
		                                  str(i + 2))).text
	#print(submitter_t)
	# returns "Submitted by MLusername" - we later acquire ID from this, which will cause issues if two people
	# share the same username. TODO: Possibly find a way to fetch the ID directly instead?
	if submitter_t == "Submitted by [ Competitor has left the league ]":
		print("ERROR: A competitor has left the league. This will cause incorrect associations of votes and people."
		      "This will be fixed in a later update, but for now, you can band-aid this by hard-coding the"
		      "real name of submitter_t below this print statement in the source code,"
		      "if only one person has left the league.")
		# submitter_t = "Submitted by INSERTNAMEHERE"
		# Uncomment the above line to hardcode the name of a person that left the league
		# TODO: fix this, which might be possible if we fetch ID instead, or at least ask user for info
	submitter_id = get_id_from_submitted_by(submitter_t)  # returns submitter user ID
	submitter_name = get_name_from_id(submitter_id)  # returns name of submitter
	# We need both, as the ID is used to initially identify the submitter
	# and the name is used in the Submitter column of the exported file.
	# (this can probably be rewritten to not require one of these)
	# TODO: reduce redundancy of having both name and ID, if applicable after rewriting the above
	track_id = spotify.split("/track/")[1]  # returns song's track ID on Spotify
	print(("{artist} - {title}\n{score} points ({vote_count})\n{submitter_t} - {spotify}".format(artist=artist,
	                                                                                             title=title,
	                                                                                             score=score,
	                                                                                             vote_count=vote_count,
	                                                                                             submitter_t=submitter_t,
	                                                                                             spotify=spotify)).expandtabs(
		30))
	# main song info done, begin parsing individual votes
	vote_scores = []
	driver.implicitly_wait(0)
	for i in range(0, len(user_ids)):  # for every user
		if user_ids[i] == submitter_id:  # if the user is the song submitter
			vote_scores.append("S")  # mark with "S"
			print((real_names[i] + "\tSubmitter").expandtabs(20))
		else:
			try:  # check if the user upvoted this
				this_score = driver.find_element(By.XPATH,
				                                 "//*[@id=\"song-spotify:track:{}-voter-{}\"]/div[3]/span/span".format(
					                                 track_id, user_ids[i])).text
				vote_scores.append(this_score)  # mark with their vote
				print((real_names[i] + "\t" + this_score).expandtabs(20))
			except NoSuchElementException:  # happens if no vote or if the vote is a downvote
				try:  # check for downvote
					this_score = driver.find_element(By.XPATH,
					                                 "//*[@id=\"song-spotify:track:{}-voter-{}\"]/div[3]/span".format(
						                                 track_id, user_ids[i])).text
					vote_scores.append(this_score)  # mark with their downvote
					print((real_names[i] + "\t" + this_score).expandtabs(20))
				except NoSuchElementException:  # happens if the voter did not vote for this
					vote_scores.append('0')  # mark with 0
					print((real_names[i] + "\t" + '0').expandtabs(20))
	driver.implicitly_wait(3)
	song_line = (  # now format all the data into a nice row
		"{artist}{s}{url}{s}{title}{s}{submitter}{s}{votes}{s}{total}{s}{vote_count}".format(artist=artist, url=spotify,
		                                                                                     title=title,
		                                                                                     submitter=submitter_name,
		                                                                                     s=sep,
		                                                                                     votes=sep.join(
			                                                                                     map(str, vote_scores)),
		                                                                                     total=score, vote_count=
		                                                                                     vote_count.split(
			                                                                                     " Voters")[
			                                                                                     0]))
	print("")
	return song_line


def add_bells(song_line, week, url):  # some extra automation for quicker transfer to Excel, this can be modified
	song_string = "=TRIM(CLEAN(HYPERLINK(CONCAT($D2),$E2)))"
	avg = "Z2/AA2"
	week_url = ("=HYPERLINK(\"" + url + "\",{})".format(week))
	song_line2 = week_url + sep + song_string + sep + song_line + sep + avg
	return song_line2


def create_header():  # the top row of the exported file, should only be run once per file
	file = open(file_out, "a", encoding='utf8')
	names = sep.join(real_names)
	file.write(
		"Round{sep}Song{sep}Artist{sep}Spotify{sep}Title{sep}Submitter{sep}{names}{sep}Total{sep}Voters{sep}Average\n".format(
			sep=sep, names=names))
	file.close()


def main():
	print("Type quit to exit.")
	url = input("url: ")
	week = input("round: ")
	if url == "quit" or week == "quit":
		exit()
	print("Please wait...", flush=True)
	driver = start_driver()
	driver.get("{}".format(url))
	driver.implicitly_wait(1)
	sleep(5)  # give extra time for page to load
	for i in range(0, len(real_names * 1)):  # for each song (replace "2" with the maximum number of songs a person
		# can submit per round)
		# TODO: just make this a while loop, it's currently a for loop that's meant to break
		try:  # get and write song info and votes as one row
			#print(i)
			sl = parse_song_info(driver, i)
			song_line = add_bells(sl, week, url)
			#print(song_line)
			file = open(file_out, "a", encoding='utf8')
			file.write(song_line + "\n")
			file.close()
		except NoSuchElementException:  # stop if we reach the end of the round
			break
	driver.close()  # this takes forever for some reason?
	main()


if __name__ == '__main__':
	main()

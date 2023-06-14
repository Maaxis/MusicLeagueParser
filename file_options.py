from time import sleep

file_ids = "user_ids.txt"
file_out = "out.txt"
sep = "|"  # This is how values will be separated in the exported file. Commas aren't preferred, because song titles
# often include commas.

# with indexing, real names, ML usernames, and ML user IDs are associated with each other
# Real name = the name that will appear in the header of the exported file - your choice
# ML username = the person's display name on musicleague.com
# ML user ID = the unique string associated with each user's profile on musicleague.com,
# which follows /user/ in their profile's URL.
# Make a file user_ids.txt with each line representing one person in the league in the format realname=username=userid
# Example: Max=max=ef5170c99dbd4c2e9224b9fdb1780a35
# Creating this automatically will be added in a future update.
# TODO: automate this part
id_list = ''
try:
	id_list = open(file_ids, "r", encoding='utf8')
except FileNotFoundError:
	print("ERROR: user_ids.txt doesn't exist. Please create a file user_ids.txt in the same directory as main.py,"
	      "and add people to it in the format RealName=MLusername=MLuserID for each line."
	      "(e.g. Max=max=ef5170c99dbd4c2e9224b9fdb1780a35)"
	      "This will be automated in a future update.")
	sleep(5)
	quit()
real_names = []
usernames = []
user_ids = []
for line in id_list:
	name = line.split("=")[0]
	username = line.split("=")[1]
	id = line.split("=")[2].rstrip()
	real_names.append(name)
	usernames.append(username)
	user_ids.append(id)
print(id_list)
id_list.close()

# MusicLeagueParser

Export votes from a Music League round into a delimited text file via Selenium.

Tested to work with Python 3.9, Chrome 110, Selenium 4.0.0

# First time setup

Download the project folder from github.

## Setting up Selenium

1. Install the latest Google Chrome from https://www.google.com/chrome/
2. Install Selenium with `pip install selenium`
3. Download `chromedriver_{your OS}.zip` from https://chromedriver.chromium.org/downloads for your version of Chrome
4. Extract `chromedriver.exe` to the same folder as `main.py`
5. Run `selenium_login.py`, if everything is correct, a Chrome window should open directing to the Music League log-in page
6. Log in to Music League (User data is stored in `/selenium/` - your log-in will be saved as a cookie)
7. Close Chrome

# Usage

## Creating user_ids.txt (once per season)

1. If `user_ids.txt` doesn't exist in the project folder, create it. If it does, delete all entries inside it
2. Add a player in the format `{Name}={Music League display name}={Music League user ID}` where:
`{Name}` is the player's preferred name and how their name will be displayed in the outputted data,
`{Music League display name}` is the player's display name in the Music League website, and
`{Music League user ID}` is the player's profile ID in the Music League website, found by going to their profile and copying the string following `https://app.musicleague.com/user/...`
3. Repeat step 2 for all players, DO NOT add players that are not in the season

   Note that this will determine the order each player appears in the columns of the outputted data, so alphabetize this list if desired

## Creating headers (once per season)

1. If `out.txt` exists in the project folder, rename or delete it
2. Run `create_header.py`

## Scraping data

1. Run `main.py`
2. When asked for URL, provide the URL of the Music League round to be parsed
3. When asked for round, provide the round number for this season (e.g. 5 for round 5 of 12)
4. Wait
5. Repeat steps 2 and 3 for each round of the season

## Importing to Excel

1. Paste the contents of `out.txt` to an empty Excel workbook.
2. If columns are not automatically delimited, do so by selecting all contents and navigating to `Data` -> `Text to Columns`, selecting `Delimited` and using the custom delimiter (default `|`)
3. Verify the selected cells, both column (absolute) and row (relative), in the second column are correct: `TRIM(CLEAN(HYPERLINK(CONCAT({Spotify URL}),{Song Title})))`
4. Add an `=` to the start of the first instance to turn it into a formula, then use the fill handle to copy the formula down the rest of the column
5. Hide the columns for Spotify URL and Song Title
6. If desired, repeat steps 3 and 4 for the last column, which should use the relative formula `{third-to-last column}/{second-to-last column}`, for a count of average votes per person
7. If desired, format the contents of the file as a table to be able to sort the data by selecting all contents and navigating to `Insert` -> `Table`

Very rarely, a bug can occur for an unknown reason where a player's votes are consistently wrong for the checked round. You may want to keep an eye out for this by keeping running calculations of each player's vote counts per round or by checking if the sum of calculated votes for a song match its actual total score and manually fixing any inconsistencies.

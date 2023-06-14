from file_options import real_names, sep, file_out


def create_header():  # the top row of the exported file, should only be run once per file
	file = open(file_out, "a", encoding='utf8')
	names = sep.join(real_names)
	file.write(
		"Round{sep}Song{sep}Artist{sep}Spotify{sep}Title{sep}Submitter{sep}{names}{sep}Total{sep}Voters{sep}Average\n".format(
			sep=sep, names=names))
	file.close()


def main():
	create_header()


if __name__ == '__main__':
	main()

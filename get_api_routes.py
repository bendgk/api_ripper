#	██╗   ██╗██████╗ ██╗         ██████╗ ██╗██████╗ ██████╗ ███████╗██████╗ 
#	██║   ██║██╔══██╗██║         ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
#	██║   ██║██████╔╝██║         ██████╔╝██║██████╔╝██████╔╝█████╗  ██████╔╝
#	██║   ██║██╔══██╗██║         ██╔══██╗██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
#	╚██████╔╝██║  ██║███████╗    ██║  ██║██║██║     ██║     ███████╗██║  ██║
#	 ╚═════╝ ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
#
#	Author: bendgk
#	xmr: 89gUjiiNw9NMguU7BHnYCTbnhereQa9aLdK8aXdtWAuNFq58qftDJ1JhggVA2V5r4E2duJKaPC3idENzJc8qwfQs3zpeKm6
                                                                                                                                                    
import argparse
import re
import os
import threading

#	 █████╗ ██████╗  ██████╗ ███████╗
#	██╔══██╗██╔══██╗██╔════╝ ██╔════╝
#	███████║██████╔╝██║  ███╗███████╗
#	██╔══██║██╔══██╗██║   ██║╚════██║
#	██║  ██║██║  ██║╚██████╔╝███████║
#	╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

parser = argparse.ArgumentParser(description="Find all api routes in a given file (url matching)")
parser.add_argument('file_path', type=str, help="path / directory to analyze")
parser.add_argument('--encoding', type=str, help="encoding to preprocess the file with")
parser.add_argument('--keywords', type=str, help="path to load list of regex strings for analysis")

args = parser.parse_args()

def analyze(string, keywords=None):
	string = string.strip().lower()
	weight = 0

	# url should probably be less than 200 chars
	if len(string) > 200:
		return weight

	# if string does not contain / (forward slash) or \ (backslash) charachter
	# then it is most likely not a url scheme 
	if ("/" not in string and "\\" not in string) or ("." not in string):
		return weight

	else:
		if keywords:
			with open(keywords) as f:
				text = f.read()
				text = text.split("\n")

				keywords = []

				for line in text:
					 for i in range(len(line)):
					 	if line[-1 - i] == ',':
					 		text_pattern = str(line[0:i].strip())
					 		text_weigth = float(line[i:].strip())
					 		keywords.append((text_pattern, text_weigth))
					 		break


		else:
			#some default keywords to allow out of the box analysis
			keywords = [
				(r'dev', 10), 			(r'api', 10), 	(r'rest', 5),
				(r'[/]v[1,2,3]', 5),	(r'&', 1),	    (r'get', 5),
				(r'post', 5),			(r'prod', 10),	(r'[?]', 1),
			]

		url_pattern = r"((http|ftp|https|ws|wss):\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
		result = re.search(url_pattern, string)

		if result:
			string = result.group()
			weight = 5
			url_weight = 10000

		else:
			weight = .5
			url_weight = 0

		count = 0
		for key in keywords:
			key_pattern = key[0]
			key_weight = key[1]

			if re.search(key_pattern, string):
				count += key_weight

		weight = url_weight + weight * count

		return weight

		# if weight is 1 it is most likely a url
		# if weight is .5 it is a string of interest (contains a '.', '/', '\')
		# weights greater than 1 indicate how many keywords have been matched (the more the better)

def prettify(ripped_strings):
	lengths = []
	out = ""
	for item in ripped_strings:
		b = f"Weight: {item[0]}\nString: {item[1]}\nPath: {item[2]}"
		out += b + "\n\n"

	return out

def worker():
	pass

#	███╗   ███╗ █████╗ ██╗███╗   ██╗
#	████╗ ████║██╔══██╗██║████╗  ██║
#	██╔████╔██║███████║██║██╔██╗ ██║
#	██║╚██╔╝██║██╔══██║██║██║╚██╗██║
#	██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
#	╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

if __name__ == '__main__':
	file_path = args.file_path
	file_paths = []

	# recursively get all files in a directory and append them to file_paths
	if os.path.isdir(file_path):
		for root, subdirs, files in os.walk(file_path):
			for file in files:
				file_paths.append(root + "/" + file)

	# if file_path is not a directory we only want to analyze one file
	else:
		file_paths.append(file_path)

	ripped_strings = []

	#Main loop
	for file_path in file_paths:
		text = ""

		with open(file_path, 'r') as f:
			try:
				text = f.read()
			except:
				print(f"could not open {file_path} as plain text trying bytes...")

				with open(file_path, 'rb') as fb:
					try:
						binary = fb.read()
						text = binary.decode('hex')

					except:
						print(f"could not open {file_path}!\nskipping...")
						continue

		string_pattern = r"(?<=\"|\')[^\'\"]+(?=\"|\')"
		strings = re.findall(string_pattern, text)

		for string in strings:
			weight = analyze(string)

			if len(ripped_strings) == 0:
				ripped_strings.append((weight, string, file_path))

			for i in range(len(ripped_strings)):
				if weight >= ripped_strings[i][0]:
					ripped_strings.insert(i, (weight, string, file_path))
					break

	with open("out.txt", "w+") as f:
		f.write(prettify(ripped_strings))

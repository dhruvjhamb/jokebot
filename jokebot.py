import time
import csv
import sys
import requests
import json

def deliver_joke(prompt, punchline):
	""" Prints prompt, waits 2 seconds, then prints punchline. """
	print("\n" + prompt)
	time.sleep(2)
	print(punchline + "\n")

def read_input():
	""" Reads user input. """
	while True: 
		user_input = input("Enter next for another joke or quit to exit:\n")

		if user_input == "next":
			return True
		elif user_input == "quit":
			return False
		else:
			print("Error: I don't understand")

def read_csv(file):
	""" Reads CSV file given by the parameter and returns a list of jokes
	    (each joke contains a prompt and punchline). """
	try:
		with open(file, newline='') as csvfile:
			jokebot_reader = csv.reader(csvfile, delimiter=',')
			return list(jokebot_reader)
	except IOError as erri:
		print("Error Reading File:", erri)
		sys.exit(1)
	except FileNotFoundError as err:
		print("File Not Found:". err)
		sys.exit(1)

def read_reddit(url):
	""" Downloads json from url, filters the posts, then extracts the post titles and
	    bodies into a list of jokes. """
	try:
		r = requests.get(url, headers={'User-agent': 'jokebot'}, timeout=3)
		r.raise_for_status()
	except requests.exceptions.HTTPError as errh:
	    print ("Http Error:", errh)
	    sys.exit(1)
	except requests.exceptions.ConnectionError as errc:
	    print ("Error Connecting:", errc)
	    sys.exit(1)
	except requests.exceptions.Timeout as errt:
	    print ("Timeout Error:", errt)
	    sys.exit(1)
	except requests.exceptions.RequestException as err:
	    print ("OOps: Something Else", err)
	    sys.exit(1)

	json_data = r.json()
	posts_data = json_data['data']['children']
	joke_reader = []

	for post in posts_data:
		safe_for_work = not post['data']['over_18']
		question = post['data']['title'].startswith(('Why', 'What', 'How'))
		if safe_for_work and question:
			joke_reader.append([post['data']['title'], post['data']['selftext']])
	
	return joke_reader

def read_arguments():
	""" Reads and returns command line arguments. Returns False if no arguments are given. """
	if len(sys.argv) > 1:
		file = sys.argv[1]
		return file
	else:
		return False

if __name__ == "__main__":
	file = read_arguments()

	if file:
		jokebot_reader = read_csv(file)
	else:
		jokebot_reader = read_reddit('https://www.reddit.com/r/dadjokes.json')
	
	while read_input() and jokebot_reader:
		# while user continues to input next and the reader is not empty
		# use pop to remove the last element from the list
		joke_and_punchline = jokebot_reader.pop()
		# joke_and_punchline is a 2 element list with the joke and punchline
		deliver_joke(joke_and_punchline[0], joke_and_punchline[1])

	print("\nGoodbye.")
	sys.exit()

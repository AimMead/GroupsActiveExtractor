import requests
import time
import datetime
import os
os.system('color a')

print("[+] Coder : Mostafa M. Mead [+]")
print("[+] Simple Python Script To Fetch Active Members In Groups [+]")

operationName = input("[+] Enter Operation Name: ")
uniqueList = []
postsList = []
accessToken = input('[+] Enter Access Token: ')
groupsText = input('[+] Enter Groups Ids Text: ')
activeList = [
	"https://graph.facebook.com/{}/likes?fields=id&access_token={}&limit=100",
	"https://graph.facebook.com/{}/comments?fields=from&access_token={}&limit=100"
	]
fileName = "{} {}.txt".format(
	operationName,
	datetime.datetime.today().strftime('%Y-%m-%d'),
	)
postsNum = int(input("[+] Enter Posts Num: "))

def GetPosts():
	with open(groupsText) as f:
		lines = f.read().split("\n")
	print("Wait While Collecting Posts Ids..")
	for _id in lines:
		postsUrl = 'https://graph.facebook.com/{}/feed?fields=id&access_token={}&limit=300'.format(_id , accessToken)
		while True:
			postsReq = requests.get(postsUrl)
			postsJson = postsReq.json()
			postsSrc = str(postsReq.content)
			print(postsSrc)
			for postId in postsJson['data']:
				postsList.append(postId['id'])
			if "next" in postsSrc:
				postsUrl = postsJson['paging']['next']
			else:
				break
			if len(postsList) >= postsNum:
				break
	print("Collected {} Ids".format(len(postsList)))

def GetActive():
	for postId in postsList:
		for activeUrl in activeList:
			activeUrl = activeUrl.format(postId , accessToken)
			while True:
				activeReq = requests.get(activeUrl)
				activeJson = activeReq.json()
				activeSrc = str(activeReq.content)
				for activator in activeJson['data']:
					if 'comments' in activeUrl:
						activator = activator['from']['id']
					else:
						activator = activator['id']
					if activator not in uniqueList:
						uniqueList.append(activator)
						file = open(fileName , 'a+')
						file.write(activator + "\n")
						file.close()
				if "next" in activeSrc:
					activeUrl = activeJson['paging']['next']
				else:
					break
		print("Current Post Id: {}\nExtracted Ids: {}".format(postId , len(uniqueList)) , end="\r")

try:
	GetPosts()
	GetActive()
except Exception as e:
	print(e)
	pass
else:
	print("Done Fetching All Groups !")
time.sleep(1000)
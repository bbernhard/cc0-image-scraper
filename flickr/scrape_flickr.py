import flickrapi
import json
import os
import sys
import urllib.request
import uuid
import requests

FLICKR_API_KEY = ""
FLICKR_LICENSE = 9 #CC0
FLICKR_SAFE_SEARCH = 1 #1 for safe, 2 for moderate, 3 for restricted.
FLICKR_API_SECRET = ""

#specify the path where the images will be downloaded to. 
BASEPATH = "" #"/home/bernhard/flickr/"

SEARCH_QUERY = ""
START_PAGE = 1

DOWNLOADPATH = BASEPATH + os.path.sep + SEARCH_QUERY

def download(url):
	req = urllib.request.Request(
		url, 
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
		}
	)

	p = DOWNLOADPATH + os.path.sep + str(uuid.uuid4()) + ".jpg"
	urllib.request.urlretrieve(url, p)


def get_preferred_image_size_suffix(image_id):
	u = ("https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=" 
			+ FLICKR_API_KEY + "&photo_id=" + str(image_id) + "&format=json&nojsoncallback=1")
	req = requests.get(u)
	if req.status_code != 200:
		raise RuntimeError("Couldn't get image size")
	data = req.json()
	sizes = data["sizes"]["size"]
	suffix = ""
	for size in sizes:
		if size["label"] == "Large": #preferred size
			suffix = "_b"
			break
		if suffix != "_b" and size["label"] == "Medium 800":
			suffix = "_c"
		if suffix != "_b" and suffix != "_c" and size["label"] == "Medium 640":
			suffix = "_z"
	return suffix


def download_all_images_at_page(flickr_client, page):
	data = flickr_client.photos_search(safe_search=FLICKR_SAFE_SEARCH, license=FLICKR_LICENSE, page=page, text=SEARCH_QUERY)
	photos = data["photos"]
	num_of_pages = photos["pages"]
	photos = photos["photo"]
	ctr = 0
	for photo in photos:
		if photo["ispublic"] != 1:
			continue

		image_size_suffix = ""
		try:
			image_size_suffix = get_preferred_image_size_suffix(photo["id"])
		except RuntimeError as e:
			print(str(e))
			continue
		except Exception as e1:
			print(str(e1))
			continue

		ctr += 1
		u = ("http://farm" + str(photo["farm"]) + ".static.flickr.com/" + 
				str(photo["server"]) + "/" + str(photo["id"]) + "_" + str(photo["secret"]) + image_size_suffix + ".jpg")
		print("downloading #%d (page: %d/%d), %s" %(ctr, page, num_of_pages, u,))
		download(u)

	return (page, num_of_pages)


if __name__ == "__main__":
	if BASEPATH == "":
		print("Please set the BASEPATH first!")
		sys.exit(1)

	if FLICKR_API_KEY == "":
		print("Please set the FLICKR_API_KEY first!")
		sys.exit(1)

	if FLICKR_API_SECRET == "":
		print("Please set the FLICKR_API_SECRET first!")
		sys.exit(1)
	
	if not os.path.exists(BASEPATH):
		print("%s is not a valid path!" %(BASEPATH,))
		sys.exit(1)

	if SEARCH_QUERY == "":
		print("SEARCH_QUERY needs to be set!")
		sys.exit(1)

	if FLICKR_SAFE_SEARCH < 1 or FLICKR_SAFE_SEARCH > 3:
		print("Invalid FLICKR_SAFE_SEARCH parameter (needs to be 1, 2 or 3)")
		sys.exit(1)

	#create directory if not exists
	if not os.path.exists(DOWNLOADPATH):
		os.makedirs(DOWNLOADPATH)
		#check again (paranoia check ;))
		if not os.path.exists(DOWNLOADPATH):
			print("%s doesn't exist!" %(DOWNLOADPATH,))
			sys.exit(1)
	
	if len(os.listdir(DOWNLOADPATH)) != 0:
		print("Folder %s needs to be empty!" %(DOWNLOADPATH,))
		sys.exit(1)

	try:
		page = START_PAGE
		flickr = flickrapi.FlickrAPI(FLICKR_API_KEY, FLICKR_API_SECRET, format='parsed-json')
		page, total_pages = download_all_images_at_page(flickr, page)
		page += 1
		while page < total_pages:
			page, total_pages = download_all_images_at_page(flickr, page)
			page += 1
	except KeyboardInterrupt:
		print("Aborted due to Ctrl+C")
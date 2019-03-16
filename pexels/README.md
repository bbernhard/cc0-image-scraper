# Howto

In order to run this script, set the `BASEPATH` and the `SEARCH_QUERY` variables inside the script. 

`BASEPATH`...the folder where script will save the images. (e.q: `/home/bernhard/pexels/`)

`SEARCH_QUERY`...the search expression (e.q: `dog`)


## How does it work?
The script uses Selenium's Webdriver to open pexels.com in a browser window to search the site for the provided search expression. 
It then scrolls down n times (can be controlled in the script with the `NUMBER_OF_SCROLL_DOWNS` variable) and extracts the image URLs
from the HTML. 

## Limitations/Todo's:

* the script doesn't automatically close the browser after it's done. 
  (i.e one has to close the browser window manually after the script prints `DONE`)
  
* change script to read parameters from commandline

#coding: UTF-8
import sys    #Importing the System Library
import urllib2
import json
tag=['cute','funny','baby','laughface','babyand']
search = 'cat'

#Downloading entire Web Document (Raw Page Content)
#Current Version of Python is 2.7
def download_page(url):

    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(req)
        page = response.read()
        return page
    except:
        return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        title="no more"
        return title,link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        start_title=s.find('"pt":',end_content+1)
        end_title=s.find(',"rid"',start_title+1)
        title_raw=str(s[start_title+6:end_title-1])
        return title_raw,content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while len(items)<10:#now each tag has 10 imgs
        d={}
        title, img, end_content = _images_get_next_item(page)
        if img == "no_links":
            break
        else:
            d[title]=img
            items.append(d)      #Append all the links in the list named 'Links'
            page = page[end_content:]
    return items

############## Main Program ############
#Download Image Links
tagimg=[]
for i in range(len(tag)):
    tagdict={}
    url = 'https://www.google.com/search?q=' + tag[i]+search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    raw_html =  (download_page(url))#all in json
    items =(_images_get_all_items(raw_html))
    tagdict[tag[i]]=items
    tagimg.append(tagdict)
with open("cat.json","w") as f:
    json.dump(tagimg,f, indent=4)
#print ("Image Links = "+str(items))
#print ("Total Image Links = "+str(len(items)))
print ("\n")

print("Everything downloaded!")

#----End of the main program ----#

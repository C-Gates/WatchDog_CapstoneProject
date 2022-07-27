#from flask import Flask, render_template
from os import remove
import random
import re

class Article():
    def __init__(self, title, desc, url, content, link):
        #duplicates do not matter for now, change if id needs to be unique (just for url display purposes)
        self.id = random.randint(100000,999999) 
        self.title = title
        self.desc = desc
        self.url = url
        self.content = content
        self.link = link
    
    def get_title(self):
        new_title = remove_html_tags(self.title)
        new_title = new_title.rsplit(" - ", 1)[0]
        return new_title

    def get_desc(self):
        return remove_html_tags(self.desc)
        

    def get_url(self):
        return self.url

    def get_content(self):
        new_content = remove_html_tags(self.content)
        new_content = new_content[:-14]
        return new_content

    def get_id(self):
        return self.id
    
    def get_link(self):
        return self.link


#remove clutter from APIs string such as html tags and random symbols that the API crawler picks up  
def remove_html_tags(html_string):
    CLEANR = re.compile('<.*?>') 
    new_str = html_string.replace("&ldquo;", "\'")
    new_str = new_str.replace("&rdquo;", "\'")
    new_str = new_str.replace("•", "")
    new_str = re.sub('&.*?;','',new_str)
    new_str = re.sub(CLEANR, '', new_str)

    return new_str

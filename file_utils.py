'''

Utility functions relating to files

'''

import time
import os
os.system("cls")    #Windows based systems us
import logging
import sys
import csv
from codecs import decode
import re

def filenameendsin(fname,filext):
    m = re.search(r'csv$',fname)
    if m:
      return True
    return False


def  write_to_file(fname, string):

  fo = open(fname, "a+") #append
  fo.write(string)
  fo.close()


def  write_list_to_file(fname, lst):
  fo = open(fname, "a+") #append
  for w in lst:
    fo.write("%s\n" % w)
  fo.close()




def  write_object_to_file(fname, obj):

  fo = open(fname, "a+") #append
  fo.write("\n\n\n\n")
  for o in obj:
    #for k,v in o.items():

    try:
      fo.write(unidecode(o["word"]).upper() + " :: " + unidecode(o["defn"]) + "\n")
    except Exception as e:
      print("Unprintable char found:", e)

  fo.close()

def  write_soup_to_file(fname, soup):

  fo = open(fname, "a+") #append
  fo.write("\n\n\n\n")
  for tag in soup:
    fo.write(tag)

  fo.close()
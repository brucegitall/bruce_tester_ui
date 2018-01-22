# -*- coding: utf-8 -*-	
#2018/1/22 使用了最新的方式使用这个功能 
#author Bruce
import os

def get_folder_files(load_folder,get_type = "path",end_word = None):
	path = os.path.abspath(load_folder)
	get_list = load_file_all_list(path)
	if end_word:
		get_list = filter(lambda x:True if x.endswith(end_word) else False,get_list)
	if get_type == "path":
		get_list = map( lambda x:os.path.join(path,x), get_list)
	return  get_list


def load_file_all_list(path):
	for r, d, files in os.walk(path ):
		get_list = files
		return  get_list
		
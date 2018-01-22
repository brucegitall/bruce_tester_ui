# -*- coding: utf-8 -*- 
import sys
import os
import re
def path2fp(x):
	if x[0] and os.path.exists(x[0]):
		x[0] = open(x[0],"r")
		if not x[1]:
			x[1] = "./dx.ini"
		return [x[0],open(x[1],"w")]
	return [None,None]
def Rlg2dx(list_path):
	fp_lists = map(path2fp,list_path)
	print fp_lists
	for fp_list in fp_lists:
		if None in fp_list:
			continue
		else:
			Rlg2dx_file(fp_list[0],fp_list[1])	
def Rlg2dx_file(rlg,dx):

	find = {}
	find["dovdd"] ={"re":r"dovdd\s+(\d+\.\d+)","value":-1}
	find["dvdd"] ={"re":r"dvdd\s+(\d+\.\d+)","value":-1}
	find["avdd"] ={"re":r"avdd\s+(\d+\.\d+)","value":-1}
	find["afvcc"] ={"re":r"af\s+(\d+\.\d+)","value":-1}


	find["VendorName"] ={"re":r"sensor_type\s+(\w+)\s+","value":-1}
	find["type"] ={"re":r"sensor_type\s+[\w]+\s+(\d)","value":-1}
	
	find["width"] = {"re":r"width\s+(\d+)","value":-1}
	find["height"] = {"re":r"height\s+(\d+)","value":-1}

	find["mclk"] = {"re":r"mclk\s+(\d+\.\d+)","value":-1}
	find["SlaveID"] = {"re":r"sensor\s+preview_i2c\s+(\w+)\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+","value":-1}
	find["mode"] = {"re":r"sensor\s+preview_i2c\s+\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*(\w+)","value":-1}
	find["ParaList"] = {"re":r"sensor\s+preview_i2c\s+\w+\s*[\,\，]\s*(\w+\s*[\,\，]\s*\w+)\s*[\,\，]\s*\w+","value":-1}

	find["SensorName"] = {"re":r"project_name\s+(\w+)\s+","value":-1}



	find["outformat"]  = {"re":r"data_format\s+(.+)[\s\n]","value":-1}
	find["type"]  = {"re":r"data_format\s+(.+)[\s\n]","value":-1}
	

	#find["FlagReg"]    = {}     
	#find["FlagData"]   = {}  
	#find["FlagMask"]   = {}  
	#find["FlagReg1"]   = {}  
	#find["FlagData1"]  = {}   
	#find["FlagMask1"]  = {}   

	find["port"] = {"re":r"\s+(\w+)\s+signal\smode","value":-1}
	#find["mode"] = {"re":r"signal\smode\s+(\d+)","value":-1}

	#quesitions
	# port ?
	# pin  ?
	# type ?
	# mode ?

	#find["exp_reg1"] = {}
	#find["exp_exp"] = {}
	#find["max_exp"] = {}
	#find["gain_reg1"] = {}
	#find["max_gain"] = {}

	

	dx.write("[Exposure-Gain]\n")


	

	


	

	dx.write("//Preview Type:0:Raw 10 bit; 1:Raw 8 bit; 2:YUV422; 3:RGB565  6:D_MIPI_RAW10\n")
	dx.write("//I2C Mode    :0:Normal 8Addr,8Data;  1:Samsung 8 Addr,8Data; \n")
	dx.write("//I2C Mode    :2:Micron 8 Addr,16Data\n")
	dx.write("//I2C Mode    :3:Stmicro 16Addr,8Data;4:Micron2 16 Addr,16Data\n")
	dx.write("//Out Format  :0:YCbYCr/RG_GB; 1:YCrYCb/GR_BG; 2:CbYCrY/GB_RG; 3:CrYCbY/BG_GR\n")
	dx.write("//MCLK Speed  :0:6M;1:8M;2:10M;3:11.4M;4:12M;5:12.5M;6:13.5M;7:15M;8:18M;9:24M;10:48M\n")
	dx.write("//pin  :BIT0 pwdn; BIT1:reset\n")
	dx.write("//port  0:MIPI; 1:Parallel; 2:MTK; 3:SPI; 4:TEST\n")
	dx.write("//avdd  0:2.8V; 1:2.5V; 2:1.8V\n")
	dx.write("//dovdd  0:2.8V; 1:2.5V; 2:1.8V\n")
	dx.write("//dvdd 0:1.8V;  1:1.5V; 2:1.2V\n")

	dx.write("[DataBase]\n")
	dx.write("DBName=Dothinkey\n")

	dx.write("[Vendor]\n")

	for line in rlg:
		for key in find.keys():
			if find[key]["value"] == -1:
				result = re.findall(find[key]["re"],line)
				if len(result) > 0:
					find[key]["value"] = result[0]
			










	dx.flush()
	dx.close()
	rlg.close()

if __name__ == "__main__":
	print sys.argv

	Rlg2dx([[sys.argv[1],sys.argv[2]]])


	

		
	
# -*- coding: utf-8 -*- 
import sys
import os
import re

import b_load
def path2fp(x):
	if x[0] and os.path.exists(x[0]):
		if not x[1]:
			x[1] = "./dx.ini"
		return [open(x[0],"r"),open(x[1],"w")]
	return 

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
	
	
	find["width"] = {"re":r"width\s+(\d+)","value":-1}
	find["height"] = {"re":r"height\s+(\d+)","value":-1}

	find["mclk"] = {"re":r"mclk\s+(\d+\.\d+)","value":-1}
	find["SlaveID"]={"re":r"sensor\s+preview_i2c\s+(\w+)\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+","value":-1}
	find["mode"] = {"re":r"sensor\s+preview_i2c\s+\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+\s*[\,\，]\s*\w+[xX]+(\w+)","value":-1}
	find["ParaList"] = {"re":r"sensor\s+preview_i2c\s+\w+\s*[\,\，]\s*(\w+\s*[\,\，]\s*\w+)\s*[\,\，]\s*\w+","value":[]}

	find["SensorName"] = {"re":r"project_name\s+(\w+)\s+","value":-1}



	find["outformat"]  = {"re":r"data_format\s+\w+\_(\w+)[\s\n]","value":-1}
	find["type"]  = {"re":r"data_format\s+(\w+)\_\w+[\s\n]","value":-1}
	

	find["pin_reset"]  = {"re":r"reset\_\w+\s+(\d+)[\s\n]+","value":-1}
	find["pin_pwnd"]   = {"re":r"pwnd\_\w+\s+(\d+)[\s\n]+","value":-1}


	find["port"] = {"re":r"\s+(\w+)\s+signal\smode","value":-1}




	for line in rlg:
		for key in find.keys():
			if find[key]["value"] == -1:
				result = re.findall(find[key]["re"],line)
				if len(result) >  0:
					find[key]["value"] = result[0]
			elif type(find[key]["value"]) == type([ ]):
				result = re.findall(find[key]["re"],line)
				if len(result) >  0:
					find[key]["value"].append(result[0])


	dx.write("//Preview Ty pe:0:Raw 10 bit,  1:Raw 8 bit,  2:YUV422,  3:RGB565   6:D_MIPI_RAW10\n")
	dx.write("//I2C Mode     :0:Normal 8Addr,8Data,   1:Samsung 8 Addr,8Data, \n")
	dx.write("//I2C Mode     :2:Micron 8 Addr,16Data\n")
	dx.write("//I2C Mode     :3:Stmicro 16Addr,8Data ,4:Micron2 16 Addr,16Data\n")
	dx.write("//Out Format   :0:YCbYCr/RG_GB,  1:YCrYCb/GR_BG,  2:CbYCrY/GB_RG,  3:CrYCbY/BG_GR\n")
	dx.write("//MCLK Speed   :0:6M,1:8M,2:10M ,3:11.4M ,4:12M ,5:12.5M ,6:13.5M ,7:15M ,8:18M ,9:24M, 10:48M\n")
	dx.write("//pin   :BIT0 pwdn, BI T1:reset\n")
	dx.write("//port   0:MIPI,  1:Parallel,  2:MTK,  3:SPI,  4:TEST\n")
	dx.write("//avdd   0:2.8V,  1:2.5V,  2:1.8V\n")
	dx.write("//dovdd   0:2.8V,  1:2.5V,  2:1.8V\n")
	dx.write("//dvdd  0:1.8V,   1:1.5V,  2:1.2V\n")
	dx.write("\n")

	dx.write("[DataBase]\n")
	dx.write("DBName=Dothinkey\n")
	dx.write("\n")

	dx.write("[Vendor]\n")
	dx.write("%s=%s\n"%("VendorName",find["VendorName"]["value"].upper()))
	dx.write("\n")

	dx.write("[Sensor]\n")
	dx.write("%s=%s %sX%s\n"%("SensorName",find["SensorName"]["value"].upper(),find["width"]["value"],find["height"]["value"]))
	dx.write("%s=%s\n"%("width",find["width"]["value"]))
	dx.write("%s=%s\n"%("height",find["height"]["value"]))

	dx_type = { "BAYLOR8":"1",  "YUYV422":"2" , "UYVY422":"2",  "RGB24":"3"  ,"BAYLOR10":"6"}
	dx.write("%s=%s\n"%("type",dx_type[find["type"]["value"].upper()]))

	dx_port = {"MIPI":"0",  "PARALLEL":"1",  "MTK":"2",  "SPI":"3"}
	dx.write("%s=%s\n"%("port",dx_port[find["port"]["value"].upper()]))

	dx.write("%s=%s\n"%("pin",str(int(find["pin_reset"]["value"])*2+int(find["pin_pwnd"]["value"]))))
	dx.write("%s=%s\n"%("SlaveID",find["SlaveID"]["value"]))


	dx_mode = {"1616":"4",  "1608":"3",  "0816":"2",  "0808":"0"}

	dx.write("%s=%s\n"%("mode",dx_mode[find["mode"]["value"]]))
	dx_outformat = {"RGGB":"0",  "GRBG":"1",  "GBRG":"2",  "BGGR":"3"}
	dx.write("%s=%s\n"%("outformat",dx_outformat[find["outformat"]["value"].upper()]))
	dx.write("\n")

	dx.write("%s=0\n"%("FlagReg",  ))#find["FlagReg"]["value"]))
	dx.write("%s=0\n"%("FlagData", ))#find["FlagData"]["value"]))
	dx.write("%s=0\n"%("FlagMask", ))#find["FlagMask"]["value"]))
	dx.write("%s=0\n"%("FlagReg1", ))#find["FlagReg1"]["value"]))
	dx.write("%s=0\n"%("FlagData1",))#find["FlagData1"]["value"]))
	dx.write("%s=0\n"%("FlagMask1",))#find["FlagMask1"]["value"]))

	
	dx_mclk =  {"6":"0" ,"8":"1" ,"10":"2" ,"11.4":"3" ,"12":"4" ,"12.5":"5" ,"13.5":"6","15":"7" ,"18":"8" ,"24":"9", "48":"10"}
	dx_avdd =  {"28":"0",  "25":"1",  "18":"2"}
	dx_dovdd =  {"28":"0",  "25":"1",  "18":"2"}
	dx_dvdd =  {"18":"0",   "15":"1",  "12":"2"}
	dx.write("%s=%s\n"%("mclk",dx_mclk[str(int(float(find["mclk"]["value"])))]))
	dx.write("%s=%s\n"%("avdd",dx_avdd[str(int(float(find["avdd"]["value"])))]))
	dx.write("%s=%s\n"%("dovdd",dx_dovdd[str(int(float(find["dovdd"]["value"])))]))
	dx.write("%s=%s\n"%("dvdd",dx_dvdd[str(int(float(find["dvdd"]["value"])))]))
	dx.write("%s=%s\n"%("afvcc",find["afvcc"]["value"]))
	dx.write("\n")


	dx.write("%s=0\n"%("Ext0",))#find["Ext0"]["value"]))
	dx.write("%s=0\n"%("Ext0",))#find["Ext0"]["value"]))
	dx.write("%s=0\n"%("Ext0",))#find["Ext0"]["value"]))
	dx.write("\n")

	dx.write("[Exposure-Gain]\n")
	dx.write("%s=0\n"%("exp_reg1",))#find["exp_reg1"]["value"]))
	dx.write("%s=0\n"%("exp_exp",))#find["exp_exp"]["value"]))
	dx.write("%s=0\n"%("max_exp",))#find["max_exp"]["value"]))
	dx.write("%s=0\n"%("gain_reg1",))#find["gain_reg1"]["value"]))
	dx.write("%s=0\n"%("max_gain",))#find["max_gain"]["value"]))
	dx.write("\n")

	dx.write("[ParaList]\n")
	for value in find["ParaList"]["value"]:
		dx.write("%s\n"%(value))
	#print find
	dx.flush()
	dx.close()
	rlg.close()
def  run():
	rlg_files = b_load.get_folder_files("./data",end_word = "txt")
	dx_files  =  map(lambda x:re.sub(r"\.[a-zA-Z]+$","_DX.ini",x),rlg_files)
	
	Rlg2dx(list(zip(rlg_files,dx_files)))
	pass

if __name__ == "__main__":

	run()


	

		
	
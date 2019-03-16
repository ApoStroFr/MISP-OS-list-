import pathlib
import json
import sys
import os
import re

part=sys.argv[1]
vendor=sys.argv[2]
product=sys.argv[3]

dicoVendors={'Product':product}
dicoCPE={'Vendor':vendor, 'Product':product}

if str(sys.argv[4]) != "'*'":
	dicoCPE["Version"]=str(sys.argv[4])[1:-1]
	dicoVendors["Version"]=str(sys.argv[4])[1:-1]

if str(sys.argv[5]) != "'*'":
	dicoCPE["Update"]=str(sys.argv[5])[1:-1]
	dicoVendors["Update"]=str(sys.argv[5])[1:-1]

if str(sys.argv[6]) != "'*'":
	dicoCPE["Edition"]=str(sys.argv[6])[1:-1]
	dicoVendors["Edition"]=str(sys.argv[6])[1:-1]

if str(sys.argv[7]) != "'*'":
	dicoCPE["Language"]=str(sys.argv[7])[1:-1]
	dicoVendors["Language"]=str(sys.argv[7])[1:-1]

if str(sys.argv[8]) != "'*'":
	dicoCPE["SoftwareEdition"]=str(sys.argv[8])[1:-1]
	dicoVendors["SoftwareEdition"]=str(sys.argv[8])[1:-1]

if str(sys.argv[9]) != "'*'":
	dicoCPE["TargetSoftware"]=str(sys.argv[9])[1:-1]
	dicoVendors["TargetSoftware"]=str(sys.argv[9])[1:-1]

if str(sys.argv[10]) != "'*'":
	dicoCPE["TargetHardware"]=str(sys.argv[10])[1:-1]
	dicoVendors["TargetHardware"]=str(sys.argv[10])[1:-1]

if str(sys.argv[11]) != "'*'":
	dicoCPE["Other"]=str(sys.argv[11])[1:-1]
	dicoVendors["Other"]=str(sys.argv[11])[1:-1]

#Création des données Json pour hrdw.json sftw.json et os.json

dicoCPE2Json = json.dumps(dicoCPE, indent=4, sort_keys=True)

#Si la valeur part du xml == h alors le produit est Hardware
if part == "h":
	with open("/root/misp_project/Apush/hrdw.json", "a") as jsonFile:
		jsonFile.write(dicoCPE2Json)
		jsonFile.write(",\n")
	dicoVendors["TypeOfProduct"]="Hardware"

#Si la valeur part du xml == a alors le produit est un Software
elif part == "a":
	with open("/root/misp_project/Apush/sftw.json", "a") as jsonFile:
		jsonFile.write(dicoCPE2Json)
		jsonFile.write(",\n")
	dicoVendors["TypeOfProduct"]="Software"

#Si la valeur part du xml == o alors le produit est un OS
elif part == "o":
	with open("/root/misp_project/Apush/os.json", "a") as jsonFile:
		jsonFile.write(dicoCPE2Json)
		jsonFile.write(",\n")
	dicoVendors["TypeOfProduct"]="OperatingSystem"

dicoVendors2json =json.dumps(dicoVendors, indent=4, sort_keys=True)

p = pathlib.Path('/root/misp_project/Apush/vendor/'+vendor+'.json')
if p.is_file():
	with open('/root/misp_project/Apush/vendor/'+vendor+'.json', "a") as vendorjson:
		vendorjson.write(dicoVendors2json+",\n")
else:
	with open('/root/misp_project/Apush/vendor/'+vendor+'.json', "a") as vendorjson:
		vendorjson.write(vendor+":{\n")
		vendorjson.write(dicoVendors2json+",\n")

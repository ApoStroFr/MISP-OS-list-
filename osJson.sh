#!/bin/bash

#Estimation du temps passé
start=$(date)

source /root/misp_project/Apush/progress_bar.sh

#Cleanup the bar if ctrl+C
enable_trapping

#Initialise the progress bar
setup_scroll_area

#Prepare the % calcul for the progress bar
nbline=$(wc -l $1 | cut -d" " -f1)
currentline=1



#Init the *.json file
echo '"Hardware":[' > /root/misp_project/Apush/hrdw.json
echo '"OperatingSystem":[' > /root/misp_project/Apush/os.json
echo '"Software":[' > /root/misp_project/Apush/sftw.json

#Je récupe mon xml
filename=$1

#Je lis ligne par ligne mon xml et récupère tous les produits qui corespond 
#à un produit (que ce soit OS/software/hardware)
while read line
do
	cpe=$(echo "$line")
	if [[  $cpe =~ "cpe-23:cpe23-item name=\"cpe:2.3:" ]]
	then
		part=$(echo $cpe | cut -d':' -f4)
		vendor=$(echo $cpe | cut -d':' -f5)
		product=$(echo $cpe | cut -d':' -f6)
		version=$(echo $cpe | cut -d':' -f7)
		update=$(echo $cpe | cut -d':' -f8)
		edition=$(echo $cpe | cut -d':' -f9)
		language=$(echo $cpe | cut -d':' -f10)
		sofEd=$(echo $cpe | cut -d':' -f11)
		targSft=$(echo $cpe | cut -d':' -f12)
		targHrd=$(echo $cpe | cut -d':' -f13)
		other=$(echo $cpe | cut -d':' -f14 | cut -d'"' -f1)

		if [[ $vendor =~ \/ ]]
		then
			vendor=$(echo $vendor | sed -e -i 's/\/\_/g')
		fi

		#Programme python qui créer les fichiers json
		python3 createJson.py "$part" "$vendor" "$product" "'$version'" "'$update'" "'$edition'" "'$language'" "'$sofEd'" "'$targSft'" "'$targHrd'" "'$other'"
	fi

	#CALCUL DU % POUR PROGRESS BAR
	pourcent=$(($currentline*100/$nbline))
	draw_progress_bar $pourcent

	#Incrément de la page
	currentline=$(($currentline+1))

done < $filename
destroy_scroll_area

echo $start
date

#Delete le , en trop dans les fichiers json
truncate -s-1 /root/misp_project/Apush/vendor/*.json

#Supprime le dernier caractère des fichiers (les virgules)
# Possibilité de devoir re-executer ces commandes plusieurs fois
# car caractère \n...
sed 's/$/\n}/' /root/misp_project/Apush/vendor/*.json
sed 's/$/\n}/' /root/misp_project/Apush/*.json


#Ajoute une } pour fermer les json
sed -i -e '$a\}' /root/misp_project/Apush/vendor/*.json

#Ajoute un } pour fermer les json
sed -i -e '$a\]' /root/misp_project/Apush/*.json

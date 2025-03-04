less herbs_name_alias.raw|awk -F "\t" '{ split($2,array,"；"); for(i in array) {print $1"\t"array[i];}}' > herbs_name_alias.txt
less herbs_name_alias.txt |grep -v "^#"|awk -F "\t" '{print $1"\n"$2}'|sort|uniq -c|awk '{if($1==1) print $2}'|perl ../match-herbs-uniq.pl - herbs_name_alias.txt uniq-alias-result.txt
python ../rename_standardization.py -i extract.txt -l oooo -o final.result

#Remove rare character problem after encoding. If the herbs have no alias name, remain themselves and do not take any change.

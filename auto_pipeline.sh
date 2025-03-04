#!/bin/sh

prescription_dataset=""
cutoff_value=""
execute_pathdir=""

while getopts "i:c:e:" opt; do
	case $opt in
		i)
			prescription_dataset=$OPTARG
			;;
		c)
			cutoff_value=$OPTARG
			;;
		e)
			execute_pathdir=$OPTARG
			;;
		\?)
			echo "Invalid option: -$OPTARG"
			exit 1
			;;
	esac
done

shift $((OPTIND-1))

if [ -z "$prescription_dataset" ]; then
	echo "Error: Missing required argument for -i <prescription_dataset>"
	exit 1
fi

if [ -z "$cutoff_value" ]; then
	echo "Error: Missing required argument for -c <cutoff_value>"
	exit 1
fi

if [ -z "$execute_pathdir" ]; then
	echo "Error: Missing required argument for -e <execute_pathdir>"
	exit 1
fi

echo "Prescription Dataset": $prescription_dataset""
echo "Cutoff Value": $cutoff_value""
echo "Execute Pathdir: $execute_pathdir"
echo "\n";
echo "====================================================";
echo "Example: sh $0 prescription.txt /software/ 0.001"
echo "Edit by Jidong Lang; E-mail: langjidong@hotmail.com;";
echo "====================================================";

#Herbs Alias Name Normalization
python $execute_pathdir/script/rename_standardization.py -i $prescription_dataset -l $execute_pathdir/script/database/uniq-alias-result.txt -o rename_normalization.txt
python $execute_pathdir/script/txt2excel.py -i rename_normalization.txt -o rename_normalization.xlsx

####Transform Hanzi to Pinyin, excel_file to txt_file, and extract the specific system information####
python $execute_pathdir/script/hanzi2pinyin.py -i rename_normalization.xlsx -o $prescription_dataset.py.xlsx
python $execute_pathdir/script/excel2txt.py -i $prescription_dataset.py.xlsx -o file.txt
rm -rf rename_normalization.xlsx $prescription_dataset.py.xlsx

####Make training dataset input####
mkdir Tmp Tmp-1
less file.txt|grep -v "^方剂"|awk -F "\t" '{print $1"\t"$2}'|while read a b;do echo "${b}" > Tmp/${a}.tmp;done
cd Tmp
ls *.tmp|awk -F ".tmp" '{print $1}' > index-list
cp index-list ../Tmp-1/
less index-list|while read a;do less ${a}.tmp|perl -e 'while(<>) {chomp; $_=~s/\s+//g; $_=~s/、/\n/g; print "$_\n";}'|sort -u|awk -F "\t" '{print $1"\t""1"}' > ${a}.txt;done
less index-list|while read a;do less ${a}.tmp|perl -e 'while(<>) {chomp; $_=~s/\s+//g; $_=~s/、/\n/g; print "$_\n";}'|sort -u|awk -F "\t" '{print $1}' > ../Tmp-1/${a}.txt;done
less index-list|while read a;do less ${a}.tmp|perl -e 'while(<>) {chomp; $_=~s/\s+//g; $_=~s/、/\n/g; print "$_\n";}'|sort -u|awk -F "\t" '{print $1}';done|sort|uniq -c|sort -rnk1|awk '{print $2}' > gene-list
rm -rf *.tmp
less index-list|while read a;do mkdir ${a};done
less index-list|while read a;do less ${a}.txt|awk '{print $1}' > ${a}/${a}-list;done
less index-list|while read a;do cp gene-list ${a};done
less index-list|while read a;do perl $execute_pathdir/script/compare.pl ./${a}/${a}-list ./${a}/gene-list;done
less index-list|while read a;do cat ${a}/${a}-list.special.xls;done
less index-list|while read a;do less ${a}/gene-list.special.xls|awk '{print $0"\t""0"}' >> ${a}.txt;done
less index-list|while read a;do rm -rf ${a};done
less index-list|while read a;do less ${a}.txt|wc -l;done|sort -u
less index-list|while read a;do perl $execute_pathdir/script/match_single_cell.pl gene-list ${a}.txt ${a}.info;done
less index-list|while read a;do rm -rf ${a}.txt;done
mkdir tmp
less index-list|while read a;do less ${a}.info |awk -F "\t" '{print $1}' > tmp/${a}.tmp1;done
less index-list|while read a;do less ${a}.info |awk -F "\t" '{print $2}' > tmp/${a}.tmp2;done
less index-list|head -n 1|while read b;do less index-list|while read a;do diff tmp/${b}.tmp1 tmp/${a}.tmp1;done;done
python $execute_pathdir/script/mergefile.py -i index-list -d tmp/ -o mergefile.info
less index-list|head -n 1|while read a;do cp tmp/${a}.tmp1 column_index.info;done
paste column_index.info mergefile.info > all.tmp
less index-list|perl -e 'while(<>) {chomp; print"\t$_";} print "\n"' > title
cat title all.tmp > ../training_dataset.txt
cd ../
rm -rf Tmp/ file.txt

####Transpose the matrix####
python $execute_pathdir/script/transpose_matrix.py -i training_dataset.txt -o training_dataset-transposed.txt

####Transform the tree generation file####
less training_dataset.txt|perl -e '<>; while(<>) {chomp; @tmp=split(/\t/,$_,2); $tmp[1]=~s/\t//g; $tmp[1]=~s/1/A/g; $tmp[1]=~s/0/T/g; print ">$tmp[0]\n$tmp[1]\n";}' > herb.tree.fasta
less training_dataset-transposed.txt|perl -e '<>; while(<>) {chomp; @tmp=split(/\t/,$_,2); $tmp[1]=~s/\t//g; $tmp[1]=~s/1.0/A/g; $tmp[1]=~s/0/T/g; print ">$tmp[0]\n$tmp[1]\n";}' > prescription.tree.fasta

####tree analysis####
####Extract Chinese name to English name####
iqtree2 -s herb.tree.fasta -b 1000 -T AUTO
iqtree2 -s prescription.tree.fasta -b 1000 -T AUTO

####Extract the baseline prescription herbs####
python $execute_pathdir/script/extract_baseinfo.py -i herb.tree.fasta.log -c $cutoff_value -o base_prescription.txt

####Caculate the goodness of fit####
python $execute_pathdir/script/goodness_fit.py -b base_prescription.txt -d Tmp-1/ -o goodness_fit.txt
#rm -rf Tmp-1

####Caculate the similarity value####
python $execute_pathdir/script/prescription_similarity.py -a training_dataset.txt -b base_prescription.txt -o caculater_similarity.txt

####Tree Plotting####
Rscript $execute_pathdir/script/tree_plot.R

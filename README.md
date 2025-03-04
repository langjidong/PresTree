# PresTree: A Workflow for Analysis of Basic Formula and Prescription Pattern

PresTree is a prescription tree workflow for analyzing basic formulas and prescription patterns. It can effectively and accurately identify the basic formulas in sizeable prescription sets while also providing a systematic analysis of prescription sets from a macro perspective. PresTree can be used for extensive analysis of the common features between prescription subsets and a clear description of the prescription structure, offering a new tool and reference for the optimization and innovation of TCM prescriptions.

Option

<prescript_dataset>  The file contains prescrition dataset, format is "prescription_name\tprescription_composition", and the prescription composition is separated by a Chinese Comma;
<cutoff_value>  The p-value cutoff;
<execute_path>  The pathdir of used scripts;

Example: <br />
** sh auto_pipeline.sh -i simulation.txt -c 0.00001 -e ./**
```
simulation.txt file format:
方剂\t方剂组成
四君子汤\t人参、白术、茯苓、炙甘草
附子理中汤\t人参、白术、炙甘草、炮附子、干姜
```

***Contact and E-mail: langjidong@hotmail.com***

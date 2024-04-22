# qif-to-csv
Using python to try to make csv file from qif file

usage :
qif2csv.py myqiffile

or to create an output csv file
qif2csv.py myqiffile -o outputcsvfile

Warning !
myqiffile is supposed to be a latin-1 encoded file, if not, change encoding='latin-1' to encoding='yourencoding')
outputcsvfile will be utf-8 encoded

Thanks to TheAntimist for the generic Argumentparser object usage


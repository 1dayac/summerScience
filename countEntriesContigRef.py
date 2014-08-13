__author__ = 'Dmitrii'
from Bio import SeqIO
import sys
import os
import getopt
#import time

def usage():
    print 'usage: countEntriesContigRef.py contigs.fa reference.fa contigs.astat'
    print 'Find set of contigs with likely unique copy number'
    print 'Options:'
    print '    -align-rate INT (0-100)         minimum rate of good aligned bp needed to keep alignment (default - 95)'
    print '    -length-diff INT                maximum difference of length between contig and part of reference to keep alignment (default - 10)'

if len(sys.argv) <= 2:
    usage()
    exit()

align_rate = 0.95
length_diff = 10
astat = 600

opts, args = getopt.getopt(sys.argv[1:], "", ["align-rate", "length-diff"])

for o, a in opts:
   if o == "align-rate":
       align_rate = float(a)
   elif o == "length-diff":
       length_diff = int(a)
   elif o == "astat":
       astat = int(a)

os.system("makeblastdb -in " + sys.argv[2] + " -dbtype nucl")
#time.sleep(25)
os.system("blastn -db " + sys.argv[2] + " -query " + sys.argv[1] + " -outfmt 6 -dust yes -word_size 50 -evalue 10 -out results.txt")
#time.sleep(25)


query_fasta = SeqIO.to_dict(SeqIO.parse(open(sys.argv[1], "rU"), "fasta"))

result_dict = {}



with open("results.txt", 'r') as blastFile:
    for line in blastFile:
        split_line = line.split('\t')
        contig_name = split_line[0]
        if len(query_fasta[contig_name]) - length_diff <= int(split_line[3]):
            if contig_name in result_dict:
                result_dict[contig_name] += 1
            else:
                result_dict[contig_name] = 1



ok_unique = 0
not_ok_unique = 0
ok_multiple = 0
not_ok_multiple = 0

numberOfAl = {}

lengthes_unique = set()
lengthes_unique_wrong = set()
lengthes_multiple = set()
lengthes_multiple_wrong = set()

with open(sys.argv[3], 'r') as astatFile:
    for line in astatFile:
#        print(line)
        line_splited = line.split()
        if float(line_splited[5]) > astat:
            if line_splited[0] not in result_dict or result_dict[line_splited[0]] <= 1:
                print(line_splited[0] + " - ok - unique or missing")
                ok_unique += 1
                lengthes_unique.add(line_splited[1])
            else:
                print(line_splited[0] + " - not ok - unique A-stat but multiple alignments")
                not_ok_unique += 1
                if result_dict[line_splited[0]] in numberOfAl:
                    numberOfAl[result_dict[line_splited[0]]] += 1
                else:
                    numberOfAl[result_dict[line_splited[0]]] = 1
                lengthes_unique_wrong.add(line_splited[1])

        else:
            if line_splited[0] not in result_dict or result_dict[line_splited[0]] <= 1:
                print(line_splited[0] + " - not ok - multiple A-stat and unique or missing alignments")
                not_ok_multiple += 1
                lengthes_multiple_wrong.add(line_splited[1])
            else:
                print(line_splited[0] + " - ok - multiple A-stat and multiple alignments")
                ok_multiple += 1
                lengthes_multiple.add(line_splited[1])

print("ok - unique or missing - " + str(ok_unique))
print(lengthes_unique)
print("not ok - unique A-stat but multiple alignments - " + str(not_ok_unique))
print(lengthes_unique_wrong)

print("not ok - multiple A-stat and unique or missing alignments - " + str(not_ok_multiple))
print(lengthes_multiple_wrong)
print("ok - multiple A-stat and multiple alignments - " + str(ok_multiple))
print(lengthes_multiple)

print(numberOfAl)

os.system("rm results.txt");

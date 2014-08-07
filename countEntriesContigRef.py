__author__ = 'Dmitrii'

from Bio import SeqIO
import sys
import os

os.system("makeblastdb -in " + sys.argv[1] + " -dbtype nucl");
os.system("blastn -db " + sys.argv[2] + " -query " + sys.argv[1] + " -outfmt 6 -dust yes -word_size 50 -evalue 10 -out results.txt");


query_fasta = SeqIO.to_dict(SeqIO.parse(open(sys.argv[1], "rU"), "fasta"))

result_dict = {}



with open("results.txt", 'r') as blastFile:
    for line in blastFile:
        split_line = line.split('\t')
        contig_name = split_line[0]
        if len(query_fasta[contig_name]) * 0.96 <= int(split_line[3]):
            if contig_name in result_dict:
                result_dict[contig_name] += 1
            else:
                result_dict[contig_name] = 1



ok_unique = 0
not_ok_unique = 0
ok_multiple = 0
not_ok_multiple = 0

numberOfAl = {}

with open(sys.argv[3], 'r') as astatFile:
    for line in astatFile:
        line_splited = line.split()
        if float(line_splited[5]) > 20.0:
            if line_splited[0] not in result_dict or result_dict[line_splited[0]] <= 1:
                print(line_splited[0] + " - ok - unique or missing")
                ok_unique += 1
            else:
                print(line_splited[0] + " - not ok - unique A-stat but multiple alignments")
                not_ok_unique += 1
                if result_dict[line_splited[0]] in numberOfAl:
                    numberOfAl[result_dict[line_splited[0]]] += 1
                else:
                    numberOfAl[result_dict[line_splited[0]]] = 1
        else:
            if line_splited[0] not in result_dict or result_dict[line_splited[0]] <= 1:
                print(line_splited[0] + " - not ok - multiple A-stat and unique or missing alignments")
                not_ok_multiple += 1
            else:
                print(line_splited[0] + " - ok - multiple A-stat and multiple alignments")
                ok_multiple += 1

print("ok - unique or missing - " + str(ok_unique))
print("not ok - unique A-stat but multiple alignments - " + str(not_ok_unique))
print("not ok - multiple A-stat and unique or missing alignments - " + str(not_ok_multiple))
print("ok - multiple A-stat and multiple alignments - " + str(ok_multiple))

print(numberOfAl)

os.system("rm results.txt");

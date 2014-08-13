###Script for working with A-statistic results from SGA-assembler.

##Usage

python countEntriesContigRef.py file_with_contigs.fa file_with_reference.astat [options]

astat-file is file, produced during SGA-assembler work when scaffolding.

Options are next:
-align-rate INT (0-100)         minimum rate of good aligned bp needed to keep alignment (default - 95)
-length-diff INT                maximum difference of length between contig and part of reference to keep alignment (default - 10)
-astat INT											lower astat-threshold for counting contig as unique (default - 600)

##Output

Script outputs list of alignments, for which blast found any results with decision and conclusion - is this alignment rate consistent with A-statistic.
Then summary for all contigs + list of lengths for this contigs.

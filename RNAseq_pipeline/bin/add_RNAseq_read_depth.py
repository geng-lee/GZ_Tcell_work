#!/usr/bin/python3
import sys
import os
import re
import pandas as pd


def addtwodimdict(thedict, key_a, key_b, val):
    ''' this is a function to add two dimetion dict '''
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a: {key_b: val}})
    return thedict


def deal_mpileup(RNAseq_mpileup_file):
    a_dict = {}
    with open(RNAseq_mpileup_file, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            chrom, pos, mapped_base, reads_count, mapping_info, mapping_qul = line.split("\t")
            match = re.search(r'[ATCG]',mapping_info.upper())
            if match:
                match.group()
                mutatype = mapping_info.upper().count(match.group())
            else:
                mutatype = 0
            wildtype = int(reads_count) - mutatype 
            addtwodimdict(a_dict, pos, 'W', wildtype)
            addtwodimdict(a_dict, pos, 'M', mutatype)
    return a_dict

xls_file = sys.argv[1]
RNAseq_mpileup_file = sys.argv[2]

mpileup_dict = deal_mpileup(RNAseq_mpileup_file)
# print(mpileup_dict)

contain_fields = [
        "Hugo_Symbol", "Entrez_Gene_Id", "Center", "NCBI_Build", "Chromosome",
        "Start_Position", "Strand", "Variant_Classification", "Variant_Type", "Reference_Allele", 
        "Tumor_Seq_Allele1", "Tumor_Seq_Allele2", "dbSNP_RS", "Genome_Change", "Annotation_Transcript", 
        "Transcript_Strand", "Transcript_Exon", "cDNA_Change", "Codon_Change", "Protein_Change",
        "Refseq_mRNA_Id", "tumor_f", "t_alt_count", "t_ref_count", "n_alt_count",
        "n_ref_count", "DP", "Mutated_Minigene", "Wild-Type_Minigene",
        "MutatedReads(RNA)", "Wild-typeReads(RNA)", "TPM",
    ]
output_file = open(os.path.basename(xls_file).rstrip("xls")+'RNA_Depth.xls', "w")
output_file.write("{}\n".format("\t".join(contain_fields)))

data = pd.read_table(xls_file, sep="\t")
for index, row in data.iterrows():
    Position_start = str(row["Start_Position"])
    if Position_start in mpileup_dict:
        RNA_wild_reads = int(mpileup_dict[Position_start].get("W", 0))
        RNA_muta_reads = int(mpileup_dict[Position_start].get("M", 0))
    else:
        RNA_wild_reads = 0
        RNA_muta_reads = 0
    output_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
        row["Hugo_Symbol"], row["Entrez_Gene_Id"], row["Center"], row["NCBI_Build"], row["Chromosome"],
        row["Start_Position"], row["Strand"], row["Variant_Classification"], row["Variant_Type"], row["Reference_Allele"],
        row["Tumor_Seq_Allele1"], row["Tumor_Seq_Allele2"], row["dbSNP_RS"], row["Genome_Change"], row["Annotation_Transcript"],
        row["Transcript_Strand"], row["Transcript_Exon"], row["cDNA_Change"], row["Codon_Change"], row["Protein_Change"],
        row["Refseq_mRNA_Id"], row["tumor_f"], row["t_alt_count"], row["t_ref_count"], row["n_alt_count"], 
        row["n_ref_count"], row["DP"],row["Mutated_Minigene"],row["Wild-Type_Minigene"],RNA_muta_reads,RNA_wild_reads, 
        row["TPM"],
        ))

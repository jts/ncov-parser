'''
A class for handling allele date from the alleles.tsv files generated by the
ARTIC nCoV pipeline.
'''

import os
import sys
import csv
import re

class Alleles():
    '''
    The Alleles class for handling the alleles.tsv file.
    '''

    def __init__(self, file, delimiter='\t'):
        '''
        Initilize the Alleles object.
        '''
        if os.path.exists(file):
            self.file = file
        else:
            sys.exit("Invalid or missing file.")
        self.delimiter = delimiter
        self.data = dict()
        with open(self.file) as file_p:
            csv_reader = csv.DictReader(file_p, delimiter=self.delimiter)
            for record in csv_reader:
                samplename = re.sub('^Consensus_', '', record['name'])
                samplename = re.sub('/ARTIC/nanopolish', '', samplename)
                samplename = re.sub('/ARTIC/medaka', '', samplename)

                if samplename not in self.data:
                    self.data[samplename] = {record['pos'] : {
                        'ref' : record['ref_allele'],
                        'alt' : record['alt_allele']}}
                else:
                    self.data[samplename][record['pos']] = {
                        'ref' : record['ref_allele'],
                        'alt' : record['alt_allele']}


    def get_variant_counts(self, sample):
        '''
        Import the data from the alleles.tsv file and count the number of
        variants (i.e. IUPAC, SNV).

        Arguments:
            * delimiter: the field delimiter in the file [optional]

        Return value:
            Method returns a dictionary containing sample names and the
            number of SNVs and IUPAC.
        '''
        total_snvs = 0
        if sample in self.data:
            for pos in self.data[sample]:
                if not is_variant_iupac(variant=self.data[sample][pos]['alt']):
                    total_snvs += 1
        return {'num_consensus_snvs' : total_snvs}


def is_variant_iupac(variant):
    '''
    A function to determine whether a variant is an IUPAC code, note that
    we are treating N as a distinct value.

    Arguments:
        * variant: a string representing the variant

    Return Value:
        Function returns a boolean
    '''
    variant = str(variant).upper()
    iupac_codes = '[RYSWKMBDHVN]'
    return re.search(iupac_codes, variant)


def is_variant_base(variant):
    '''
    A method to determine whether a variant is a valid nucleotide.

    Arguments:
        * variant: a string representing the variant

    Return value:
        Method returns a boolean.
    '''
    variant = str(variant).upper()
    bases = '[ACTG]'
    return re.search(bases, variant)
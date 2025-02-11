# -*- coding: utf-8 -*-
"""
YOUR HEADER COMMENT HERE

@author:

"""

import random
from amino_acids import aa, codons, aa_table   # you may find these useful
from load import load_seq


def shuffle_string(s):
    """Shuffles the characters in the input string
        NOTE: this is a helper function, you do not
        have to modify this in any way """
    return ''.join(random.sample(s, len(s)))

# YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """

    if nucleotide == "A":
        return "T"
    if nucleotide == "T":
        return "A"
    if nucleotide == "C":
        return "G"
    if nucleotide == "G":
        return "C"


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence

        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """

    c_dna =[]
    for letter in dna:
        n_dna = get_complement(letter)
        c_dna.append(n_dna)

    complementary_dna = "".join(c_dna)

    return complementary_dna[ : :-1]


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start
        codon and returns the sequence up to but not including the
        first in frame stop codon.  If there is no in frame stop codon,
        returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """

    stop_codons = ["TAG", "TAA","TGA"]
    for i in range(0,len(dna),3):
        codon = dna[i:i+3]
        for stop in stop_codons:
            if (codon == stop):
                return dna [:i]
    return dna

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA
        sequence and returns them as a list.  This function should
        only find ORFs that are in the default frame of the sequence
        (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    stop_codons = ['TAA', 'TAG', 'TGA']
    start_codon = 'ATG'
    orfs = []
    i =0

    while i < len(dna):
        codon = dna[i:i+3]
        if (codon == start_codon):
            orf = rest_of_ORF(dna[i:])
            orfs.append(orf)
            i = i + len(orf)
        i = i +3
    return orfs


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in
        all 3 possible frames and returns them as a list.  By non-nested we
        mean that if an ORF occurs entirely within another ORF and they are
        both in the same frame, it should not be included in the returned list
        of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    return [i for j in range(0,3) for i in find_all_ORFs_oneframe(dna[j:])]


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    longest = ''
    for orf in find_all_ORFs_both_strands(dna):
    	if len(orf) > len(longest):
    		longest = orf
    return longest

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    res = 0
    for i in range(num_trials):
    	working_dna = shuffle_string(dna)
    	if len(longest_ORF(working_dna)) > res:
    		res = len(longest_ORF(working_dna))
    return res


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).

        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    acid = ''
    for i in range(0,int(len(dna)/3)):
    	acid = acid + aa_table[dna[3*i:3*(i+1)]]
    return acid


def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna

        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna,1500)
    orfs = find_all_ORFs_both_strands(dna)
    genes = []
    for orf in orfs:
        if len(orf) > threshold:
            genes.append(coding_strand_to_AA(orf))
    return genes


if __name__ == "__main__":
#     import doctest
#     # doctest.testmod()
#     doctest.run_docstring_examples(coding_strand_to_AA,globals(), verbose=True)

    dna = load_seq("./data/X73525.fa")
    print(gene_finder(dna))

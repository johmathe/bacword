"""Process all bacteria dataset."""

import glob
import gzip
import h5py
import os
import ssl
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

DATA_PATH = './data/'
ASSEMBLY_URL = 'https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt'  # NOQA
ASSEMBLY_PATH = os.path.join(DATA_PATH, 'assembly_summary.txt')
ASSEMBLY_HEADERS = {
    "# assembly_accession": str,
    "bioproject": str,
    "biosample": str,
    "wgs_master": str
}
OUTPUT_FILE = 'output.hdf5'

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)


def line_to_gene_name_if_gene(line):
    if line[0] != '>':
        return None
    return ' '.join(line.strip().split(' ')[1:])


def run():
    files = glob.glob('%s/genes/*.gz' % DATA_PATH)
    with h5py.File(OUTPUT_FILE, 'w') as out:
        # TODO(johmathe): Process more data
        MAX = 100000
        for filename in files[:MAX]:
            print('processing %s' % filename)
            with gzip.open(filename, 'rt') as f:
                genes = []
                for line in f:
                    gene = line_to_gene_name_if_gene(line)
                    if gene:
                        genes.append(gene)
                genes = np.array(genes, dtype='S')
                out.create_dataset(filename, data=genes)


if __name__ == '__main__':
    run()

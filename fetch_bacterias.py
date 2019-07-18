"""Download all bacteria dataset."""

import os
import pandas as pd
import ssl
import urllib.request


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


def fetch_all_prots(target_path):
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    if not os.path.exists(ASSEMBLY_PATH):
        urllib.request.urlretrieve(ASSEMBLY_URL, ASSEMBLY_PATH)

    bacterias = pd.read_csv(
        ASSEMBLY_PATH,
        delimiter='\t',
        dtype=ASSEMBLY_HEADERS,
        header=1)

    for index, row in bacterias.iterrows():
        url = 'https%s/%s_%s_protein.faa.gz' % (
            row['ftp_path'][3:], row['# assembly_accession'], row['asm_name'])
        path = '%s/%s_%s.txt' % (DATA_PATH, row['# assembly_accession'],
                                 row['asm_name'])
        if not os.path.exists(path):
            print('%s -> %s' % (url, path))
            urllib.request.urlretrieve(url, path)
        else:
            print('%s already exists' % path)


if __name__ == '__main__':
    fetch_all_prots(target_path=DATA_PATH)

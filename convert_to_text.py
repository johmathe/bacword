import h5py

HDF5_file = 'output.hdf5'


def run(input_file, output_file):
    with h5py.File(input_file, 'r') as h5file:
        with open(output_file, 'w') as output_buf:
            for key in h5file['data']['genes'].keys():
                genes = h5file['data']['genes'][key]
                for g in genes:
                    output_buf.write('%s ' %
                                     g.decode('ascii').replace(' ', '_'))
                output_file.write('\n')


if __name__ == '__main__':
    run('output.hdf5', 'corpus.txt')

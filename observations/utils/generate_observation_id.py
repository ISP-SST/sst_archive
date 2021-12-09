import re

from astropy.io import fits

from observations.utils import generate_sparse_list_string


FILENAME_SCANS_REGEX = re.compile(r'.*_scans=(?P<scans>[^_]+).*')


def _descend_into_multi_dim_array(array, levels, index=0):
    result = array
    for i in range(levels):
        result = result[index]
    return result


def _generate_sparse_scans_list_string(fits_hdus):
    primary_fits_header = fits_hdus[0].header

    try:
        scannum_ext_index = fits_hdus.index_of('VAR-EXT-SCANNUM')

        scannum_ext = fits_hdus[scannum_ext_index]
        scannum_col_name = scannum_ext.header['TTYPE1']
        scannum_dim = scannum_ext.header['TDIM1']

        scannum_field = scannum_ext.data.field(scannum_col_name)[0]

        dimensions_to_ignore = len(scannum_dim[1:-1].split(',')) - 1

        scan_numbers = [_descend_into_multi_dim_array(scannum, dimensions_to_ignore) for scannum in scannum_field]

        scannum_list = generate_sparse_list_string(scan_numbers)
    except KeyError as e:
        scannum_list = str(primary_fits_header['SCANNUM'])

    return scannum_list


def _get_scan_list_from_filename(fits_hdus):
    """
    Extracts the scan sequence from the filename. If the filename is not provided on the expected format the function
    will generate a similar (though not identical) string of sparse scans on its own.
    """
    primary_fits_header = fits_hdus[0].header

    filename = primary_fits_header['FILENAME']
    result = FILENAME_SCANS_REGEX.match(filename)

    if result:
        return result.group('scans')
    else:
        return _generate_sparse_scans_list_string(fits_hdus)


def _get_sparse_scans_list_string(fits_hdus):
    return _get_scan_list_from_filename(fits_hdus)


def generate_observation_id(fits_hdus: fits.HDUList):
    """
    Generates an observation ID the same way the SSTRED pipeline does it when exporting cubes. It will generate a string
    on the form: "2019-04-16T08:20:18.96758_6173_0-36,38,39"

    The first part is the DATE-BEG keyword, the second part is the spectral line and the last part is the list of scans.
    """
    primary_fits_header = fits_hdus[0].header

    date_beg = primary_fits_header['DATE-BEG']
    filter1 = primary_fits_header['FILTER1']
    scannum_list = _get_sparse_scans_list_string(fits_hdus)

    return '%s_%s_%s' % (date_beg.strip(), filter1.strip(), scannum_list)
import datetime

from astropy.io import fits
from django.contrib.auth.models import Group, User
from django.test import TestCase

from data_access.ingesters.ingest_access_control_entities import ingest_access_control_entities
from data_access.models import DataCubeGroupGrant, DataCubeUserGrant
from data_access.utils import data_cube_requires_access_grant, user_has_access_to_data_cube
from observations.models import Instrument, DataCube


def get_datetime(year, month, day):
    return datetime.datetime(year, month, day, tzinfo=datetime.timezone.utc)


TEST_FITS_HEADER = """SIMPLE  =                    T / Written by IDL:  Sat Mar 20 11:00:01 2021      BITPIX  =                  -32 /                                                NAXIS   =                    5 / Number of data axes                            NAXIS1  =                 1173 / Number of positions along axis 1               NAXIS2  =                 1157 / Number of positions along axis 2               NAXIS3  =                   14 / Number of positions along axis 3               NAXIS4  =                    4 / Number of positions along axis 4               NAXIS5  =                    5 / Number of positions along axis 5               EXTEND  =                    T / The file has extension(s).                     DATEREF = '2019-04-19T00:00:00.000000' / Reference time in ISO-8601             PRSTEP1 = 'MOMFBD  '           / Processing step name                           PRPARA1 = '{"WAVELENGTH":"6.17300e-07","MODES":"2-6,9,10,7,8,14,15,11-13,20,21&'CONTINUE  ',18,19,16,17,27,28,25,26,22-24,35,36,33,34,44,45,31,32,29,30,54,55,&'CONTINUE  '42,43,40,41,37-39,65,66,52,53,50","BASIS":"Karhunen-Loeve","NEW_CON&'CONTINUE  'STRAINTS":"","FPMETHOD":"horint","SIM_X":[61,109,157,206,254,303,35&'CONTINUE  '1,400,448,497,545,593,642,690,739,787,836,884,933],"ARCSECPERPIX":"&'CONTINUE  '0.0592","GETSTEP":"getstep_conjugate_gradient","MAX_LOCAL_SHIFT":"3&'CONTINUE  '0","FAST_QR":"","FILE_TYPE":"MOMFBD","SIM_Y":[62,111,161,211,260,31&'CONTINUE  '0,360,410,459,509,559,608,658,708,758,807,857,907,957],"TRACE":"","&'CONTINUE  'TELESCOPE_D":"0.97","GET_PSF":"","OUTPUT_FILE":"results/camXX_2019-&'CONTINUE  '04-19T17:34:39_00004_6173","DATE_OBS":"2019-04-19","NUM_POINTS":"88&'CONTINUE  '","GET_PSF_AVG":"","IMAGE_NUMS":"7140:2:7170,7176:2:7206,7212:2:724&'CONTINUE  '2,7248:2:7278,7284:2:7314,7320:2:7350,7356:2:7386,7392:2:7422,7428:&'CONTINUE  '2:7458,7464:2:7494,7500:2:7530,7536:2:7566,7572:2:7602,7608:2:7638"&'CONTINUE  ',"PIXELSIZE":"1.60000e-05","GRADIENT":"gradient_diff"}&' / List of   CONTINUE  '' / parameters/options for PRPROC1                                   CADAVG  =              21.9216 / Average of actual cadence                      CADMIN  =              21.9216 / Minimum of actual cadence                      CADMAX  =              21.9216 / Maximum of actual cadence                      CADVAR  =          6.86365E-10 / Variance of actual cadence                     DATE-OBS= '2019-04-19T17:34:39' /  Data set timestamp                                                                                                           LONGSTRN= 'OGIP 1.0'           / The OGIP long string convention may be used.   INSTRUME= 'CRISP   '           /  Name of instrument                            TELCONFG= 'Schupmann, imaging' /  Telescope configuration                       OBSGEO-Z=              3051730 /  [m] SST location                              OBSGEO-Y=             -1718726 /  [m] SST location                              OBSGEO-X=              5327403 /  [m] SST location                              AO_NMODE=                   84 /  Number of AO corrected Mirror modes           OBSRVTRY= 'Observatorio del Roque de los Muchachos (ORM)' /  Name of observatoryTELESCOP= 'Swedish 1-meter Solar Telescope (SST)' /  Name of telescope          OBJECT  = 'Sun     '           /                                                STARTOBS= '2019-04-19T17:34:39' /                                               FILLED  =                    1 /  Missing pixels have been filled.              PC1_1   =              1.00000 / No rotations                                   PC2_2   =              1.00000 / No rotations                                   PC3_3   =              1.00000 / No rotations                                   PC4_4   =              1.00000 / No rotations                                   PC5_5   =              1.00000 / No rotations                                   CTYPE1  = 'HPLN-TAB'           / Helioprojective longitude                      CUNIT1  = 'arcsec  '           / Unit along axis 1                              CNAME1  = 'Spatial X'          /                                                PS1_0   = 'WCS-TAB '           / EXTNAME; EXTVER=EXTLEVEL=1 is default          PS1_1   = 'HPLN+HPLT+WAVE+TIME' / TTYPE for column w/coordinates                PS1_2   = 'HPLN-INDEX'         / TTYPE for INDEX                                PV1_3   =                    1 / Coord. 1 tabulated coordinate number           CRPIX1  =                    0 / Unity transform                                CRVAL1  =                    0 / Unity transform                                CDELT1  =                    1 / Unity transform                                CSYER1  =              60.0000 / [arcsec] Orientation known                     CTYPE2  = 'HPLT-TAB'           / Helioprojective latitude                       CUNIT2  = 'arcsec  '           / Unit along axis 2                              CNAME2  = 'Spatial Y'          /                                                PS2_0   = 'WCS-TAB '           / EXTNAME; EXTVER=EXTLEVEL=1 is default          PS2_1   = 'HPLN+HPLT+WAVE+TIME' / TTYPE for column w/coordinates                PS2_2   = 'HPLT-INDEX'         / TTYPE for INDEX                                PV2_3   =                    2 / Coord. 2 tabulated coordinate number           CRPIX2  =                    0 / Unity transform                                CRVAL2  =                    0 / Unity transform                                CDELT2  =                    1 / Unity transform                                CSYER2  =              60.0000 / [arcsec] Orientation known                     CTYPE3  = 'WAVE-TAB'           / Wavelength, function of tuning and scan number CNAME3  = 'Wavelength'         /                                                CUNIT3  = 'nm      '           / Wavelength unit, tabulated for dim. 3 and 5    PS3_0   = 'WCS-TAB '           / EXTNAME; EXTVER=EXTLEVEL=1 is default          PS3_1   = 'HPLN+HPLT+WAVE+TIME' / TTYPE for column w/coordinates                PV3_3   =                    3 / Coord. 3 tabulated coordinate number           CRPIX3  =                    0 / Unity transform                                CRVAL3  =                    0 / Unity transform                                CDELT3  =                    1 / Unity transform                                CWERR3  =           0.00795488 / [nm] Max total distortion                      CWDIS3  = 'Lookup  '           / WAVE distortions in lookup table               DW3     = 'EXTVER: 1'          / Extension version number                       DW3     = 'NAXES: 5'           / Number of axes in the extension                DW3     = 'AXIS.1: 1'          / Spatial X                                      DW3     = 'AXIS.2: 2'          / Spatial Y                                      DW3     = 'AXIS.3: 3'          / Tuning                                         DW3     = 'AXIS.4: 4'          / Stokes                                         DW3     = 'AXIS.5: 5'          / Scan number                                    DW3     = 'CWERR: 0.00795488'  / [nm] Max distortion (this correction step)     DW3     = 'CWDIS: 1'           / Distortions in lookup table                    DW3     = 'ASSOCIATE: 1'       / Association stage (pixel coordinates)          DW3     = 'APPLY: 6'           / Application stage (world coordinates)          CTYPE4  = 'STOKES  '           / Stokes vector [I,Q,U,V]                        CRPIX4  =                    1 / Index of Stokes components in pixel 1          CRVAL4  =                    1 / The first Stokes index is 1                    CDELT4  =                    1 / Stokes indices [1,2,3,4] --> [I,Q,U,V]         CTYPE5  = 'UTC--TAB'           / Time, function of tuning and scan number       CNAME5  = 'Time since DATEREF, increases with dim. 3 and 5' /                   CUNIT5  = 's       '           /                                                PS5_0   = 'WCS-TAB '           / EXTNAME; EXTVER=EXTLEVEL=1 is default          PS5_1   = 'HPLN+HPLT+WAVE+TIME' / TTYPE for column w/coordinates                PV5_3   =                    4 / Coord. 5 tabulated coordinate number           CRPIX5  =                    0 / Unity transform                                CRVAL5  =                    0 / Unity transform                                CDELT5  =                    1 / Unity transform                                OBS_HDU =                    1 /                                                BUNIT   = 'W m^-2 Hz^-1 sr^-1' / Units in array                                 BTYPE   = 'Intensity'          / Type of data in array                          FILTER1 = '6173    '           / Inferred from filename.                        WAVELNTH=              617.380 / [nm] Prefilter peak wavelength                 WAVEMIN =              617.155 / [nm] Prefilter min wavelength (0.5 peak)       WAVEMAX =              617.605 / [nm] Prefilter max wavelength (0.5 peak)       WAVEBAND= 'Fe I 6173'          /                                                WAVEUNIT=                   -9 / WAVELNTH in units 10^WAVEUNIT m = nm           PRLIB1  = 'momfbd/redux'       / Additional software library                    PRVER1  = '20201208.18'        / Library version/MJD of last update (From .momfbPRREF1  = 'DATE: 2020-12-30T13:15:42' / When this step was performed            PRBRA1  = 'master  '           / Version control branch                         PRSTEP2 = 'DEMODULATION'       / Processing step name                           PRPROC2 = 'crisp::demodulate'  / Name of procedure used                         PRPARA2 = '{"NBRFAC":3.701677895171844e-11,"NBTFAC":3.512923263566968e-11,"SMO&'CONTINUE  'OTH_BY_KERNEL":5,"SMOOTH_BY_SUBFIELD":0,"TILES":[8,16,32,64,128],"C&'CONTINUE  'LIPS":[8,4,2,1,1]}' / List of parameters/options for PRPROC2         PRLIB2  = 'reduxdlm'           / Additional software library                    PRVER2  = '1.0.18-13'          / Library version/MJD of last update             PRREF2  = 'DATE: 2021-05-26T19:18:00' / When this step was performed            PRBRA2  = 'master  '           / Version control branch                         PRSTEP3 = 'CONCATENATION'      / Processing step name                           PRPROC3 = 'crisp::make_nb_cube' / Name of procedure used                        PRPARA3 = '{"NOCROSSTALK":1,"REDEMODULATE":1,"WCFILE":"cubes_wb/wb_6173_2019-0&'CONTINUE  '4-19T17:34:39_scans=0-4_corrected_im.fits","INTENSITYCORRMETHOD":"o&'CONTINUE  'ld","NOMISSING_NANS":1}' / List of parameters/options for PRPROC3    PRREF3A = 'DATE: 2021-05-26T20:04:16' / When this step was performed            PRLIB3  = 'SSTRED  '           / Software library containing crisp::make_nb_cubePRVER3  = '1.1.0-632'          / Library version/MJD of last update             PRLIB3A = 'IDLAstro'           / Additional software library                    PRVER3A = '392     '           / Library version/MJD of last update             PRLIB3B = 'Coyote  '           / Additional software library                    PRVER3B = '1154    '           / Library version/MJD of last update             PRLIB3C = 'mpfit   '           / Additional software library                    PRVER3C = '2017-01-03'         / Library version/MJD of last update             PRLIB3D = 'reduxdlm'           / Additional software library                    PRVER3D = '1.0.18-13'          / Library version/MJD of last update             PRBRA3  = 'master  '           / Version control branch                         PRSTEP4 = 'CALIBRATION-INTENSITY-SPECTRAL' / Processing step name               PRPROC4 = 'crisp::make_nb_cube' / Name of procedure used                        PRPARA4 = '{"NOCROSSTALK":1,"REDEMODULATE":1,"WCFILE":"cubes_wb/wb_6173_2019-0&'CONTINUE  '4-19T17:34:39_scans=0-4_corrected_im.fits","INTENSITYCORRMETHOD":"o&'CONTINUE  'ld","NOMISSING_NANS":1}' / List of parameters/options for PRPROC4    PRREF4  = 'Hamburg FTS spectral atlas (Neckel 1999)' /                          PRREF4A = 'Calibration data from 11:29:43' /                                    PRREF4B = 'DATE: 2021-05-26T20:04:16' / When this step was performed            PRLIB4  = 'SSTRED  '           / Software library containing crisp::make_nb_cubePRVER4  = '1.1.0-632'          / Library version/MJD of last update             PRLIB4A = 'IDLAstro'           / Additional software library                    PRVER4A = '392     '           / Library version/MJD of last update             PRLIB4B = 'Coyote  '           / Additional software library                    PRVER4B = '1154    '           / Library version/MJD of last update             PRLIB4C = 'mpfit   '           / Additional software library                    PRVER4C = '2017-01-03'         / Library version/MJD of last update             PRLIB4D = 'reduxdlm'           / Additional software library                    PRVER4D = '1.0.18-13'          / Library version/MJD of last update             PRBRA4  = 'master  '           / Version control branch                         PRSTEP5 = 'CALIBRATION-INTENSITY-TEMPORAL' / Processing step name               PRPROC5 = 'red::fitscube_intensitycorr' / Name of procedure used                PRMODE5 = 'LOCAL   '           / Processing mode                                PRPARA5 = '{"FILENAME":"/scratch/olexa/2019-04-19/CRISP//cubes_nb/nb_6173_2019&'CONTINUE  '-04-19T17:34:39_scans=0-4_stokes_corrected_im.fits"}&' / List of     CONTINUE  '' / parameters/options for PRPROC5                                   PRREF5  = 'Mean DC WB median intensity in counts from prefilter fit data : 708&'CONTINUE  '.43523' /                                                            PRREF5A = 'DATE: 2021-05-26T20:06:18' / When this step was performed            PRLIB5  = 'SSTRED  '           / Software library containing red::fitscube_intenPRVER5  = '1.1.0-632'          / Library version/MJD of last update             PRLIB5A = 'IDLAstro'           / Additional software library                    PRVER5A = '392     '           / Library version/MJD of last update             PRLIB5B = 'Coyote  '           / Additional software library                    PRVER5B = '1154    '           / Library version/MJD of last update             PRLIB5C = 'mpfit   '           / Additional software library                    PRVER5C = '2017-01-03'         / Library version/MJD of last update             PRLIB5D = 'reduxdlm'           / Additional software library                    PRVER5D = '1.0.18-13'          / Library version/MJD of last update             PRBRA5  = 'master  '           / Version control branch                         PRSTEP6 = 'STOKES-CROSSTALK-CORRECTION' / Processing step name                  PRPROC6 = 'red::fitscube_crosstalk' / Name of procedure used                    PRPARA6 = '{"MARGIN":50,"TUNING_SELECTION":[0]}&'                               CONTINUE  '' / List of parameters/options for PRPROC6                           PRREF6  = 'DATE: 2021-05-26T21:27:31' / When this step was performed            PRLIB6  = 'SSTRED  '           / Software library containing red::fitscube_crossPRVER6  = '1.1.0-632'          / Library version/MJD of last update             PRLIB6A = 'IDLAstro'           / Additional software library                    PRVER6A = '392     '           / Library version/MJD of last update             PRLIB6B = 'Coyote  '           / Additional software library                    PRVER6B = '1154    '           / Library version/MJD of last update             PRLIB6C = 'mpfit   '           / Additional software library                    PRVER6C = '2017-01-03'         / Library version/MJD of last update             PRLIB6D = 'reduxdlm'           / Additional software library                    PRVER6D = '1.0.18-13'          / Library version/MJD of last update             PRBRA6  = 'master  '           / Version control branch                         PRSTEP7 = 'HEADER-CORRECTION'  / Processing step name                           PRPROC7 = 'red::fitscube_finalize' / Name of procedure used                     PRPARA7 = '{"KEYWORDS":{"OBSERVER":"Nazaret Bello Gonzales, Philip Lindner"}}&' CONTINUE  '' / List of parameters/options for PRPROC7                           PRREF7  = 'DATE: 2021-05-28T15:39:52' / When this step was performed            PRLIB7  = 'SSTRED  '           / Software library containing red::fitscube_finalPRVER7  = '1.1.0-632'          / Library version/MJD of last update             PRLIB7A = 'IDLAstro'           / Additional software library                    PRVER7A = '392     '           / Library version/MJD of last update             PRLIB7B = 'Coyote  '           / Additional software library                    PRVER7B = '1154    '           / Library version/MJD of last update             PRLIB7C = 'mpfit   '           / Additional software library                    PRVER7C = '2017-01-03'         / Library version/MJD of last update             PRLIB7D = 'reduxdlm'           / Additional software library                    PRVER7D = '1.0.18-13'          / Library version/MJD of last update             PRBRA7  = 'master  '           / Version control branch                         CAMERA  = 'Crisp-T,Crisp-R'    /                                                DETECTOR= 'camXIX,camXXV'      /                                                TIMESYS = 'UTC     '           /                                                DATE    = '2021-05-28T15:08:12' / Creation UTC date of FITS header              FILENAME= 'nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-0&'CONTINUE  '5-28T15:08:12_im.fits' /                                             VAR_KEYS= 'VAR-EXT-DATE-BEG;DATE-BEG,VAR-EXT-DATE-END;DATE-END,VAR-EXT-DATE-AV&'CONTINUE  'G;DATE-AVG,VAR-EXT-RESPAPPL;RESPAPPL,VAR-EXT-SCANNUM;SCANNUM,VAR-EX&'CONTINUE  'T-ATMOS_R0;ATMOS_R0,VAR-EXT-AO_LOCK;AO_LOCK,VAR-EXT-ELEV_ANG;ELEV_A&'CONTINUE  'NG,VAR-EXT-XPOSURE;XPOSURE,VAR-EXT-TEXPOSUR;TEXPOSUR,VAR-EXT-NSUMEX&'CONTINUE  'P;NSUMEXP,VAR-EXT-DATAMAD;DATAMAD,VAR-EXT-DATAKURT;DATAKURT,VAR-EXT&'CONTINUE  '-DATASKEW;DATASKEW,VAR-EXT-DATANRMS;DATANRMS,VAR-EXT-DATAMEAN;DATAM&'CONTINUE  'EAN,VAR-EXT-DATAMAX;DATAMAX,VAR-EXT-DATAMIN;DATAMIN,VAR-EXT-NDATAPI&'CONTINUE  'X;NDATAPIX,VAR-EXT-DATAP01;DATAP01,VAR-EXT-DATAP02;DATAP02,VAR-EXT-&'CONTINUE  'DATAP05;DATAP05,VAR-EXT-DATAP10;DATAP10,VAR-EXT-DATAP25;DATAP25,VAR&'CONTINUE  '-EXT-DATAMEDN;DATAMEDN,VAR-EXT-DATAP75;DATAP75,VAR-EXT-DATAP90;DATA&'CONTINUE  'P90,VAR-EXT-DATAP95;DATAP95,VAR-EXT-DATAP98;DATAP98,VAR-EXT-DATAP99&'CONTINUE  ';DATAP99' / SOLARNET variable-keywords                               SOLARNET=                    1 / SOLARNET compliant file                        OBSERVER= 'Nazaret Bello Gonzales, Philip Lindner' /                            RELEASE = '2020-08-05'         /                                                RELEASEC= 'Data acquired within the SOLARNET Trans-National Access programme w&'CONTINUE  'ith funding from the European Union''s Horizon2020 research and inn&'CONTINUE  'ovation programme under grant agreement no 824135. PI: Philip Lindn&'CONTINUE  'er. See https://dubshen.astro.su.se/wiki/index.php/Science_data.' /  WCSNAMEA= 'AVERAGED APPROXIMATE HPLN-TAN/HPLT-TAN CENTER POINT' /               CRPIX1A =              587.000 / Center pixel of image array                    CRPIX2A =              579.000 / Center pixel of image array                    CRVAL1A =        708.465683121 / [arcsec] Coordinates of center of image array  CRVAL2A =        134.521699788 / [arcsec] Coordinates of center of image array  CDELT1A =              0.00000 / Zero FOV extent                                CDELT2A =              0.00000 / Zero FOV extent                                DATE-BEG= '2019-04-19T17:34:55.50395&'                                          CONTINUE  '' / Beginning time of observation (first value)                      DATE-END= '2019-04-19T17:36:30.03073' / End time of observation (last value)    DATE-AVG= '2019-04-19T17:35:42.76733&'                                          CONTINUE  '' / Average time of observation (provided value)                     RESPAPPL=        36400236941.0 / Mean of applied response function (mean value) SCANNUM =                    0 / Scan number (first value)                      ATMOS_R0=      0.0833495000000 / Atmospheric coherence length (mean value)      AO_LOCK =       0.934098000000 / Fraction of time the AO was locking, 2s averageELEV_ANG=        26.2324000000 / Elevation angle (mean value)                   XPOSURE =       0.277752000000 / Summed exposure times (median value)           TEXPOSUR=      0.0173595000000 / [s] Single-exposure time (median value)        NSUMEXP =        16.0000000000 / Number of summed exposures (median value)      DATAMAD =    1.25612736581E-08 / The mean absolute deviation from the mean (provDATAKURT=      -0.167994702696 / The excess kurtosis of the data (provided valueDATASKEW=        1.29221057381 / The skewness of the data (provided value)      DATANRMS=        1.77306898707 / The normalized RMS deviation from the mean (proDATAMEAN=    8.37219023298E-09 / The average data value (provided value)        DATAMAX =          5.32761E-08 / The maximum data value (provided value)        DATAMIN =         -1.42056E-08 / The minimum data value (provided value)        NDATAPIX=            251768440 / Number of pixels (provided value)              DATAP01 =   -3.03432385815E-10 / The 01 percentile of the data (provided value) DATAP02 =   -1.94000020633E-10 / The 02 percentile of the data (provided value) DATAP05 =   -1.26785738363E-10 / The 05 percentile of the data (provided value) DATAP10 =   -8.76650255645E-11 / The 10 percentile of the data (provided value) DATAP25 =   -3.26868712784E-11 / The 25 percentile of the data (provided value) DATAMEDN=    3.11521557292E-11 / The 50 percentile of the data (provided value) DATAP75 =    5.12399989105E-09 / The 75 percentile of the data (provided value) DATAP90 =    3.67140713821E-08 / The 90 percentile of the data (provided value) DATAP95 =    3.88390493654E-08 / The 95 percentile of the data (provided value) DATAP98 =    4.06226014885E-08 / The 98 percentile of the data (provided value) DATAP99 =    4.17349560774E-08 / The 99 percentile of the data (provided value) DATASUM = '3747977843'         / data unit checksum updated 2021-05-28T15:09:27 CHECKSUM= 'jH7AjH61jH68jH68'   / HDU checksum updated 2021-05-28T15:09:27       PRREF3  = 'Align reference: wb_6173_2019-04-19T17:34:39_scans=0-4_corrected_ex&'CONTINUE  'port2021-05-28T15:08:12_im.fits' / WB cube file name                 COMMENT This FITS file may contain long string keyword values that are          COMMENT continued over multiple keywords. This convention uses the '&'          COMMENT character at the end of a string which is then continued on             COMMENT subsequent keywords whose name = 'CONTINUE'.                                                                                                                                                                                            COMMENT FITS (Flexible Image Transport System) format is defined in 'Astronomy  COMMENT and Astrophysics', volume 376, page 359; bibcode 2001A&A...376..359H    END                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             """

EXPECTED_RELEASE_COMMENT = "Data acquired within the SOLARNET Trans-National Access programme with funding from the " \
                           "European Union's Horizon2020 research and innovation programme under grant agreement no " \
                           "824135. PI: Philip Lindner. See https://dubshen.astro.su.se/wiki/index.php/Science_data."

EXPECTED_RELEASE_DATE = datetime.date(2020, 8, 5)


class TestIngestAndCheck(TestCase):
    def setUp(self):
        self.maxDiff = None
        Instrument.objects.bulk_create(
            [Instrument(name='CHROMIS', description=''), Instrument(name='CRISP', description='')])
        self.data_cube = DataCube.objects.create(oid='test_oid', filename='test_file.fits', path='/path/to/test_file.fits',
                                size=1000000000, instrument=Instrument.objects.get(name='CHROMIS'))
        self.swedish_group = Group.objects.create(name='Swedish')

        self.swedish_test_user = User.objects.create(username='swedish_test_user')
        self.test_user = User.objects.create(username='test_user')

        self.swedish_group.user_set.add(self.swedish_test_user)
        self.swedish_group.save()

    def test_ingest_data_cube(self):
        data_cube = self.data_cube

        primary_fits_header = fits.Header.fromstring(TEST_FITS_HEADER)
        ingest_access_control_entities(data_cube, primary_fits_header)

        self.assertIsNotNone(data_cube.access_control)
        self.assertEqual(data_cube.access_control.release_date, EXPECTED_RELEASE_DATE)
        self.assertEqual(data_cube.access_control.release_comment, EXPECTED_RELEASE_COMMENT)

    def test_requires_access_grant(self):
        data_cube = self.data_cube

        primary_fits_header = fits.Header.fromstring(TEST_FITS_HEADER)
        ingest_access_control_entities(data_cube, primary_fits_header)

        self.assertTrue(data_cube_requires_access_grant(data_cube, get_datetime(2019, 1, 1)))
        self.assertTrue(data_cube_requires_access_grant(data_cube, get_datetime(2020, 8, 4)))

        self.assertFalse(data_cube_requires_access_grant(data_cube, get_datetime(2020, 8, 5)))
        self.assertFalse(data_cube_requires_access_grant(data_cube, get_datetime(2020, 8, 10)))
        self.assertFalse(data_cube_requires_access_grant(data_cube, get_datetime(2021, 12, 12)))

    def test_group_access_grants(self):
        data_cube = self.data_cube

        primary_fits_header = fits.Header.fromstring(TEST_FITS_HEADER)
        ingest_access_control_entities(data_cube, primary_fits_header)

        grant = DataCubeGroupGrant.objects.create(group=self.swedish_group, data_cube=data_cube)

        self.assertTrue(user_has_access_to_data_cube(self.swedish_test_user, data_cube, datetime_now=get_datetime(2019, 1, 1)))
        self.assertFalse(user_has_access_to_data_cube(self.test_user, data_cube, datetime_now=get_datetime(2019, 1, 1)))

        self.assertTrue(user_has_access_to_data_cube(self.test_user, data_cube, datetime_now=get_datetime(2022, 1, 1)))
        self.assertTrue(
            user_has_access_to_data_cube(self.swedish_test_user, data_cube, datetime_now=get_datetime(2022, 1, 1)))

    def test_user_access_grants(self):
        data_cube = self.data_cube

        primary_fits_header = fits.Header.fromstring(TEST_FITS_HEADER)
        ingest_access_control_entities(data_cube, primary_fits_header)

        grant = DataCubeUserGrant.objects.create(user=self.test_user, data_cube=data_cube)

        self.assertTrue(user_has_access_to_data_cube(self.test_user, data_cube, datetime_now=get_datetime(2019, 1, 1)))
        self.assertFalse(user_has_access_to_data_cube(self.swedish_test_user, data_cube, datetime_now=get_datetime(2019, 1, 1)))

        self.assertTrue(user_has_access_to_data_cube(self.test_user, data_cube, datetime_now=get_datetime(2022, 1, 1)))
        self.assertTrue(user_has_access_to_data_cube(self.swedish_test_user, data_cube, datetime_now=get_datetime(2022, 1, 1)))

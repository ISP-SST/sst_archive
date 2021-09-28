from django.db import models


class CombinedMetadataManager(models.Manager):
    """Manager that optimize the queries by selecting the foreign objects"""

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('data_location')
        return queryset


class CombinedMetadata(models.Model):
    """Model for the joint set of metadata present in CRISP and CHROMIS"""

    class Meta:
        verbose_name = 'Combined Metadata'
        verbose_name_plural = 'Combined Metadata'
        ordering = ['date_beg']

    oid = models.CharField('Observation ID',
                           help_text='Unique identification string for the observation metadata, usually in the form '
                                     'YYYYMMDDHHMMSS; cannot be modified once it is set',
                           unique=True, db_index=True, max_length=191)
    data_location = models.OneToOneField('dataset.DataLocation', related_name='metadata', null=True,
                                      blank=True, on_delete=models.SET_NULL)
    fits_header = models.TextField(null=True, blank=True)
    date_beg = models.DateTimeField('DATE-BEG', help_text='Start time of the observation [UTC]', blank=True, null=True,
                                    db_index=True)
    date_end = models.DateTimeField('DATE-END', help_text='End time of the observation [UTC]', blank=True, null=True,
                                    db_index=True)
    wavemin = models.FloatField('WAVEMIN', help_text='Min value of the observation spectral range [nm]', blank=True,
                                null=True, db_index=True)
    wavemax = models.FloatField('WAVEMAX', help_text='Max value of the observation spectral range [nm]', blank=True,
                                null=True, db_index=True)

    ao_lock = models.FloatField(verbose_name='AO_LOCK', help_text='Fraction of time the AO was locking, 2s average',
                                blank=True, null=True)
    ao_nmode = models.BigIntegerField(verbose_name='AO_NMODE', help_text='Number of AO corrected Mirror modes',
                                      blank=True, null=True)
    atmos_r0 = models.FloatField(verbose_name='ATMOS_R0', help_text='Atmospheric coherence length (mean value)',
                                 blank=True, null=True)
    btype = models.TextField(verbose_name='BTYPE', help_text='Type of data in array', blank=True, null=True)
    bunit = models.TextField(verbose_name='BUNIT', help_text='Units in array', blank=True, null=True)
    cadavg = models.FloatField(verbose_name='CADAVG', help_text='Average of actual cadence', blank=True, null=True)
    cadmax = models.FloatField(verbose_name='CADMAX', help_text='Maximum of actual cadence', blank=True, null=True)
    cadmin = models.FloatField(verbose_name='CADMIN', help_text='Minimum of actual cadence', blank=True, null=True)
    cadvar = models.FloatField(verbose_name='CADVAR', help_text='Variance of actual cadence', blank=True, null=True)
    camera = models.TextField(verbose_name='CAMERA', help_text='', blank=True, null=True)
    cdelt1 = models.BigIntegerField(verbose_name='CDELT1', help_text='Unity transform', blank=True, null=True)
    cdelt1a = models.FloatField(verbose_name='CDELT1A', help_text='Zero FOV extent', blank=True, null=True)
    cdelt2 = models.BigIntegerField(verbose_name='CDELT2', help_text='Unity transform', blank=True, null=True)
    cdelt2a = models.FloatField(verbose_name='CDELT2A', help_text='Zero FOV extent', blank=True, null=True)
    cdelt3 = models.BigIntegerField(verbose_name='CDELT3', help_text='Unity transform', blank=True, null=True)
    cdelt4 = models.BigIntegerField(verbose_name='CDELT4', help_text='Stokes indices [1,2,3,4] --> [I,Q,U,V]',
                                    blank=True, null=True)
    cdelt5 = models.BigIntegerField(verbose_name='CDELT5', help_text='Unity transform', blank=True, null=True)
    cname1 = models.TextField(verbose_name='CNAME1', help_text='', blank=True, null=True)
    cname2 = models.TextField(verbose_name='CNAME2', help_text='', blank=True, null=True)
    cname3 = models.TextField(verbose_name='CNAME3', help_text='', blank=True, null=True)
    cname5 = models.TextField(verbose_name='CNAME5', help_text='', blank=True, null=True)
    crpix1 = models.BigIntegerField(verbose_name='CRPIX1', help_text='Unity transform', blank=True, null=True)
    crpix1a = models.FloatField(verbose_name='CRPIX1A', help_text='Center pixel of image array', blank=True, null=True)
    crpix2 = models.BigIntegerField(verbose_name='CRPIX2', help_text='Unity transform', blank=True, null=True)
    crpix2a = models.FloatField(verbose_name='CRPIX2A', help_text='Center pixel of image array', blank=True, null=True)
    crpix3 = models.BigIntegerField(verbose_name='CRPIX3', help_text='Unity transform', blank=True, null=True)
    crpix4 = models.BigIntegerField(verbose_name='CRPIX4', help_text='Index of Stokes components in pixel 1',
                                    blank=True, null=True)
    crpix5 = models.BigIntegerField(verbose_name='CRPIX5', help_text='Unity transform', blank=True, null=True)
    crval1 = models.BigIntegerField(verbose_name='CRVAL1', help_text='Unity transform', blank=True, null=True)
    crval1a = models.FloatField(verbose_name='CRVAL1A', help_text='Coordinates of center of image array', blank=True,
                                null=True)
    crval2 = models.BigIntegerField(verbose_name='CRVAL2', help_text='Unity transform', blank=True, null=True)
    crval2a = models.FloatField(verbose_name='CRVAL2A', help_text='Coordinates of center of image array', blank=True,
                                null=True)
    crval3 = models.BigIntegerField(verbose_name='CRVAL3', help_text='Unity transform', blank=True, null=True)
    crval4 = models.BigIntegerField(verbose_name='CRVAL4', help_text='The first Stokes index is 1', blank=True,
                                    null=True)
    crval5 = models.BigIntegerField(verbose_name='CRVAL5', help_text='Unity transform', blank=True, null=True)
    csyer1 = models.BigIntegerField(verbose_name='CSYER1', help_text='Orientation unknown', blank=True, null=True)
    csyer2 = models.BigIntegerField(verbose_name='CSYER2', help_text='Orientation unknown', blank=True, null=True)
    ctype1 = models.TextField(verbose_name='CTYPE1', help_text='SOLAR X', blank=True, null=True)
    ctype2 = models.TextField(verbose_name='CTYPE2', help_text='SOLAR Y', blank=True, null=True)
    ctype3 = models.TextField(verbose_name='CTYPE3', help_text='Wavelength, function of tuning and scan number',
                              blank=True, null=True)
    ctype4 = models.TextField(verbose_name='CTYPE4', help_text='Stokes vector [I,Q,U,V]', blank=True, null=True)
    ctype5 = models.TextField(verbose_name='CTYPE5', help_text='Time, function of tuning and scan number', blank=True,
                              null=True)
    cunit1 = models.TextField(verbose_name='CUNIT1', help_text='Unit along axis 1', blank=True, null=True)
    cunit2 = models.TextField(verbose_name='CUNIT2', help_text='Unit along axis 2', blank=True, null=True)
    cunit3 = models.TextField(verbose_name='CUNIT3', help_text='Wavelength unit, tabulated for dim. 3 and 5',
                              blank=True, null=True)
    cunit5 = models.TextField(verbose_name='CUNIT5', help_text='', blank=True, null=True)
    cwdis3 = models.TextField(verbose_name='CWDIS3', help_text='WAVE distortions in lookup table', blank=True,
                              null=True)
    cwerr3 = models.FloatField(verbose_name='CWERR3', help_text='Max total distortion', blank=True, null=True)
    datakurt = models.FloatField(verbose_name='DATAKURT', help_text='The excess kurtosis of the data (provided value',
                                 blank=True, null=True)
    datamax = models.FloatField(verbose_name='DATAMAX', help_text='The maximum data value (provided value)', blank=True,
                                null=True)
    datamean = models.FloatField(verbose_name='DATAMEAN', help_text='The average data value (provided value)',
                                 blank=True, null=True)
    datamedn = models.FloatField(verbose_name='DATAMEDN', help_text='The 50 percentile of the data (provided value)',
                                 blank=True, null=True)
    datamin = models.FloatField(verbose_name='DATAMIN', help_text='The minimum data value (provided value)', blank=True,
                                null=True)
    datap01 = models.FloatField(verbose_name='DATAP01', help_text='The 01 percentile of the data (provided value)',
                                blank=True, null=True)
    datap10 = models.FloatField(verbose_name='DATAP10', help_text='The 10 percentile of the data (provided value)',
                                blank=True, null=True)
    datap25 = models.FloatField(verbose_name='DATAP25', help_text='The 25 percentile of the data (provided value)',
                                blank=True, null=True)
    datap75 = models.FloatField(verbose_name='DATAP75', help_text='The 75 percentile of the data (provided value)',
                                blank=True, null=True)
    datap90 = models.FloatField(verbose_name='DATAP90', help_text='The 90 percentile of the data (provided value)',
                                blank=True, null=True)
    datap95 = models.FloatField(verbose_name='DATAP95', help_text='The 95 percentile of the data (provided value)',
                                blank=True, null=True)
    datap98 = models.FloatField(verbose_name='DATAP98', help_text='The 98 percentile of the data (provided value)',
                                blank=True, null=True)
    datap99 = models.FloatField(verbose_name='DATAP99', help_text='The 99 percentile of the data (provided value)',
                                blank=True, null=True)
    datarms = models.FloatField(verbose_name='DATARMS', help_text='The RMS deviation from the mean (provided value',
                                blank=True, null=True)
    dataskew = models.FloatField(verbose_name='DATASKEW', help_text='The skewness of the data (provided value)',
                                 blank=True, null=True)
    date = models.TextField(verbose_name='DATE', help_text='Creation UTC date of FITS header', blank=True, null=True)
    date_avg = models.DateTimeField(verbose_name='DATE-AVG', help_text='Average time of observation (provided va',
                                    blank=True, null=True)
    date_obs = models.DateTimeField(verbose_name='DATE-OBS', help_text='Inferred from directory.', blank=True,
                                    null=True)
    dateref = models.TextField(verbose_name='DATEREF', help_text='Reference time in ISO-8601', blank=True, null=True)
    detector = models.TextField(verbose_name='DETECTOR', help_text='', blank=True, null=True)
    dw3_apply = models.FloatField(verbose_name='DW3.APPLY', help_text='Application stage (world coordinates)',
                                  blank=True, null=True)
    dw3_associate = models.FloatField(verbose_name='DW3.ASSOCIATE', help_text='Association stage (pixel coordinates)',
                                      blank=True, null=True)
    dw3_axis1 = models.BigIntegerField(verbose_name='DW3 AXIS1', help_text='Spatial X', blank=True, null=True)
    dw3_axis2 = models.BigIntegerField(verbose_name='DW3 AXIS2', help_text='Spatial Y', blank=True, null=True)
    dw3_axis3 = models.BigIntegerField(verbose_name='DW3 AXIS3', help_text='Scan number', blank=True, null=True)
    dw3_axis_1 = models.FloatField(verbose_name='DW3.AXIS.1', help_text='Spatial X', blank=True, null=True)
    dw3_axis_2 = models.FloatField(verbose_name='DW3.AXIS.2', help_text='Spatial Y', blank=True, null=True)
    dw3_axis_3 = models.FloatField(verbose_name='DW3.AXIS.3', help_text='Scan number', blank=True, null=True)
    dw3_cwdis_lookup = models.FloatField(verbose_name='DW3.CWDIS.LOOKUP', help_text='Distortions in lookup table',
                                         blank=True, null=True)
    dw3_cwerr = models.FloatField(verbose_name='DW3 CWERR', help_text='Max distortion (this correction step)',
                                  blank=True, null=True)
    dw3_extver = models.FloatField(verbose_name='DW3.EXTVER', help_text='Extension version number', blank=True,
                                   null=True)
    dw3_name = models.TextField(verbose_name='DW3 NAME', help_text='Type of correction', blank=True, null=True)
    dw3_naxes = models.BigIntegerField(verbose_name='DW3 NAXES', help_text='3 axes in the lookup table', blank=True,
                                       null=True)
    elev_ang = models.FloatField(verbose_name='ELEV_ANG', help_text='Elevation angle (mean value)', blank=True,
                                 null=True)
    filename = models.TextField(verbose_name='FILENAME', help_text='', blank=True, null=True)
    filled = models.BigIntegerField(verbose_name='FILLED', help_text='Missing pixels have been filled.', blank=True,
                                    null=True)
    filter1 = models.TextField(verbose_name='FILTER1', help_text='Inferred from filename.', blank=True, null=True)
    fnumsum = models.TextField(verbose_name='FNUMSUM', help_text='List of frame numbers in the sum', blank=True,
                               null=True)
    instrume = models.TextField(verbose_name='INSTRUME', help_text='Name of instrument', blank=True, null=True)
    longstrn = models.TextField(verbose_name='LONGSTRN', help_text='The OGIP long string convention may be used.',
                                blank=True, null=True)
    naxis = models.BigIntegerField(verbose_name='NAXIS', help_text='Number of data axes', blank=True, null=True)
    naxis1 = models.BigIntegerField(verbose_name='NAXIS1', help_text='Number of positions along axis 1', blank=True,
                                    null=True)
    naxis2 = models.BigIntegerField(verbose_name='NAXIS2', help_text='Number of positions along axis 2', blank=True,
                                    null=True)
    naxis3 = models.BigIntegerField(verbose_name='NAXIS3', help_text='Number of positions along axis 3', blank=True,
                                    null=True)
    naxis4 = models.BigIntegerField(verbose_name='NAXIS4', help_text='Number of positions along axis 4', blank=True,
                                    null=True)
    naxis5 = models.BigIntegerField(verbose_name='NAXIS5', help_text='Number of positions along axis 5', blank=True,
                                    null=True)
    npixels = models.BigIntegerField(verbose_name='NPIXELS', help_text='Number of pixels (provided value)', blank=True,
                                     null=True)
    nsumexp = models.FloatField(verbose_name='NSUMEXP', help_text='Number of summed exposures (median value)',
                                blank=True, null=True)
    object = models.TextField(verbose_name='OBJECT', help_text='', blank=True, null=True)
    obs_hdu = models.BigIntegerField(verbose_name='OBS_HDU', help_text='', blank=True, null=True)
    observer = models.TextField(verbose_name='OBSERVER', help_text='', blank=True, null=True)
    obsgeo_x = models.BigIntegerField(verbose_name='OBSGEO-X', help_text='SST location', blank=True, null=True)
    obsgeo_y = models.BigIntegerField(verbose_name='OBSGEO-Y', help_text='SST location', blank=True, null=True)
    obsgeo_z = models.BigIntegerField(verbose_name='OBSGEO-Z', help_text='SST location', blank=True, null=True)
    obsrvtry = models.TextField(verbose_name='OBSRVTRY', help_text='Name of observatory', blank=True, null=True)
    pc1_1 = models.FloatField(verbose_name='PC1_1', help_text='No rotations', blank=True, null=True)
    pc2_2 = models.FloatField(verbose_name='PC2_2', help_text='No rotations', blank=True, null=True)
    pc3_3 = models.FloatField(verbose_name='PC3_3', help_text='No rotations', blank=True, null=True)
    pc4_4 = models.FloatField(verbose_name='PC4_4', help_text='No rotations', blank=True, null=True)
    pc5_5 = models.FloatField(verbose_name='PC5_5', help_text='No rotations', blank=True, null=True)
    prbra1 = models.TextField(verbose_name='PRBRA1', help_text='Version control branch', blank=True, null=True)
    prbra2 = models.TextField(verbose_name='PRBRA2', help_text='Version control branch', blank=True, null=True)
    prbra3 = models.TextField(verbose_name='PRBRA3', help_text='Version control branch', blank=True, null=True)
    prbra4 = models.TextField(verbose_name='PRBRA4', help_text='Version control branch', blank=True, null=True)
    prbra5 = models.TextField(verbose_name='PRBRA5', help_text='Version control branch', blank=True, null=True)
    prbra6 = models.TextField(verbose_name='PRBRA6', help_text='Version control branch', blank=True, null=True)
    prlib1 = models.TextField(verbose_name='PRLIB1', help_text='Software library', blank=True, null=True)
    prlib1a = models.TextField(verbose_name='PRLIB1A', help_text='Additional software library', blank=True, null=True)
    prlib1b = models.TextField(verbose_name='PRLIB1B', help_text='Additional software library', blank=True, null=True)
    prlib1c = models.TextField(verbose_name='PRLIB1C', help_text='Additional software library', blank=True, null=True)
    prlib1d = models.TextField(verbose_name='PRLIB1D', help_text='Additional software library', blank=True, null=True)
    prlib1e = models.TextField(verbose_name='PRLIB1E', help_text='Additional software library', blank=True, null=True)
    prlib2 = models.TextField(verbose_name='PRLIB2', help_text='Software library containing red::make_wb_cube',
                              blank=True, null=True)
    prlib2a = models.TextField(verbose_name='PRLIB2A', help_text='Additional software library', blank=True, null=True)
    prlib2b = models.TextField(verbose_name='PRLIB2B', help_text='Additional software library', blank=True, null=True)
    prlib2c = models.TextField(verbose_name='PRLIB2C', help_text='Additional software library', blank=True, null=True)
    prlib2d = models.TextField(verbose_name='PRLIB2D', help_text='Additional software library', blank=True, null=True)
    prlib3 = models.TextField(verbose_name='PRLIB3', help_text='Software library containing crisp::demodulate',
                              blank=True, null=True)
    prlib3a = models.TextField(verbose_name='PRLIB3A', help_text='Additional software library', blank=True, null=True)
    prlib3b = models.TextField(verbose_name='PRLIB3B', help_text='Additional software library', blank=True, null=True)
    prlib3c = models.TextField(verbose_name='PRLIB3C', help_text='Additional software library', blank=True, null=True)
    prlib3d = models.TextField(verbose_name='PRLIB3D', help_text='Additional software library', blank=True, null=True)
    prlib4 = models.TextField(verbose_name='PRLIB4', help_text='Software library containing crisp::make_nb_cube',
                              blank=True, null=True)
    prlib4a = models.TextField(verbose_name='PRLIB4A', help_text='Additional software library', blank=True, null=True)
    prlib4b = models.TextField(verbose_name='PRLIB4B', help_text='Additional software library', blank=True, null=True)
    prlib4c = models.TextField(verbose_name='PRLIB4C', help_text='Additional software library', blank=True, null=True)
    prlib4d = models.TextField(verbose_name='PRLIB4D', help_text='Additional software library', blank=True, null=True)
    prlib5 = models.TextField(verbose_name='PRLIB5', help_text='Software library containing red::fitscube_cross',
                              blank=True, null=True)
    prlib5a = models.TextField(verbose_name='PRLIB5A', help_text='Additional software library', blank=True, null=True)
    prlib5b = models.TextField(verbose_name='PRLIB5B', help_text='Additional software library', blank=True, null=True)
    prlib5c = models.TextField(verbose_name='PRLIB5C', help_text='Additional software library', blank=True, null=True)
    prlib5d = models.TextField(verbose_name='PRLIB5D', help_text='Additional software library', blank=True, null=True)
    prlib6 = models.TextField(verbose_name='PRLIB6', help_text='Software library containing red::fitscube_expor',
                              blank=True, null=True)
    prlib6a = models.TextField(verbose_name='PRLIB6A', help_text='Additional software library', blank=True, null=True)
    prlib6b = models.TextField(verbose_name='PRLIB6B', help_text='Additional software library', blank=True, null=True)
    prlib6c = models.TextField(verbose_name='PRLIB6C', help_text='Additional software library', blank=True, null=True)
    prlib6d = models.TextField(verbose_name='PRLIB6D', help_text='Additional software library', blank=True, null=True)
    prmode1 = models.TextField(verbose_name='PRMODE1', help_text='Processing mode', blank=True, null=True)
    prmode3 = models.TextField(verbose_name='PRMODE3', help_text='Processing mode', blank=True, null=True)
    prmode4 = models.TextField(verbose_name='PRMODE4', help_text='Processing mode', blank=True, null=True)
    prmode5 = models.TextField(verbose_name='PRMODE5', help_text='Processing mode', blank=True, null=True)
    prmode6 = models.TextField(verbose_name='PRMODE6', help_text='Processing mode', blank=True, null=True)
    prpara1 = models.TextField(verbose_name='PRPARA1', help_text='List of parameters/options for PRPROC1', blank=True,
                               null=True)
    prpara2 = models.TextField(verbose_name='PRPARA2', help_text='List o', blank=True, null=True)
    prpara3 = models.TextField(verbose_name='PRPARA3', help_text='List of parameters/options for PRPROC2', blank=True,
                               null=True)
    prpara4 = models.TextField(verbose_name='PRPARA4', help_text='List of parameters/options for PRPROC4', blank=True,
                               null=True)
    prpara6 = models.TextField(verbose_name='PRPARA6', help_text='List of parameters/options for PRPROC6', blank=True,
                               null=True)
    prproc2 = models.TextField(verbose_name='PRPROC2', help_text='Name of procedure used', blank=True, null=True)
    prproc3 = models.TextField(verbose_name='PRPROC3', help_text='Name of procedure used', blank=True, null=True)
    prproc4 = models.TextField(verbose_name='PRPROC4', help_text='Name of procedure used', blank=True, null=True)
    prproc5 = models.TextField(verbose_name='PRPROC5', help_text='Name of procedure used', blank=True, null=True)
    prproc6 = models.TextField(verbose_name='PRPROC6', help_text='Name of procedure used', blank=True, null=True)
    prstep1 = models.TextField(verbose_name='PRSTEP1', help_text='Processing step name', blank=True, null=True)
    prstep2 = models.TextField(verbose_name='PRSTEP2', help_text='Processing step name', blank=True, null=True)
    prstep3 = models.TextField(verbose_name='PRSTEP3', help_text='Processing step name', blank=True, null=True)
    prstep4 = models.TextField(verbose_name='PRSTEP4', help_text='Processing step name', blank=True, null=True)
    prstep5 = models.TextField(verbose_name='PRSTEP5', help_text='Processing step name', blank=True, null=True)
    prstep6 = models.TextField(verbose_name='PRSTEP6', help_text='Processing step name', blank=True, null=True)
    prver1 = models.TextField(verbose_name='PRVER1', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver1a = models.TextField(verbose_name='PRVER1A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver1b = models.TextField(verbose_name='PRVER1B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver1c = models.TextField(verbose_name='PRVER1C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver1d = models.TextField(verbose_name='PRVER1D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver1e = models.TextField(verbose_name='PRVER1E', help_text='Library version/MJD of last update (From .momfb',
                               blank=True, null=True)
    prver2 = models.TextField(verbose_name='PRVER2', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver2a = models.TextField(verbose_name='PRVER2A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver2b = models.TextField(verbose_name='PRVER2B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver2c = models.TextField(verbose_name='PRVER2C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver2d = models.TextField(verbose_name='PRVER2D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver3 = models.TextField(verbose_name='PRVER3', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver3a = models.TextField(verbose_name='PRVER3A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver3b = models.TextField(verbose_name='PRVER3B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver3c = models.TextField(verbose_name='PRVER3C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver3d = models.TextField(verbose_name='PRVER3D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver4 = models.TextField(verbose_name='PRVER4', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver4a = models.TextField(verbose_name='PRVER4A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver4b = models.TextField(verbose_name='PRVER4B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver4c = models.TextField(verbose_name='PRVER4C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver4d = models.TextField(verbose_name='PRVER4D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver5 = models.TextField(verbose_name='PRVER5', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver5a = models.TextField(verbose_name='PRVER5A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver5b = models.TextField(verbose_name='PRVER5B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver5c = models.TextField(verbose_name='PRVER5C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver5d = models.TextField(verbose_name='PRVER5D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver6 = models.TextField(verbose_name='PRVER6', help_text='Library version/MJD of last update', blank=True,
                              null=True)
    prver6a = models.TextField(verbose_name='PRVER6A', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver6b = models.TextField(verbose_name='PRVER6B', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver6c = models.TextField(verbose_name='PRVER6C', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    prver6d = models.TextField(verbose_name='PRVER6D', help_text='Library version/MJD of last update', blank=True,
                               null=True)
    ps1_0 = models.TextField(verbose_name='PS1_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True,
                             null=True)
    ps1_1 = models.TextField(verbose_name='PS1_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
    ps1_2 = models.TextField(verbose_name='PS1_2', help_text='TTYPE for INDEX', blank=True, null=True)
    ps2_0 = models.TextField(verbose_name='PS2_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True,
                             null=True)
    ps2_1 = models.TextField(verbose_name='PS2_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
    ps2_2 = models.TextField(verbose_name='PS2_2', help_text='TTYPE for INDEX', blank=True, null=True)
    ps3_0 = models.TextField(verbose_name='PS3_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True,
                             null=True)
    ps3_1 = models.TextField(verbose_name='PS3_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
    ps5_0 = models.TextField(verbose_name='PS5_0', help_text='EXTNAME; EXTVER=EXTLEVEL=1 is default', blank=True,
                             null=True)
    ps5_1 = models.TextField(verbose_name='PS5_1', help_text='TTYPE for column w/coordinates', blank=True, null=True)
    pv1_3 = models.BigIntegerField(verbose_name='PV1_3', help_text='Coord. 1 tabulated coordinate number', blank=True,
                                   null=True)
    pv2_3 = models.BigIntegerField(verbose_name='PV2_3', help_text='Coord. 2 tabulated coordinate number', blank=True,
                                   null=True)
    pv3_3 = models.BigIntegerField(verbose_name='PV3_3', help_text='Coord. 3 tabulated coordinate number', blank=True,
                                   null=True)
    pv5_3 = models.BigIntegerField(verbose_name='PV5_3', help_text='Coord. 5 tabulated coordinate number', blank=True,
                                   null=True)
    release = models.TextField(verbose_name='RELEASE', help_text='', blank=True, null=True)
    releasec = models.TextField(verbose_name='RELEASEC', help_text='', blank=True, null=True)
    requestr = models.TextField(verbose_name='REQUESTR', help_text='', blank=True, null=True)
    scannum = models.BigIntegerField(verbose_name='SCANNUM', help_text='Scan number (first value)', blank=True,
                                     null=True)
    solarnet = models.FloatField(verbose_name='SOLARNET', help_text='Fully SOLARNET-compliant=1.0, partially=0.5',
                                 blank=True, null=True)
    startobs = models.DateTimeField(verbose_name='STARTOBS', help_text='', blank=True, null=True)
    telconfg = models.TextField(verbose_name='TELCONFG', help_text='Telescope configuration', blank=True, null=True)
    telescop = models.TextField(verbose_name='TELESCOP', help_text='Name of telescope', blank=True, null=True)
    texposur = models.FloatField(verbose_name='TEXPOSUR', help_text='Single-exposure time (median value)', blank=True,
                                 null=True)
    timesys = models.TextField(verbose_name='TIMESYS', help_text='', blank=True, null=True)
    var_keys = models.TextField(verbose_name='VAR_KEYS', help_text='SOLARNET variable-keywords', blank=True, null=True)
    waveband = models.TextField(verbose_name='WAVEBAND', help_text='', blank=True, null=True)
    wavelnth = models.FloatField(verbose_name='WAVELNTH', help_text='Prefilter peak wavelength', blank=True, null=True)
    waveunit = models.BigIntegerField(verbose_name='WAVEUNIT', help_text='WAVELNTH in units 10^WAVEUNIT m = nm',
                                      blank=True, null=True)
    wcsnamea = models.TextField(verbose_name='WCSNAMEA', help_text='', blank=True, null=True)
    xposure = models.FloatField(verbose_name='XPOSURE', help_text='Summed exposure times (median value)', blank=True,
                                null=True)

    # Apparently only in CHROMIS:
    detfirm = models.TextField(verbose_name='DETFIRM', help_text='', blank=True, null=True)
    detgain = models.FloatField(verbose_name='DETGAIN', help_text='or camera specific unit', blank=True, null=True)
    detmodel = models.TextField(verbose_name='DETMODEL', help_text='', blank=True, null=True)
    detoffs = models.BigIntegerField(verbose_name='DETOFFS', help_text='or camera specific unit', blank=True, null=True)
    extname = models.TextField(verbose_name='EXTNAME', help_text='', blank=True, null=True)
    origin = models.TextField(verbose_name='ORIGIN', help_text='', blank=True, null=True)
    prmode2 = models.TextField(verbose_name='PRMODE2', help_text='Processing mode', blank=True, null=True)

    objects = CombinedMetadataManager()

    def __str__(self):
        return self.oid

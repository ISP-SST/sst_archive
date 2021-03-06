#!/usr/bin/env bash

ENVIRONMENT="$1"
ENVIRONMENT_SETTINGS="sst_archive.settings.${ENVIRONMENT}"

shift

BASE_DIR="$1"

shift

PASS_THROUGH_OPTIONS="$@"

FITS_CUBES=(
"2019-04-16/CHROMIS/nb_3950_2019-04-16T08:20:03_scans=0-111_corrected_export2021-03-30T11:57:00_im.fits"
"2019-04-16/CHROMIS/nb_3950_2019-04-16T08:40:00_scans=0-35,38_corrected_export2021-03-30T07:38:28_im.fits"
"2019-04-16/CHROMIS/nb_3950_2019-04-16T10:15:24_scans=0-52,55-80_corrected_export2021-03-30T07:48:44_im.fits"
"2019-04-16/CHROMIS/nb_3950_2019-04-16T10:42:32_scans=0-15,17-36,38-41_corrected_export2021-03-30T08:23:22_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-05-28T15:08:12_im.fits"
"2020-08-30/CRISP/nb_6173_2020-08-30T11:35:24_scans=0-4_stokes_corrected_export2021-06-08T11:37:04_im.fits"
"2019-04-19/CHROMIS/nb_3950_2019-04-19T10:33:27_scans=0-99_corrected_export2021-03-24T15:47:37_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T10:33:29_scans=0-34_stokes_corrected_export2021-05-28T14:11:49_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T10:33:29_scans=0-34_stokes_corrected_export2021-05-29T10:14:36_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T10:49:55_scans=0-22_stokes_corrected_export2021-05-28T14:52:30_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T11:03:06_scans=0-17_stokes_corrected_export2021-05-28T14:52:02_im.fits"
"2019-04-19/CHROMIS/nb_3950_2019-04-19T10:49:53_scans=0-65_corrected_export2021-03-24T20:19:25_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T15:26:41_scans=0-35_stokes_corrected_export2021-05-28T15:07:33_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T17:42:24_scans=0-27_stokes_corrected_export2021-05-28T15:12:13_im.fits"
"2019-04-19/CHROMIS/nb_3950_2019-04-19T11:03:06_scans=0-31,33-46,48-51_corrected_export2021-03-24T20:31:22_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T18:23:36_scans=0-12,15-29_stokes_corrected_export2021-05-28T15:45:54_im.fits"
"2019-04-19/CHROMIS/nb_3950_2019-04-19T15:26:44_scans=10-19,24,26,31,32:2:38,42,51-53,55,58,59,62,64,70-80,89-92,96,97_corrected_export2021-03-24T21:33:50_im.fits"
"2019-04-19/CHROMIS/nb_3950_2019-04-19T17:34:37_scans=0-2,4-11,14_corrected_export2021-03-24T17:03:36_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T10:49:55_scans=0-22_stokes_corrected_export2021-05-29T10:14:45_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T11:03:06_scans=0-17_stokes_corrected_export2021-05-29T10:14:16_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T15:26:41_scans=0-35_stokes_corrected_export2021-05-29T10:27:17_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-03-25T09:39:57_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T17:42:24_scans=0-27_stokes_corrected_export2021-03-25T12:44:23_im.fits"
"2019-04-19/CRISP/nb_8542_2019-04-19T18:23:36_scans=0-12,15-29_stokes_corrected_export2021-03-25T11:36:36_im.fits"
"2019-04-18/CRISP/nb_8542_2019-04-18T10:37:30_scans=0-4_stokes_corrected_export2021-03-26T08:59:49_im.fits"
"2019-04-18/CRISP/nb_6173_2019-04-18T10:37:30_scans=0-4_stokes_corrected_export2021-03-26T09:13:08_im.fits"
"2019-04-18/CRISP/nb_8542_2019-04-18T17:31:34_scans=0-17_stokes_corrected_export2021-03-26T09:15:39_im.fits"
"2019-04-18/CRISP/nb_6173_2019-04-18T17:31:34_scans=0-17_stokes_corrected_export2021-03-26T09:22:12_im.fits"
"2019-04-16/CHROMIS/cubes_nb/nb_3950_2019-04-16T08:40:00_scans=0-35,38_corrected_im.fits"
"2019-04-16/CHROMIS/cubes_nb/nb_3950_2019-04-16T10:15:24_scans=0-52,55-80_corrected_im.fits"
"2019-04-16/CHROMIS/cubes_nb/nb_3950_2019-04-16T10:42:32_scans=0-15,17-36,38-41_corrected_im.fits"
"2019-04-16/CHROMIS/cubes_nb/nb_3950_2019-04-16T08:20:03_scans=0-111_corrected_im.fits"
"2019-04-16/CRISP/nb_6173_2019-04-16T08:20:03_scans=0-36,38,39_stokes_corrected_export2021-04-02T13:12:35_im.fits"
"2019-04-16/CRISP/nb_6173_2019-04-16T08:40:00_scans=0-12_stokes_corrected_export2021-04-02T13:25:20_im.fits"
"2019-04-16/CRISP/nb_6173_2019-04-16T10:15:24_scans=1-27_stokes_corrected_export2021-04-02T13:29:29_im.fits"
"2019-04-16/CRISP/nb_6173_2019-04-16T10:42:32_scans=0-13_stokes_corrected_export2021-04-02T13:37:29_im.fits"
"2019-04-16/CRISP/nb_8542_2019-04-16T08:40:00_scans=0-12_stokes_corrected_export2021-04-02T14:18:27_im.fits"
"2019-04-16/CRISP/nb_8542_2019-04-16T10:15:24_scans=0-27_stokes_corrected_export2021-04-02T14:23:33_im.fits"
"2019-04-16/CRISP/nb_8542_2019-04-16T08:20:03_scans=0-36,38,39_stokes_corrected_export2021-04-02T15:01:56_im.fits"
"2019-04-16/CRISP/nb_8542_2019-04-16T10:42:32_scans=0-5,7-13_stokes_corrected_export2021-04-02T15:44:30_im.fits"
"2019-04-24/CHROMIS/nb_3950_2019-04-24T08:30:04_scans=0-227_corrected_export2021-04-04T07:38:15_im.fits"
"2019-04-24/CRISP/nb_6173_2019-04-24T10:58:22_scans=0-11_stokes_corrected_export2021-04-05T10:14:07_im.fits"
"2019-04-24/CRISP/nb_6563_2019-04-24T10:58:22_scans=0-11_corrected_export2021-04-05T10:17:10_im.fits"
"2019-04-24/CRISP/nb_8542_2019-04-24T10:58:22_scans=0-11_stokes_corrected_export2021-04-05T10:18:33_im.fits"
"2019-04-24/CRISP/nb_6563_2019-04-24T08:30:04_scans=0-257_corrected_export2021-04-07T10:36:23_im.fits"
"2019-04-24/CRISP/nb_6173_2019-04-24T08:30:04_scans=0-257_stokes_corrected_export2021-04-11T18:22:31_im.fits"
"2019-04-24/CRISP/nb_8542_2019-04-24T08:30:04_scans=0-257_stokes_corrected_export2021-04-11T19:40:17_im.fits"
"2019-04-19/CRISP/nb_6173_2019-04-19T11:29:24_scans=0,1_corrected_im.fits"
"2020-04-25/CRISP/nb_6302_2020-04-25T11:08:59_scans=0-189_stokes_corrected_export2021-06-07T11:14:38_im.fits"
"2020-04-25/CHROMIS/nb_3950_2020-04-25T11:08:59_scans=0-117,119_corrected_export2021-06-07T10:49:48_im.fits"
"2020-04-27/CHROMIS/nb_4846_2020-04-27T07:50:04_scans=2,7,9,12,16,17,21-23,28,29,32-34,36,38_corrected_export2021-06-07T13:15:07_im.fits"
"2020-04-27/CHROMIS/nb_3950_2020-04-27T07:50:04_scans=0-32,36-38,40_corrected_export2021-06-07T13:31:24_im.fits"
"2020-04-25/CHROMIS/nb_4846_2020-04-25T11:08:59_scans=0,9:5:19,30:5:40,42,44,45,47,50,51,53,54,56,57,59-62,64-66,69-71,74,76,82,84:6:96,97,98,101,103,111,113,117,118_corrected_export2021-06-07T19:29:56_im.fits"
"2020-10-11/CHROMIS/nb_4846_2020-10-11T08:04:16_scans=1,5,6,9,10:2:16,19,21:3:27,29,32,33,35,40,42:3:48,64,66,93,103_corrected_export2021-06-07T15:13:58_im.fits"
"2020-10-11/CHROMIS/nb_3950_2020-10-11T08:04:16_scans=0:2:4,5-20,22-33,35-60,62,63,65-96,98,99,101-104,106,107_corrected_export2021-06-07T14:42:43_im.fits"
"2020-10-11/CHROMIS/nb_4846_2020-10-11T08:04:16_scans=0,2-4,7,8,11:2:17,18:2:22,23,25,26:2:30,31,34,36-39,41,43,44,46,47,49-63,65,67-92,94,95,97-102,104-106_corrected_export2021-06-07T15:24:50_im.fits"
"2020-10-11/CRISP/nb_5173_2020-10-11T08:04:16_scans=0-53_corrected_export2021-06-07T16:23:19_im.fits"
"2020-10-11/CRISP/nb_6563_2020-10-11T08:04:16_scans=0-53_corrected_export2021-06-07T16:24:33_im.fits"
"2020-10-11/CRISP/nb_8542_2020-10-11T08:04:16_scans=0-53_stokes_corrected_export2021-06-07T16:25:32_im.fits"
"2020-10-11/CRISP/nb_5173_2020-10-11T08:38:49_scans=0-37,39-63_corrected_export2021-06-07T17:42:14_im.fits"
"2020-10-11/CRISP/nb_6563_2020-10-11T08:38:49_scans=0-5,7-36,39-58,60-63_corrected_export2021-06-07T17:44:39_im.fits"
"2020-10-11/CRISP/nb_8542_2020-10-11T08:38:49_scans=0-63_stokes_corrected_export2021-06-07T18:08:19_im.fits"
"2020-10-11/CHROMIS/nb_3950_2020-10-11T08:38:49_scans=0,3,5-10,12,13,15,18,20,24,25,27-33,37-46,48,50-52,54-66,70-75,81,82,84,85,89-92,96-99,106,107,109-114,117,123,125,128-130_corrected_export2021-06-07T18:34:15_im.fits"
"2020-04-25/CHROMIS/nb_4846_2020-04-25T11:08:59_scans=1-8,10-13,15-18,20-29,31-34,36-39,41,43,46,48,49:3:58,63,67,68,72,73:2:77,78-81,83,85-89,91-95,99,100:2:104,105-110,112,114-116,119_corrected_export2021-06-07T19:30:12_im.fits"
"2020-10-11/CHROMIS/nb_3950_2020-10-11T09:16:47_scans=0-4,6-9,11:2:15,16,18-21,23,25,26,28-32,34,36_corrected_export2021-06-07T20:50:10_im.fits"
"2020-10-11/CHROMIS/nb_4846_2020-10-11T09:16:47_scans=8,10,14,16,20:2:26,27,32,33_corrected_export2021-06-07T21:57:47_im.fits"
"2020-10-11/CHROMIS/nb_4846_2020-10-11T09:16:47_scans=0-7,11:2:17,18,19:2:25,28-31,34,35_corrected_export2021-06-07T21:58:14_im.fits"
"2020-10-11/CRISP/nb_5173_2020-10-11T09:16:47_scans=0-16_corrected_export2021-06-07T22:13:39_im.fits"
"2020-10-11/CRISP/nb_6563_2020-10-11T09:16:47_scans=0-16_corrected_export2021-06-07T22:14:42_im.fits"
"2020-10-11/CRISP/nb_8542_2020-10-11T09:16:47_scans=0-16_stokes_corrected_export2021-06-07T22:15:50_im.fits"
"2020-04-25/CRISP/nb_8542_2020-04-25T11:08:59_scans=0-186,188,189_corrected_export2021-06-07T16:45:12_im.fits"
"2020-10-11/CHROMIS/nb_4846_2020-10-11T08:38:49_scans=3,4,6,7,9,10:2:14,17,20,25-27,29-34,36-45,47,49-66,69-74,76-82,84,85,88-93,96,97,99-107,109,111-115,119,121,125,127-129_corrected_export2021-06-07T21:54:42_im.fits"
"2020-04-25/CRISP/nb_6563_2020-04-25T11:08:59_scans=0-189_corrected_export2021-06-07T16:41:19_im.fits"
"2020-04-24/CRISP/nb_6302_2020-04-24T11:26:22_scans=0-151,155-184,186-227,229-239_stokes_corrected_export2021-06-08T08:24:35_im.fits"
"2020-08-30/CRISP/nb_6173_2020-08-30T11:06:20_scans=0-10_stokes_corrected_export2021-06-08T10:35:43_im.fits"
"2020-08-30/CRISP/nb_6563_2020-08-30T11:06:20_scans=0-10_corrected_export2021-06-08T10:56:08_im.fits"
"2020-08-30/CRISP/nb_8542_2020-08-30T11:06:20_scans=0-10_stokes_corrected_export2021-06-08T11:08:39_im.fits"
"2020-08-30/CRISP/nb_6563_2020-08-30T11:35:24_scans=0-4_corrected_export2021-06-08T11:39:51_im.fits"
"2020-08-30/CRISP/nb_8542_2020-08-30T11:35:24_scans=0-4_stokes_corrected_export2021-06-08T11:46:13_im.fits"
"2020-08-30/CHROMIS/nb_4846_2020-08-30T11:06:20_scans=0-18_corrected_export2021-06-08T10:29:56_im.fits"
"2020-08-30/CHROMIS/nb_3950_2020-08-30T11:06:20_scans=0-18_corrected_export2021-06-08T10:30:07_im.fits"
"2020-08-30/CHROMIS/nb_3950_2020-08-30T11:35:24_scans=0-7_corrected_export2021-06-08T11:54:22_im.fits"
"2020-04-24/CHROMIS/nb_3950_2020-04-24T11:26:25_scans=0-23,25,26,28-188,190-211,215-258,260-287,289-317,321-331,333-335_corrected_export2021-06-08T08:58:48_im.fits"
"2020-08-30/CHROMIS/nb_4846_2020-08-30T11:35:24_scans=0-8_corrected_export2021-06-08T13:03:29_im.fits"
"2020-10-16/CRISP/nb_6173_2020-10-16T09:11:04_scans=0-2,4-6_stokes_corrected_export2021-06-08T16:22:56_im.fits"
"2020-04-24/CRISP/nb_8542_2020-04-24T11:26:22_scans=0-134,136-151,154-185,187-228,230-239_stokes_corrected_export2021-06-08T08:58:34_im.fits"
"2020-08-30/CRISP/nb_6173_2020-08-30T09:38:36_scans=0-21_stokes_corrected_export2021-06-08T14:56:14_im.fits"
"2020-08-30/CHROMIS/nb_3950_2020-08-30T09:38:36_scans=0-14_corrected_export2021-06-08T14:54:18_im.fits"
"2020-10-16/CRISP/nb_6563_2020-10-16T09:11:04_scans=0,1,3-5_corrected_export2021-06-08T15:21:18_im.fits"
"2020-08-30/CHROMIS/nb_3950_2020-08-30T10:09:06_scans=0-21,23-69_corrected_export2021-06-08T15:13:14_im.fits"
"2020-08-30/CRISP/nb_6173_2020-08-30T10:09:06_scans=0-121_stokes_corrected_export2021-06-08T15:14:22_im.fits"
"2020-10-16/CRISP/nb_6173_2020-10-16T08:58:56_scans=0-35_stokes_corrected_export2021-06-08T16:07:09_im.fits"
"2020-10-16/CRISP/nb_8542_2020-10-16T09:11:04_scans=0-6_stokes_corrected_export2021-06-08T16:23:26_im.fits"
"2020-10-16/CHROMIS/nb_3950_2020-10-16T08:58:56_scans=0-7,9-17_corrected_export2021-06-08T16:05:25_im.fits"
"2020-10-16/CHROMIS/nb_4846_2020-10-16T09:11:04_scans=0-10_corrected_export2021-06-08T15:40:55_im.fits"
)

ROOT_DIR="$(dirname "$(dirname "$(realpath "$0")")")"

MAX_COUNT=100

INGESTION_OPTIONS="--settings ${ENVIRONMENT_SETTINGS} ${PASS_THROUGH_OPTIONS}"

MPLCONFIGDIR=`mktemp -d`
echo "Creating MPLCONFIGDIR $MPLCONFIGDIR"

export MPLCONFIGDIR="$MPLCONFIGDIR"

function cleanup {
  rm -rf "$MPLCONFIGDIR"
  echo "Deleted MPLCONFIGDIR $WORK_DIR"
}

trap cleanup EXIT

. "${ROOT_DIR}/venv/bin/activate"

for file in "${FITS_CUBES[@]}"; do
  if [ "$MAX_COUNT" -le 0 ]; then
    echo "Hit max count of cubes to import, aborting."
    break;
  else
    ((MAX_COUNT=MAX_COUNT - 1))
  fi

  echo "Ingesting FITS cube: ${file}"
  "${ROOT_DIR}/manage.py" ingest_fits_cube ${INGESTION_OPTIONS} -f "${BASE_DIR}/${file}"
done

deactivate

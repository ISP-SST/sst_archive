#!/usr/bin/env sh

BASE_DIR="/Users/dani2978/local_science_data"

FITS_CUBES=(
"2019-04-19/CRISP/nb_6173_2019-04-19T17:34:39_scans=0-4_stokes_corrected_export2021-05-28T15:08:12_im.fits"
"2020-08-30/CRISP/nb_6173_2020-08-30T11:35:24_scans=0-4_stokes_corrected_export2021-06-08T11:37:04_im.fits"
)

MAX_COUNT=10

for file in "${FITS_CUBES[@]}"; do
  if [ "$MAX_COUNT" -le 0 ]; then
    echo "Hit max count of cubes to import, aborting."
    break;
  else
    ((MAX_COUNT=MAX_COUNT - 1))
  fi

  echo "Ingesting FITS cube: ${file}"
  ./manage.py ingest_fits_cube -f "${BASE_DIR}/${file}"

done

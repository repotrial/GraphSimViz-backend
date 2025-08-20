#/usr/bin/env bash

echo "Preparing result data"
wget -q https://cloud.uni-hamburg.de/public.php/dav/files/ka4AHFgSDTg765P/?accept=zip -O results.zip
unzip -q results.zip
cd result_data
unzip -q '*.zip'
rm *.zip
rm -rf __MACOSX
rm -rf **/__MACOSX
cd ..
mv result_data/* .
rm -rf result_data
mv GED_drug_indication_distances_vs_DrPPD GED_drug_indication_distances_vs_DrPD
cd GED_drug_indication_distances_vs_DrPD_UMLS
mv global_mwu_p_values.csv global_mwu_p_values_together.csv
cd ..

echo "Preparing source data"
wget -q https://cloud.uni-hamburg.de/public.php/dav/files/od5pEkwiAScWtc9/?accept=zip -O source_data.zip

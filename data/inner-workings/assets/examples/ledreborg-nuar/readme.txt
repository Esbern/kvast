Example data: 2026 norms and NUAR at Ledreborg
==============================================

Data for the SemanticGIS example comparing the 2026 nitrogen norms with NUAR (2027) at Ledreborg Gods, Lejre (Agriculture), frozen as they were used.

  2026 norms and NUAR at Ledreborg: https://semanticgis.org/domain-hubs/agriculture/2026-norms-and-nuar-at-ledreborg-(example)

Date:  2026-11-12 (the data as they were on this date)
CRS:   EPSG:25832
Area:  681231, 6165603, 686468, 6170768 (EPSG:25832)


Files
-----

ledreborg_nuar.gpkg  Field pieces with NUAR inputs and results, and landscapes (GeoPackage)
  Marker 2024–2026 flattened (2 m) within the landscapes; pieces of at least 0.05 ha with a crop in all three years. Results from NUAR-regneark v1.3 (SEGES/Aarhus University) through the nuar code, for two catch-crop scenarios.
  layer fields: field pieces, inputs and results (517 features)
  layer landscapes: the example's landscape types (8 features)


Code lists
----------

The coded fields keep their codes; the names are in codelists/ (join them by code,
e.g. Layer Properties > Joins in QGIS).

codelists/crop_codes_dk.csv  Danish crop codes: names in Danish and English, groups, categories, simplified classes  (source: https://semanticgis.org/data/code-lists/danish-crop-codes-(afgkode), retrieved 2026-11-12)


Sources, licences and attribution
---------------------------------

Marker 2024–2026, Jordbundskort 2024, Kvælstofretention UMR 2027: Styrelsen for Grøn Arealomlægning og Vandmiljø
  Free public data, fetched 12 November 2026; Marker 2026 is preliminary.
  Attribution: Indeholder data fra Styrelsen for Grøn Arealomlægning og Vandmiljø, hentet 12. november 2026

Jordartskort 1:25 000: GEUS
  Version 7.1, January 2026. Attribution: Indeholder data fra GEUS, Jordartskort 1:25 000

Kulstof 2022 and DJF_LAVBUND: via Danmarks Miljøportal
  Fetched 12 November 2026.

DMI 10 km climate grid
  dmidk/Climate-Data-Grid-Map; the NUAR cell numbering is inferred (see the nuar code).

Model: NUAR-regneark v1.3 (SEGES Innovation / Aarhus University), via https://github.com/Esbern/nuar
  A preliminary tool; the final regulation may differ. The tables of the workbook are not included.

Landscapes
  Digitised for the example by Esbern Holmes, Roskilde University.

The extracts are for teaching and for reproducing the examples. For other areas or
dates, use the original sources: their pages on semanticgis.org link to them.

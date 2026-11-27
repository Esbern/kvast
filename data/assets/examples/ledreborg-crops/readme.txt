Example data: Crop rotations at Ledreborg
=========================================

Data for the SemanticGIS example on crop rotations at Ledreborg Gods, Lejre (Agriculture), frozen as they were used, so the example's numbers can be reproduced without downloading.

  Crop rotations at Ledreborg: https://semanticgis.org/domain-hubs/agriculture/crop-rotations-at-ledreborg-(example)

Date:  2026-11-12 (the data as they were on this date)
CRS:   EPSG:25832
Area:  681231, 6165603, 686468, 6170768 (EPSG:25832)


Files
-----

ledreborg_crops.gpkg  Fields 2021–2026 and landscapes (GeoPackage)
  Marker 2021–2026 as the example used it: fetched with Download snapshot series (SemanticGIS plugin), clipped to the landscapes, one feature per field and year. Identifiers of the applicant are left out.
  layer marker: Marker 2021–2026, clipped to the landscapes (2814 features)
  layer landscapes: the example's landscape types (8 features)


Code lists
----------

The coded fields keep their codes; the names are in codelists/ (join them by code,
e.g. Layer Properties > Joins in QGIS).

codelists/crop_codes_dk.csv  Danish crop codes: names in Danish and English, groups, categories, simplified classes  (source: https://semanticgis.org/data/code-lists/danish-crop-codes-(afgkode), retrieved 2026-11-12)


Sources, licences and attribution
---------------------------------

Marker 2021–2026: Styrelsen for Grøn Arealomlægning og Vandmiljø, WFS geodata.fvm.dk
  Free public data. Fetched 12 November 2026; 2026 is preliminary.
  Attribution: Indeholder data fra Styrelsen for Grøn Arealomlægning og Vandmiljø, Marker, hentet 12. november 2026
  (standard wording; check the publisher's terms before publishing)

Crop codes: SemanticGIS, from the agency's Oversigt over afgrødekoder til Fællesskema 2026
  English names and simplified classes by SemanticGIS.

Landscapes
  Digitised for the example by Esbern Holmes, Roskilde University.

The extracts are for teaching and for reproducing the examples. For other areas or
dates, use the original sources: their pages on semanticgis.org link to them.

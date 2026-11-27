Example data: Habitats and soil carbon at Ledreborg
===================================================

Data for the SemanticGIS examples at Ledreborg Gods, Lejre (Landscape ecology and Soil), frozen as they were used, so the examples' numbers can be reproduced without API keys.

  Habitat network at Ledreborg: https://semanticgis.org/Domain-hubs/Landscape-ecology/Habitat-network-at-Ledreborg-(Example)
  Soil carbon and land use at Ledreborg: https://semanticgis.org/Domain-hubs/Soil/Soil-carbon-and-land-use-at-Ledreborg-(Example)

Date:  2026-10-27 (the data as they were on this date)
CRS:   EPSG:25832
Area:  679077, 6164317, 687782, 6171607 (EPSG:25832)


Files
-----

ledreborg_example.gpkg  Landscapes and nature content (GeoPackage)
  Whole features: every feature that touches the area is included, not cut at its edge, exactly as the examples used them.
  layer landscapes: the example's landscape types (8 features)
  layer protected_nature: §3 protected nature (Beskyttede naturtyper) (695 features)
  layer woodland: GeoDanmark Skov (239 features)
  layer hedges: GeoDanmark Hegn (12645 features)
  layer streams: GeoDanmark Vandløbsmidte (1183 features)

basemap04_lu_agg_2021_ledreborg.tif  Basemap04 aggregated land use 2021, 10 m (COG)
  Styles: basemap04_lu_agg_2021_ledreborg.qml (English names), _da.qml (Danish).
  35 classes, named in codelists/basemap04_lu_agg_2021.csv

soc_0_30cm_ledreborg.tif  Soil organic carbon 0–30 cm, % by mass, 10 m (COG)
  NoData −1. Style: soc_0_30cm_ledreborg.qml.


Code lists
----------

The coded fields keep their codes; the names are in codelists/ (join them by code,
e.g. Layer Properties > Joins in QGIS).

codelists/basemap04_lu_agg_2021.csv  Basemap04 aggregated land-use classes  (source: Basemap04, lu_agg_2021.tif.vat.dbf (the raster attribute table distributed with the map), retrieved 2026-10-24)


Sources, licences and attribution
---------------------------------

GeoDanmark (Skov, Hegn, Vandløbsmidte): Klimadatastyrelsen and the municipalities, via Datafordeleren
  Free public data.
  Attribution: Indeholder data fra Klimadatastyrelsen, GeoDanmark, hentet 27. oktober 2026

Beskyttede naturtyper (§3): the municipalities, via Danmarks Miljøportal
  Attribution: Indeholder data fra Kommunerne, Beskyttede naturtyper, hentet 27. oktober 2026
  (standard wording; check the publisher's terms before publishing)

Basemap04: Aarhus University, Department of Environmental Science (DCE)
  Open access. Cite: Levin, G. 2022. Basemap04. Documentation of the data and method for the
  elaboration of a land use and land cover map for Denmark. Aarhus University, DCE - Danish Centre
  for Environment and Energy, 77 pp. Technical Report No. 252.
  The map is not legally binding and cannot be used for handling cases about land use and land cover.

Kulstofkort i 10 m opløsning (SOC 0-30 cm), version 1.1, 4 July 2024
  Licence CC BY 4.0. Copyright Aarhus Universitet, DHI, SEGES, Københavns Universitet.
  Author Anders Bjørn Møller, Aarhus Universitet. Method: Møller, A. B. et al. 2025. Advances in
  Agronomy 194, 133-. doi:10.1016/bs.agron.2025.07.001

Landscapes
  Digitised for the example by Esbern Holmes, Roskilde University.

The extracts are for teaching and for reproducing the examples. For other areas or
dates, use the original sources: their pages on semanticgis.org link to them.

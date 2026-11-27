Example data: Dwellings in Copenhagen
=====================================

Data for the SemanticGIS examples on dwellings in Copenhagen (Housing studies), frozen as they were used, so the examples' numbers can be reproduced without API keys.

  Share of rented dwellings in Copenhagen: https://semanticgis.org/Domain-hubs/Housing-studies/Share-of-rented-dwellings-in-Copenhagen-(Example)
  Dwelling size by construction period in Copenhagen: https://semanticgis.org/Domain-hubs/Housing-studies/Dwelling-size-by-construction-period-in-Copenhagen-(Example)

Date:  2026-10-24 (the data as they were on this date)
CRS:   EPSG:25832
Area:  716908, 6168578, 734618, 6182092 (EPSG:25832)


Files
-----

dwellings.parquet  Standing dwellings (GeoParquet, points)
  Every standing dwelling in Københavns Kommune (BBR status 6, use 110–190) on its entrance's address point (DAR). Addresses, register ids and coordinate fields are left out.
  349,743 rows
    status_kode              BBR status (6 = standing)  [codes: codelists/bbr_livscyklus.csv]
    anvendelse_kode          use of the unit (110–190 = dwellings)  [codes: codelists/bbr_enhedens_anvendelse.csv]
    samlet_areal             total area, m²
    areal_beboelse           residential area, m²
    antal_vaerelser          number of rooms
    udlejning_kode           rental arrangement  [codes: codelists/bbr_udlejningsforhold.csv]
    offentlig_stoette_kode   public support  [codes: codelists/bbr_offentlig_stoette.csv]
    opfoerelsesaar           the building's construction year

divisions.gpkg  Københavns Kommune's statistical divisions (GeoPackage)
  The same divisions as Statistikbanken, as published by SemanticGIS.
  layer bydel: bydele, 10 districts (10 features)
  layer lokaludvalg: local council areas, 12 (12 features)
  layer kvarter: statistical neighbourhoods, 67 (67 features)
  layer rode: roder, 400 smallest statistical units (400 features)


Code lists
----------

The coded fields keep their codes; the names are in codelists/ (join them by code,
e.g. Layer Properties > Joins in QGIS).

codelists/bbr_livscyklus.csv  BBR Livscyklus (status)  (source: https://teknik.bbr.dk/kodelister/0/1/0/Livscyklus, retrieved 2026-10-28)
codelists/bbr_enhedens_anvendelse.csv  BBR Enhedens anvendelse (use)  (source: https://teknik.bbr.dk/kodelister/0/1/0/EnhAnvendelse, retrieved 2026-10-28)
codelists/bbr_udlejningsforhold.csv  BBR Udlejningsforhold (rental arrangement)  (source: https://teknik.bbr.dk/kodelister/0/1/0/Udlejningsforhold, retrieved 2026-10-28)
codelists/bbr_offentlig_stoette.csv  BBR Offentlig støtte (public support)  (source: https://teknik.bbr.dk/kodelister/0/1/0/OffentligStoette, retrieved 2026-10-28)


Sources, licences and attribution
---------------------------------

BBR (Bygnings- og Boligregistret) and DAR (Danmarks Adresseregister), via Datafordeleren
  Free public data. Extracted 24 October 2026.
  Attribution: Indeholder data fra BBR og DAR (Datafordeleren), hentet 24. oktober 2026
  (standard wording; check Datafordeleren's terms before publishing)

Statistical divisions: Københavns Kommune
  Open data (CC BY 4.0, via opendata.dk), snapshot 22 October 2026,
  renumbered to Statistikbanken's codes by SemanticGIS.

Code lists: BBR, teknik.bbr.dk/kodelister
  Retrieved on the date given for each list.

The extracts are for teaching and for reproducing the examples. For other areas or
dates, use the original sources: their pages on semanticgis.org link to them.

# -*- coding: utf8 -*-
import geopandas
from pathlib import Path
import argparse
import matplotlib
from shapely.affinity import translate
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("path", type=Path)
dataset = parser.parse_args()

output_dir = Path.cwd() / "countries"
if not output_dir.exists():
  Path.mkdir(output_dir)
# Path to where the countries are saved to
with open(output_dir / "country_flags.pkl", "rb") as f:
  country_flags = pickle.load(f)

if dataset.path.exists():
  if dataset.path.is_dir():
    for file in dataset.path.iterdir():
      if file.suffix == ".shp":
        dataset.path = file
    if dataset.path.suffix != ".shp":
      raise Exception("No Shapefile in folder!")
  else:
    pass
else:
  raise Exception("Folder does not exist!")

dataset = geopandas.read_file(dataset.path)

def wrap_antimeridian(geom):
  geom = geom.explode()
  
  leftside = []
  rightside = []
  for region in geom:
    if region.bounds[0] >= 0:
      rightside.append(region)
    else:
      leftside.append(region)
  
  if geopandas.GeoSeries(leftside).area.max() > geopandas.GeoSeries(rightside).area.max():
    rightside = [translate(region, xoff=-360) for region in rightside]
  else:
    leftside = [translate(region, xoff=360) for region in leftside]
  
  return geopandas.GeoSeries(leftside + rightside)

def check_flags(country_list):
  for country_data in country_list:
    if not 'flag' in country_data:
      print(country_data['names'])

countries = []
for country in dataset.itertuples():
  if (country.TYPE == "Country" or country.TYPE == "Sovereign country"):
    feature_geometry = geopandas.GeoSeries(country.geometry).explode(index_parts=True)

    # If the difference between xmax and xmin is too high, transform parts of the region on the right to the left
    # Primarily meant for regions like the USA, where Alaska is on both the left and right side of the map
    if (feature_geometry.total_bounds[2] - feature_geometry.total_bounds[0]) >= 300:
      feature_geometry = wrap_antimeridian(feature_geometry)

    # Get the largest landmass by area
    largest_landmass = geopandas.GeoSeries(feature_geometry.loc[feature_geometry.area.idxmax()])

    # Create a buffer around the landmass equal to 300% of the diagonal distance across the boundary
    landmass_buffer = largest_landmass.boundary.buffer(
      geopandas.GeoSeries(
        geopandas.points_from_xy(largest_landmass.bounds.minx, largest_landmass.bounds.miny)
      ).distance(
        geopandas.GeoSeries(
          geopandas.points_from_xy(largest_landmass.bounds.maxx, largest_landmass.bounds.maxy)
        )
      ) * 3
    )

    # Include only regions that are greater than 1% the size of the largest landmass
    # Not really needed, so it's disabled, but saved here but just in case
    # feature_geometry = feature_geometry[feature_geometry.area > (largest_landmass[0].area * 0.01)]

    # Create a region only including landmasses within the buffer
    # Not an editorial decision, just looks nicer if France doesn't have to render its territory in Africa,
    # or if Norway doesn't have to render its territory down south
    region = feature_geometry.intersection(landmass_buffer[0])
    region = region.set_crs("EPSG:4326")
    region.plot(
      color="#5865F2"
    ).set_axis_off()
    matplotlib.pyplot.savefig(
      output_dir / f"{country.NAME_EN}.png",
      transparent=True,
      bbox_inches='tight' # Tight borders around image
    )
    matplotlib.pyplot.close()
    print(f"Saved {country.NAME_EN}.png")
    countrynames = []
    for key, value in country._asdict().items():
        if ("NAME" in key or "FORMAL" in key) and (type(value) == str):
          if not value in countrynames:
            countrynames.append(value)
    countries.append(
      {
        "names": countrynames,
        "type": country.TYPE,
        "path": (output_dir / f"{country.NAME_EN}.png").relative_to(Path.cwd())
      }
    )

# Add flags to countries data
for country_data in countries:
  for flag in country_flags:
    if flag in country_data['names']:
      country_data['flag'] = country_flags[flag]
      break

with open(output_dir / "country_info.pkl", "wb") as country_info:
  pickle.dump(countries, country_info)
# Last updated 2/19/2026
# Used Natural Earth dataset v5.1.1
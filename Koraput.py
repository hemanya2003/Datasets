{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNL3Oc01K8MMrSMQhX/bwes",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/hemanya2003/Datasets/blob/main/Koraput.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "r_MrVaXYi18B"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import geopandas as gpd\n",
        "import pydeck as pdk\n",
        "\n",
        "# Load your shapefile\n",
        "shapefile_path = \"LUSE_FINAL.shp\"  # Make sure the shapefile is in the repo\n",
        "gdf = gpd.read_file(shapefile_path)\n",
        "\n",
        "# Reproject to EPSG:4326 (WGS84) if necessary\n",
        "if gdf.crs != 'EPSG:4326':\n",
        "    gdf = gdf.to_crs(epsg=4326)\n",
        "\n",
        "# Explode MultiPolygon geometries into individual Polygon geometries\n",
        "gdf = gdf.explode(index_parts=True).reset_index(drop=True)\n",
        "\n",
        "# Define heights for each LANDUSE category\n",
        "landuse_heights = {\n",
        "    'bare': 15, 'built': 30, 'crops': 10, 'grass': 20,\n",
        "    'shrub_and_scrub': 25, 'trees': 35, 'water': -5\n",
        "}\n",
        "\n",
        "# Define colors for each LANDUSE category (in RGB format)\n",
        "landuse_colors = {\n",
        "    'bare': [255, 192, 203], 'built': [255, 0, 0], 'crops': [255, 255, 0],\n",
        "    'grass': [144, 238, 144], 'shrub_and_scrub': [255, 0, 255], 'trees': [0, 128, 0], 'water': [0, 0, 255]\n",
        "}\n",
        "\n",
        "# Assign heights and colors\n",
        "gdf['height'] = gdf['LANDUSE'].map(landuse_heights)\n",
        "gdf['color'] = gdf['LANDUSE'].map(landuse_colors)\n",
        "\n",
        "# Replace with your MapTiler API key\n",
        "MAPTILER_API_KEY = \"E6ZRsLot4eQsQImxowwm\"\n",
        "\n",
        "# Create a PyDeck layer\n",
        "polygon_layer = pdk.Layer(\n",
        "    'PolygonLayer',\n",
        "    data=gdf,\n",
        "    get_polygon='geometry.coordinates',\n",
        "    extruded=True,\n",
        "    get_elevation='height',\n",
        "    get_fill_color='color',\n",
        "    elevation_scale=1,\n",
        "    pickable=True,\n",
        ")\n",
        "\n",
        "# Create a TileLayer for MapTiler Satellite Imagery\n",
        "tile_layer = pdk.Layer(\n",
        "    'TileLayer',\n",
        "    data=None,\n",
        "    get_tile_data=f'https://api.maptiler.com/maps/hybrid/{{z}}/{{x}}/{{y}}.jpg?key={MAPTILER_API_KEY}',\n",
        "    pickable=False,\n",
        ")\n",
        "\n",
        "# Set the view state to center on the data\n",
        "view_state = pdk.ViewState(\n",
        "    latitude=gdf.geometry.centroid.y.mean(),\n",
        "    longitude=gdf.geometry.centroid.x.mean(),\n",
        "    zoom=10,\n",
        "    pitch=45,\n",
        "    bearing=30,\n",
        ")\n",
        "\n",
        "# Create a PyDeck map\n",
        "deck = pdk.Deck(layers=[tile_layer, polygon_layer], initial_view_state=view_state)\n",
        "\n",
        "# Streamlit App\n",
        "st.title(\"3D Land Use Visualization\")\n",
        "\n",
        "st.pydeck_chart(deck)"
      ]
    }
  ]
}
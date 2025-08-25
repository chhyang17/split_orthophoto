# split_orthophoto

A tiny Python utility that splits a large orthophoto (GeoTIFF) into multiple tiles based on a maximum uncompressed file size target.

The script estimates how many tiles are needed from the raster’s dimensions, band count, and data type, then cuts a roughly square grid of tiles and writes them with LZW compression (GeoTIFF). Georeferencing is preserved via `gdal.Translate`.

---

## What you need to edit

Open `split_orthophoto.py` and update these three lines:

```python
input_file = r"file_path_to_Ortho.tif"                  # ← your source orthophoto
output_folder = r"file_path_to_output\OrthophotoTiles"  # ← where tiles will be written
max_file_size = 1 * 1024 * 1024 * 1024                  # ← target size per tile (bytes). Default: 1 GB

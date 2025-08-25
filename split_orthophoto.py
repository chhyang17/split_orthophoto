import os
import math

# === Environment Fix: Ensure GDAL uses correct PROJ version ===

os.environ['PROJ_LIB'] = r"C:\Users\anaconda3\envs\orthophoto\Library\share\proj"
os.environ['PROJ_NETWORK'] = 'OFF'
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'TRUE'

original_path = os.environ.get('PATH', '')
path_parts = original_path.split(';')
filtered_path = [p for p in path_parts if 'PostgreSQL' not in p and 'postgis' not in p.lower()]
os.environ['PATH'] = ';'.join(filtered_path)

print("✅ PATH scrubbed. Using PROJ_LIB:", os.environ['PROJ_LIB'])

# === Now safe to import GDAL ===

from osgeo import gdal
gdal.UseExceptions()

# === User Configuration ===

input_file = r"file_path_to_Ortho.tif"

output_folder = r"file_path_to_output\OrthophotoTiles"

max_file_size = 1 * 1024 * 1024 * 1024  # 1 GB

# === Open Raster ===

os.makedirs(output_folder, exist_ok=True)
dataset = gdal.Open(input_file)
if not dataset:
    raise RuntimeError("❌ Failed to open input orthophoto.")

width = dataset.RasterXSize
height = dataset.RasterYSize
bands = dataset.RasterCount
datatype = dataset.GetRasterBand(1).DataType
bytes_per_pixel = gdal.GetDataTypeSize(datatype) // 8
bytes_total = bytes_per_pixel * bands

# === Estimate number of tiles needed ===

total_size = width * height * bytes_total
num_tiles = math.ceil(total_size / max_file_size)

tiles_x = tiles_y = math.ceil(math.sqrt(num_tiles))
tile_width = width // tiles_x
tile_height = height // tiles_y

print(f"📐 Estimated tiles: {tiles_x} x {tiles_y} = {tiles_x * tiles_y} tiles")

# === Split Image ===

tile_index = 0
for i in range(tiles_y):
    for j in range(tiles_x):
        x_off = j * tile_width
        y_off = i * tile_height
        w = tile_width if j < tiles_x - 1 else width - x_off
        h = tile_height if i < tiles_y - 1 else height - y_off

        out_file = os.path.join(output_folder, f"tile_{i}_{j}.tif")
        print(f"🧩 Writing {out_file} ...")

        gdal.Translate(
            out_file,
            dataset,
            srcWin=[x_off, y_off, w, h],
            creationOptions=["COMPRESS=LZW"]
        )

        tile_index += 1

print(f"\n✅ Done! {tile_index} tiles saved to:\n{output_folder}")


from netCDF4 import Dataset

file_path = "./mosdac_downloads_nc_files/E06OCML3AD_20230601_01km_LAC_v1.0.0.nc"

dataset = Dataset(file_path, mode='r')

print("🔹 Global Attributes:")
for attr in dataset.ncattrs():
    print(f"{attr}: {getattr(dataset, attr)}")

print("\n🔹 Dimensions:")
for dim in dataset.dimensions.items():
    print(f"{dim[0]}: {len(dim[1])}")

print("\n🔹 Variables:")
for var_name, var in dataset.variables.items():
    print(f"{var_name} ({var.dimensions}): {var.shape}")

if "temperature" in dataset.variables:
    temp = dataset.variables["temperature"]
    print("\n🔹 Sample 'temperature' data (first 10 values):")
    print(temp[:10])

dataset.close()

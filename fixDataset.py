import shutil
import os
import csv
from PIL import Image

# Preprocessing

# We reorganize the dataset to create one filter by type

# For the dataset with the name of each pokemon
file = "./dataset/pokemon_types_names.csv"
with open(file, 'r') as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip the header
    pkm_dict1 = {rows[1]: rows[2] for rows in reader}

for pkm_name, pkm_type in pkm_dict1.items():
    source = './dataset/dataset/{pkm_name}/'.format(pkm_name=pkm_name)
    dest = './Pokemon/dataset/{pkm_type}'.format(pkm_type=pkm_type)
    if not os.path.exists(source):
        continue
    for f in os.listdir(source):
        # If directory does not exist, create it
        if not os.path.exists(dest):
            os.makedirs(dest)

        # Modify the file name by adding the Pokémon name as a suffix
        file_name, file_ext = os.path.splitext(f)
        new_file_name = pkm_name + '_' + '1'

        # Verify if files with suffix were created in the destination
        files_with_suffix = [f for f in os.listdir(dest) if f.startswith(pkm_name)]
        if files_with_suffix:
            # Find the maximum suffix number and increment by 1
            max_suffix = max([int(f.split('_')[-1].split('.')[0]) for f in files_with_suffix])
            new_suffix = str(max_suffix + 1)
            file_name, file_ext = os.path.splitext(f)
            new_file_name = pkm_name + '_' + new_suffix + file_ext
        else:
            file_name, file_ext = os.path.splitext(f)
            new_file_name = pkm_name + '_1' + file_ext
            print("No files created with suffix called " + pkm_name + " in the destination directory")

        # Copy the files to the destination directory with the new file name
        shutil.copy(os.path.join(source, f), os.path.join(dest, new_file_name))

        # Check if the file is an SVG
        if file_ext.lower() == ".svg":
            print("Skipping SVG file:", f)
            continue

        # Open the image and convert it to RGB mode
        image_path = os.path.join(dest, new_file_name)
        image = Image.open(image_path)
        image = image.convert("RGB")

        # Resize the copied image to 200x200 pixels and save it as PNG
        resized_image = image.resize((200, 200))

        # Save the resized image with PNG format
        new_file_path = os.path.splitext(image_path)[0] + ".png"
        resized_image.save(new_file_path, format="PNG")

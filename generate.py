import json
import os
import random
import sys
from copy import deepcopy

from PIL import Image

config = json.load(open(("config.json")))

IMAGE_COUNT = int(sys.argv[1])
METADATA_TEMPLATE = json.loads(open("metadata_template.json").read())
PADDING_AMOUNT = len(str(IMAGE_COUNT))
SCALE_FACTOR = 20


def get_random_image() -> {}:
    """Returns dictionary containing attributes and a random values.

    Example:
        >>> get_random_image()
        {"rice": "white", "background": "beige": "mouth": "smile", "front": "nori"}

    """
    new_image = {}

    for layer in config["layers"]:
        # Skip backgrounds since they're added at the end.
        if layer["name"] == "background":
            continue
        # Choose a random attribute based on given probabilities and add it to this image's metadata.
        choice = random.choices(list(layer["values"].keys()), layer["values"].values())[0]
        new_image[layer["name"]] = choice

    return new_image


def generate_all_image_metadata() -> []:
    """Returns array of dictionaries containing unique attribute metadata.

    Example:
        >>> generate_all_image_metadata()
        [{'body': 'triangle', 'front': 'nori'}, {'body': 'triangle', 'front': 'suit'}]

    """
    all_images = []

    while len(all_images) < IMAGE_COUNT:
        new_trait_image = get_random_image()
        # If the generated metadata already exists, skip it.
        if new_trait_image in all_images:
            continue
        all_images.append(new_trait_image)

    # Add backgrounds. Backgrounds are added separately to ensure each NFT has a unique combination of attributes.
    for image in all_images:
        # Choose a random background based on probabilities in the config file.
        backgrounds = config["layers"][0]
        choice = random.choices(list(backgrounds["values"].keys()), backgrounds["values"].values())[0]
        image["background"] = choice

    return all_images


def save_metadata(metadata_list):
    """Writes each dictionary in the input array to a separate file."""
    for idx, image in enumerate(metadata_list):
        padded_id = str(idx).zfill(PADDING_AMOUNT)
        token_metadata = deepcopy(METADATA_TEMPLATE)
        token_metadata["name"] = "#" + token_metadata["name"].replace("000", padded_id)
        for key in image:
            token_metadata["attributes"].append(
                {"trait_type": key.replace("-", " ").title(), "value": image[key].replace("-", " ").title()}
            )
        with open(f"assets/{padded_id}.json", "w") as outfile:
            json.dump(token_metadata, outfile, indent=4)


def create_assets_folder():
    """Creates a folder named 'assets' if it doesn't already exist."""
    if os.path.isdir("assets"):
        return
    os.mkdir("assets")


def generate_image(base_file, layer_files, output_file):
    """Create an image file composed of `base_file` with `layer_files` applied on top."""
    base = Image.open(base_file)

    for layer_file in layer_files:
        if "none.png" in layer_file:
            continue
        layer = Image.open(layer_file)
        base.paste(layer, (0, 0), layer)

    resized_img = base.resize((base.width * SCALE_FACTOR, base.height * SCALE_FACTOR), resample=Image.NEAREST)
    resized_img.save(output_file)


def generate_images(metadata_list):
    """Creates images based on metadata in `metadata_list`"""
    for idx, image in enumerate(metadata_list):
        padded_id = str(idx).zfill(PADDING_AMOUNT)
        base_file = f"trait-layers/background/{image['background']}.png"
        layer_files = [
            f"trait-layers/{attribute}/{image[attribute]}.png" for attribute in image if attribute != "background"
        ]
        generate_image(base_file, layer_files, f"assets/{padded_id}.png")


if __name__ == "__main__":
    create_assets_folder()
    metadata_list = generate_all_image_metadata()
    save_metadata(metadata_list)
    generate_images(metadata_list)

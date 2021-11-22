# Onigiri Town's Art Generation Tool (Open-Sourced)

Onigiri Town is a cozy community built on Solana. For more information, please see our [website](https://www.onigiritown.com/).

## Instructions

1. Create the directory structure

Have a `trait-layers` folder that contains one subfolder for each attribute type. For example, if you look at this project's [trait-layers](trait-layers/), you will see seven different subfolders:

- background
- cheeks
- eyes
- front
- headpiece
- mouth
- rice

2. Export each attribute to its subfolder

For example, each exported headpiece can be found in the [trait-layers/headpiece](trait-layers/headpiece) folder. In general, filenames should be kept lowercase, with any spaces replaced with hyphens (e.g. "Rainbow Hat" is saved as "rainbow-hat.png").

3. Update the configuration file with desired probabilities

The configuration file, [config.json](config.json), has the structure:

```json
{
    "layers": [
        {
            "name": "background",
            "values": {
                "beige": 20,
                "blue": 20,
                "brown": 20,
            }
        },
    ]
}
```

The `layers` array contains the configuration for each attribute. `name` is the attribute name (e.g. background, eyes, headpiece). `values` is a mapping between each attribute value and their weighted probability. These probabilities do not need to sum up to 100.

In this example, all NFTs will have either a beige, blue, or brown background. There's a 1/3 chance for it to be beige, another 1/3 chance for it to blue, etc. 

If sometimes you do not want any value for this attribute, you can use the keyword `none`.

Use [config.json](config.json) as a reference for a fully complete configuration file.

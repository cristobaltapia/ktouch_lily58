import argparse
import json
import os
import re
import uuid
import xml.etree.ElementTree as ET
from xml.dom import minidom

parser = argparse.ArgumentParser("Generate KTouch layout for Lily58")
parser.add_argument("--keyboard-config")
parser.add_argument("--layout")
parser.add_argument("--name", default="new_layout")

args = parser.parse_args()

KEYBOARD_CONFIG = args.keyboard_config
KEYBOARD_LAYOUT = args.layout
NAME = args.name

# Pattern to detect a special key
P = re.compile(r"m\((.+)\)")
# Pattern to extract type of special key
# Define size of the keys
KS = 80
# Define special key types
SK_TYPES = ["return", "tab", "space", "backspace", "shift"]
MODIFIERS = {"layer-2": "shift", "layer-3": "mod3", "layer-4": "mod4"}


def is_special_key(row: int, col: int, config: dict) -> bool:
    """Detect if the key should be considered as a 'special key'.

    Parameters
    ----------
    row : int
        Row number (starts from 0)
    col : int
        Column number (starts from 0)
    config : dict
        Configuration

    Returns
    -------
    bool :
        True if the key at (i,j) is a special key.

    """
    # Consider only the first layer
    curr_key = config["layer-1"][row][col]

    return bool(P.match(curr_key))


def process_configuration(config: dict) -> dict:
    """Process the configuration file.

    A dictionary of lists is created. Each key of the dictionary corresponds to
    a layer. Each layer defines a list for each row, and each list contains the
    corresponding character or special key of the key.

    Parameters
    ----------
    config : dict
        Configuration file read directly with the toml library.

    Returns
    -------
    proc_config : dict
        Processed configuration for the layout

    """
    layout = dict()
    for layer_i, layout_i in config.items():
        layer_proc = []
        for row in layout_i:
            proc_row = [k for x in row for k in x]
            layer_proc.append(proc_row)

        layout[layer_i] = layer_proc

    return layout


def gen_key(keys, coord: list, finger: int, haptic: bool = False, special: bool = False):
    """Add a new key to the XML tree at the given position with given properties.

    Parameters
    ----------
    keys :
        parent XML element
    pos : list
        List with coordinates [x,y] of the key.
    finger : int
        Index of the finger associated to the key.
    haptic: bool
        Whether the key has a haptic marker or not.
    special : bool
        Whether it is a special key.

    Returns
    -------
    ki :
        The XML element.

    """
    if special:
        ki = ET.SubElement(keys, "specialKey")
    else:
        ki = ET.SubElement(keys, "key")
        ki.set("fingerIndex", f"{finger}")

    if haptic:
        ki.set("hasHapticMarker", "true")

    ki.set("top", f"{coord[1]}")
    ki.set("left", f"{coord[0]}")
    ki.set("height", f"{KS}")
    ki.set("width", f"{KS}")

    return ki


def define_special_type(key, ki):
    mod = P.match(key).group(1)
    if mod in SK_TYPES:
        ki.set("type", mod)
    else:
        ki.set("type", "other")
        ki.set("modifierId", mod)
        ki.set("label", mod)


def main():
    # Create root element
    root = ET.Element("keyboardLayout")
    name = ET.SubElement(root, "id")
    name.text = f"{{{uuid.uuid4()}}}"
    name = ET.SubElement(root, "title")
    name.text = f"Lily58-{NAME}"
    name = ET.SubElement(root, "name")
    name.text = "de(noted)"
    width = ET.SubElement(root, "width")
    width.text = "1290"
    height = ET.SubElement(root, "height")
    height.text = "450"

    xml_keys = ET.SubElement(root, "keys")

    # Read the coordinates of the keys
    with open(KEYBOARD_CONFIG, "r") as f:
        kb_props = json.load(f)

    # Read the layout configuration
    with open(KEYBOARD_LAYOUT, "r") as f:
        layout = json.load(f)

    positions = {
        "layer-1": "bottomLeft",
        "layer-2": "topLeft",
        "layer-3": "bottomRight",
        "layer-4": "topRight",
    }
    # Process config file
    # Fill information for each key
    for i, row in enumerate(kb_props["coords"]):
        for j, pos_i in enumerate(row):
            # Add new key
            haptic = [i, j] in kb_props["haptic_marker"]
            finger = kb_props["fingers"][i][j]
            print(haptic)
            if is_special_key(i, j, layout):
                # Generate the key element in the XML tree
                ki = gen_key(xml_keys, pos_i, finger, haptic=haptic, special=True)
                # Get the name of the modifier key
                key = layout["layer-1"][i][j]
                define_special_type(key, ki)

            else:
                ki = gen_key(xml_keys, pos_i, finger, haptic=haptic, special=False)
                # Iterate over each defined layer
                for k, layer in layout.items():
                    # Get the actual char for the key
                    key = layer[i][j]
                    # Confirma that it is not a blank char
                    if len(key) >= 1:
                        ch = ET.SubElement(ki, "char")
                        ch.text = key
                        # Define position of the char within the key
                        ch.set("position", positions[k])
                        # Define the modifier that activates the key
                        if k in MODIFIERS.keys():
                            ch.set("modifier", MODIFIERS[k])

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent=" ")
    with open(f"Lily58_{NAME}.xml", "w") as f:
        f.write(xmlstr)


if __name__ == "__main__":
    main()

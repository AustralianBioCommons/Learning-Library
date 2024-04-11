"""
Adapted from https://github.com/elixir-europe/rdmkit/blob/master/var/conversions.py
"""

import pandas as pd
import yaml
import os

# --------- Variables ---------
google_id = "1fkilWZmnh3P7VLEvM01I7g9shLkGGTHoT2pHsZmaCmc"
gid = "0"
url = f"https://docs.google.com/spreadsheets/d/1uIBItELephFZNjC4UPoegQpo1pIzY15IjOgX8q33slU/edit#gid=0"
output_path = "_data/resource_list.yml"
rootdir = '../pages'
allowed_registries = ['biotools', 'fairsharing', 'tess', 'europmc']

# --------- Converting the table ---------

print(f"----> Converting google table to {output_path} started.")
resource_table = pd.read_csv(url, dtype={'name': str, 'url': str, 'description': str, 'id': str, 'fairsharing': str,
                                         'biotools': str, 'tess': str, 'europmc': pd.Int64Dtype()})
resource_list = resource_table.to_dict("records")
clean_resource_list = []
for resource in resource_list:
    registry_dict = {}
    for registry in allowed_registries:
        if not pd.isna(resource[registry]):
            registry_dict[registry] = resource[registry]
        del(resource[registry])
    clean_resource = {k: resource[k] for k in resource if not pd.isna(resource[k])}
    clean_resource_list.append(clean_resource)
    clean_resource['registry'] = registry_dict

print(os.getcwd())
with open(output_path, 'w+') as yaml_file:
    documents = yaml.dump(clean_resource_list, yaml_file)

print("----> YAML is dumped successfully")

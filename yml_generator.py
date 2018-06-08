#!/usr/bin/python

## pip install PyYAML
import yaml
from collections import OrderedDict
from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter


# a yaml converter keeping order
class Orderedyaml():
    def __init__(self):
        self._mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
        self.dumper = Dumper
        self.loader = Loader
        self.dumper.add_representer(OrderedDict, self.dict_representer)
        self.loader.add_constructor(self._mapping_tag, self.dict_constructor)
        self.dumper.add_representer(str,
                                    SafeRepresenter.represent_str)
        self.dumper.add_representer(unicode,
                                    SafeRepresenter.represent_unicode)
        self.dumper.add_representer(list,
                                    SafeRepresenter.represent_list)
        self.dumper.ignore_aliases = lambda *args: True

    def dict_representer(self, dumper, data):
        return dumper.represent_dict(data.iteritems())

    def dict_constructor(self, loader, node):
        return OrderedDict(loader.construct_pairs(node))


def add_deployments(prefixes, loader):
    # load sample data
    with open("./sample.yml") as f:
        sample_data = yaml.load(f, loader)

    drone_data = {'pipeline': OrderedDict()}

    # generate new data
    for prefix in prefixes:
        new_data = transverse_replacer(sample_data, prefix)
        drone_data['pipeline'].update(new_data['root-node'])

    return drone_data


def yml_generator(data, file_name, dumper):
    with open("./" + file_name, 'w') as f:
        yaml.dump(data, f, Dumper=dumper, default_flow_style=False)


def transverse_replacer(node, prefix):
    if isinstance(node, basestring):
        newnode = node
        for key, value in prefix.iteritems():
            if key in node:
                newnode = newnode.replace(key, value)
        return newnode
    elif isinstance(node, bool):
        return node
    elif isinstance(node, OrderedDict):
        new_node = OrderedDict()
        for key, value in node.items():
            keyreplace = False
            for k2, v2 in prefix.iteritems():
                if k2 in key:
                    newkey = key.replace(k2, v2)
                    new_node[newkey] = transverse_replacer(value, prefix)
                    keyreplace = True

            if not keyreplace:
                new_node[key] = transverse_replacer(value, prefix)
        return new_node
    else:
        new_node = []
        for i in range(len(node)):
            keyreplace = False
            for k2, v2 in prefix.iteritems():
                if k2 in node[i]:
                    new_node.append(node[i].replace(k2, v2))
                    keyreplace = True
            if not keyreplace:
                new_node.append(node[i])
        return new_node


def main():
    prefixes = []
    prefixes.append(
        {"<prefix>": "staging", "<PREFIX>": "STAGING", "<namespace>": "core-product-developers-staging-east",
         "<environment>": "staging", "<region>": "us-east4", "<branch>": "staging",
         "<prefix-deploy>": "staging"})

    prefixes.append(
        {"<prefix>": "prod_east", "<PREFIX>": "PROD_EAST", "<namespace>": "core-product-developers-production-east",
         "<environment>": "production", "<region>": "us-east4", "<branch>": "master",
         "<prefix-deploy>": "prod-east"})

    prefixes.append(
        {"<prefix>": "prod_west", "<PREFIX>": "PROD_WEST", "<namespace>": "core-product-developers-production-west",
         "<environment>": "production", "<region>": "us-west1", "<branch>": "master",
         "<prefix-deploy>": "prod-west"})

    yaml_maker = Orderedyaml()

    data = add_deployments(prefixes, yaml_maker.loader)

    yml_generator(data, "deploy-all.yml", yaml_maker.dumper)


if __name__ == "__main__":
    main()

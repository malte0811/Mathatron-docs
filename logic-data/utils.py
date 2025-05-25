from dataclasses import dataclass
import os
import json

def load_dotname_to_base(data_dir):
    data = dict()
    with open(f'{data_dir}/nets.txt', 'r') as f:
        for line in f:
            if 'empty' in line:
                continue
            (dotname, base_str) = line.split(' ')
            if base_str[0] == '?':
                continue
            data[dotname] = int(base_str)
    return data

def load_special_ccs(data_dir, base_lookup):
    next_auto_id = 0
    to_component = dict()
    with open(f'{data_dir}/special-ccs.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if '.' in parts[-1]:
                component_name = 'special'+str(next_auto_id)
                next_auto_id += 1
            else:
                component_name = parts[-1]
                if component_name.startswith('base('):
                    component_name = base_lookup(int(component_name[5:-1]))
                parts = parts[:-1]
            for dot in parts:
                to_component[dot] = component_name
    return to_component

def load_names(data_dir):
    data = dict()
    with open(f'{data_dir}/names.txt', 'r') as f:
        for line in f:
            bjt, name = line.split('=')
            data[int(bjt)] = name.strip()
    return data


@dataclass
class ExtraComponentType:
    name_prefix: str
    line_suffix: str
    pins: list[list[str]]

def load_extra_components(data_dir):
    data: list[ExtraComponentType] = []
    try:
        with open(os.path.join(data_dir, 'components.json')) as f:
            json_data = json.load(f)
    except:
        return data
    for element in json_data:
        data.append(ExtraComponentType(element['namePrefix'], element['lineSuffix'], element['connections']))
    return data


class ColumnData:
    def __init__(self, from_dir):
        self.bjt_names = load_names(from_dir)
        self.dotname_to_base = load_dotname_to_base(from_dir)
        self.components: list[ExtraComponentType] = load_extra_components(from_dir)
        self.ccomp_overrides = load_special_ccs(from_dir, lambda i: self.base(i))

    def bjt_name(self, i, upper_case = True):
        if i in self.bjt_names:
            name = self.bjt_names[i]
            return name[0].upper() + name[1:]
        else:
            return str(i)

    def collector(self, i, spice=True):
        if i in self.bjt_names:
            return self.bjt_names[i]
        elif spice:
            return f'collector{i}'
        else:
            return str(i)

    def base(self, i):
        return f'base{self.bjt_name(i)}'

    def dot_resistor_bottom(self, dotname, spice=True):
        if dotname in self.ccomp_overrides:
            return self.ccomp_overrides[dotname]
        else:
            bjt = int(dotname[:dotname.index('.')])
            return self.collector(bjt, spice)


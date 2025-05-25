import sys
from collections import Counter
from utils import ColumnData

pnp_name = 'mathatron_pnp'
positive_rail = 'vplus'
negative_rail = 'vneg'
data = ColumnData(sys.argv[1])

def write_preambel():
    print('.title logic segment')
    print('.include constants.spice')

def write_bjt(i):
    print(f'Q{data.bjt_name(i)} {data.collector(i)} {data.base(i)} 0 0 {pnp_name}')
    print(f'Rbase{data.bjt_name(i)} {positive_rail} {data.base(i)} 100k')
    print(f'Rcoll{data.bjt_name(i)} {negative_rail} {data.collector(i)} 2.2k')

write_preambel()

for i in range(1, 41):
    write_bjt(i)

for dotname, bjt in data.dotname_to_base.items():
    print(f'Rdot{dotname} {data.base(bjt)} {data.dot_resistor_bottom(dotname)} 12k')

prefix_index: Counter[str] = Counter()
for component in data.components:
    for pins in component.pins:
        component_id = prefix_index[component.name_prefix]
        prefix_index[component.name_prefix] += 1
        pin_names = [data.dot_resistor_bottom(pin) for pin in pins]
        pins_string = ' '.join(pin_names)
        print(f'{component.name_prefix}{component_id} {pins_string} {component.line_suffix}')

print('.end')

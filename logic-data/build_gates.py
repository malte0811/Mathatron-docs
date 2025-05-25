import sys
from utils import ColumnData

data = ColumnData(sys.argv[1])

bjt_ids = range(1, 41)

inputs = [[] for _ in bjt_ids]
inputs.append([])
for dotname, bjt in data.dotname_to_base.items():
    inputs[bjt].append(data.dot_resistor_bottom(dotname, False))

for i in bjt_ids:
    print(f'{data.bjt_name(i, False)} = NOR[{", ".join(inputs[i])}]')

# TODO handle capacitive coupling

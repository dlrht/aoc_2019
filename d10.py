from pathlib import Path


data = list(map(str, (Path(__file__).parent / 'd10_input.txt').read_text().split('\n')))  # Rose this is SO smooth, dang
print(data)
print(data[0])
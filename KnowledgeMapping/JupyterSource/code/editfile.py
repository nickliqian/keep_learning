import json

with open("D:\\A\\jup\\1.ipynb", "r") as f:
    p = f.read()
    print(p)
cell = json.loads(p)

obj = {
    "cell_type": "code",
    "execution_count": "null",
    "metadata": {},
    "outputs": [],
    "source": [
        "1234567\n",
        "qwertyuio\n",
        "asdfghjkl"
    ]
}
cell["cells"].insert(0, obj)

result = json.dumps(cell, ensure_ascii=False).replace('"null"', 'null')
print(result)

with open("D:\\A\\jup\\1.ipynb", "w") as f:
    f.write(result)

import re


with open("./notebook.js", "r") as f:
    rl = f.read()



r = re.findall(r"(Notebook\.prototype.*?)\s{", rl)


for i in r:
    print(i)
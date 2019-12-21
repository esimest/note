with open('README.md', 'r', encoding='utf-8') as fp:
    lines = fp.readlines()

with open('README.md', 'w', encoding='utf-8') as fp:
    for line in lines[:]:
        if line.startswith('#'):
            fp.write(line + '\n')
            lines.remove(line)
        elif line == '\n':
            lines.remove(line)

    lines.sort(key=lambda x: len(x))

    for index, line in enumerate(lines):
        fp.write(line)
        if len(lines) -1 != index:
            fp.write('\n')

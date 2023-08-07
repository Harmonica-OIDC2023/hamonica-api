migration = ["from fdk import response\n"]

with open('./func_knative.py', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if 'def main(' in line:
            start = line.find("(")
            end = line.find(")")
            line = line.replace(line[start+1:end], "ctx, data")
        migration.append(line)

with open('./func.py', 'w') as file:
    file.writelines(migration)

migration_requirements = []

with open('./requirements_knative.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if "\n" not in line:
            line = line + "\n"
        migration_requirements.append(line)

with open('./requirements.txt', 'w') as file:
    file.writelines(migration_requirements)
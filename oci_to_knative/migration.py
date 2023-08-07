migration = ["from parliament import Context\n"]

with open('./func_oci.py', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if 'def main(' in line:
            start = line.find("(")
            end = line.find(")")
            line = line.replace(line[start+1:end], "context")
        migration.append(line)

with open('./func.py', 'w') as file:
    file.writelines(migration)

migration_requirements = []

with open('./requirements_oci.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if "\n" not in line:
            line = line + "\n"
        migration_requirements.append(line)

migration_requirements.append("parliament-functions")

with open('./requirements.txt', 'w') as file:
    file.writelines(migration_requirements)
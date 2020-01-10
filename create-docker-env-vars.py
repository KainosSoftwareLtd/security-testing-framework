# The purpose of this script is to create the docker environment file environment_variables_docker.env.
# The contents of environment_variables.sh are copied and converted to Docker format.


def convert_export(line):
    space_index = line.index(' ')
    new_line = line[space_index + 1: len(line)]
    return new_line


def convert_line(line):
    converted_line = ''

    if line.startswith('#!'):
        converted_line = None
    elif line.startswith('export'):
        converted_line = convert_export(line)
    elif line.startswith('#') or line.startswith('\n'):
        converted_line = line
    else:
        converted_line = None

    return converted_line


# Process environment file
converted_lines = list()
env_file = open('environment_variables.sh')
line = env_file.readline()
while line:
    converted_line = convert_line(line)
    if converted_line is not None:
        converted_lines.append(converted_line)
    line = env_file.readline()

# Write new file
docker_env_file = open('environment_variables_docker.env', 'w')
docker_env_file.writelines(converted_lines)
print('Written environment_variables_docker.env')

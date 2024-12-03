import glob
import fileinput
import yaml
import os

# Load settings from settings.yml
with open('settings.yml', 'r') as file:
    settings = yaml.safe_load(file)

# Get color settings
colors = settings['colors']

# Get all .svelte files in client/src directory and subdirectories
svelte_files = glob.glob('client/src/**/*.svelte', recursive=True)

def replace_to_color():
    # Replace text in each .svelte file
    for filename in svelte_files:
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                for color, value in colors.items():
                    line = line.replace(f'[[color:{color}]]', value)
                print(line, end='')

def return_to_original():
    # Return the original text in each .svelte file
    for filename in svelte_files:
        with fileinput.FileInput(filename, inplace=True) as file:
            for line in file:
                for color, value in colors.items():
                    line = line.replace(value, f'[[color:{color}]]')
                print(line, end='')
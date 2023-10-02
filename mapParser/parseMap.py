import re

WORDLIST = [ "item_objectivefailed", "item_objectivecomplete",
            "speaker", "monster", "item", "ammo", "armor"]

def process_map_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    inside_object = False
    comment_lines = False

    with open(output_file, 'w') as f:
        for line in lines:
            if '{' in line:
                inside_object = True
                comment_lines = False
            elif '}' in line:
                inside_object = False

            if inside_object and 'classname' in line:
                # Extracting the classname value
                match = re.search(r'"classname"\s+"([^"]+)"', line)
                if match and match.group(1) in WORDLIST:
                    # Commenting out the line
                    f.write(line)
                    comment_lines = True
                    continue
                else:
                    comment_lines = False

            if comment_lines and '}' not in line:
                # Commenting out all lines within the object after 'classname'
                line = "//" + line

            f.write(line)

            
if __name__ == "__main__":
    input_file = "walker.map"
    output_file = "walker_parsed.map"
    process_map_file(input_file, output_file)

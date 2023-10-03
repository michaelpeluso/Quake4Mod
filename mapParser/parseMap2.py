import re

WORDLIST = [ "item_objectivefailed", "item_objectivecomplete",
            "speaker", "monster", "item", "weapon", "ammo", "armor",
             "radiochatter", "vehicle_walker"]

def process_map_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    inside_object = False
    comment_lines = False

    with open(output_file, 'w') as f:
        for i, line in enumerate(lines):
            if '{' in line:
                inside_object = True
                comment_lines = False
                
                classname_line = None
                for j in range(i + 1, min(i + 10, len(lines))):  # Look ahead for at most 10 lines
                    if 'classname' in lines[j]:
                        match = re.search(r'"classname"\s+"([^"]+)"', lines[j])
                        if match and any(word in match.group(1) for word in WORDLIST):
                            comment_lines = True
                            break  # Corrected indentation to break the loop here

            elif '}' in line:
                if comment_lines :
                    f.write('//' + line)
                    continue
                inside_object = False

            if inside_object and comment_lines and '//' not in line:
                # Commenting out all lines within the object after 'classname'
                line = "//" + line

            f.write(line)

if __name__ == "__main__":
    input_file = "walker.map"
    output_file = "walker_parsed.map"
    process_map_file(input_file, output_file)

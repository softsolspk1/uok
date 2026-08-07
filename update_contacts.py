import os

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    modified = False
    for i, line in enumerate(lines):
        if "Acting Vice Chancellor" in line:
            lines[i] = line.replace("Acting Vice Chancellor", "Vice Chancellor")
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Successfully updated {filepath}")
    else:
        print(f"Could not find 'Acting Vice Chancellor' in {filepath}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    contacts_path = os.path.join(base_dir, 'pages_raw', 'contacts.html')
    replace_in_file(contacts_path)

if __name__ == '__main__':
    main()

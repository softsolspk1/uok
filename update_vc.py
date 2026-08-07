import os

def replace_in_file(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Could not find exact text in {filepath}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    vc_path = os.path.join(base_dir, 'pages_raw', 'vc.html')
    contacts_path = os.path.join(base_dir, 'pages_raw', 'contacts.html')
    
    # In pages_raw/vc.html
    replace_in_file(vc_path, 
                    "Acting Vice Chancellor, University of Karachi", 
                    "Vice Chancellor, University of Karachi")
                    
    # In pages_raw/contacts.html
    replace_in_file(contacts_path,
                    "Prof. Dr. Muhammad Tufail<br />\n      Acting Vice Chancellor",
                    "Prof. Dr. Muhammad Tufail<br />\n      Vice Chancellor")
                    
    # Also try without the line break just in case
    replace_in_file(contacts_path,
                    "Prof. Dr. Muhammad Tufail<br />\r\n      Acting Vice Chancellor",
                    "Prof. Dr. Muhammad Tufail<br />\r\n      Vice Chancellor")

if __name__ == '__main__':
    main()

import os
import json

def forward_slash(file_path: str):
    '''
    '''
    
    if '\\' not in file_path:
        return file_path
    
    file_path = file_path.replace('\\', '/')
    
    return file_path

def find_package_path(package_name: str):
    """
    """
    
    current_path = os.path.abspath(__file__)
    
    while current_path:
        current_dir, dirname = os.path.split(current_path)
        if dirname == package_name:
            return current_path
        
        current_path = current_dir
        
def get_list(json_file: str, key: str):
    """
    """
    
    with open(json_file, 'r') as file:
        style_dict = json.load(file)
    
    styles_list = style_dict[key]
        
    return styles_list

def get_current(json_file: str, key: str):
    """
    """
    
    with open(json_file, 'r') as file:
        style_dict = json.load(file)
    current_style = style_dict[key]
    return current_style

def change_current(json_file: str,json_current_dict_name: str,json_other_dict_name: str, new_current_name: str):
    """
    exemple:  change_current(PROJECT_JSON_PATH,"current_project","projects",current_project)

    """
    try:
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Update the "current_project" key
        # first get the new_current_project_name data:
        new_current_project_data=data[json_other_dict_name][new_current_name]
        # then
        data[json_current_dict_name] = {new_current_name: new_current_project_data}
        
        # Write the updated JSON back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"{json_current_dict_name} set to '{new_current_name}'")
    except FileNotFoundError:
        print(f"File '{json_file}' not found.")
    except KeyError:
        print(f"Project '{new_current_name}' not found in the '{json_other_dict_name}' dictionary.")

def format_size(size_bytes):
    # Liste des suffixes pour les unités de taille
    suffixes = ['o', 'Ko', 'Mo', 'Go', 'To', 'Po', 'Eo', 'Zo', 'Yo']
    
    # Si la taille est égale à 0, retournez directement "0 B"
    if size_bytes == 0:
        return "0 o"
    
    # Calcul du nombre d'unités de taille
    i = 0
    while size_bytes >= 1024 and i < len(suffixes)-1:
        size_bytes /= 1024.0
        i += 1
    
    # Formate la taille avec le suffixe approprié
    size_formatted = "{:.2f} {}".format(size_bytes, suffixes[i])
    
    return size_formatted

def get_size(path):
    
    return format_size(os.path.getsize(path))

def add_text_to_line_edit(line_edit_name,text):
    line_edit_name.setText(text)

def set_style_sheet(window,style,palette_path):

    palette = read_json_file(palette_path)
    style_path = style 

    with open(style_path, "r") as file:
        style_sheet = file.read()
    style_sheet = style_sheet.replace("MAIN_COLOR", palette["MAIN_COLOR"])
    style_sheet = style_sheet.replace("SECONDARY_COLOR", palette["SECONDARY_COLOR"])
    style_sheet = style_sheet.replace("TERTEARY_COLOR", palette["TERTEARY_COLOR"])
    style_sheet = style_sheet.replace("CUTE_COLOR", palette["CUTE_COLOR"])
    style_sheet = style_sheet.replace("COLOR_4", palette["COLOR_4"])
    style_sheet = style_sheet.replace("BORDER_SIZE", palette["BORDER_SIZE"])
    style_sheet = style_sheet.replace("BORDER_RADIUS", palette["BORDER_RADIUS"])

    window.setStyleSheet(style_sheet)

def read_json_file(json_file_path):
    """This function read a json file and return all his variables"""

    with open(json_file_path, "r") as json_file:
        config = json.load(json_file)
    return config

def write_json_file(json_file_path,variable_name,variable):
        """This function apply the dictionary with all the variable to a json file"""

        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        data[variable_name] = variable

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file)

if __name__ == '__main__':
    
    pass

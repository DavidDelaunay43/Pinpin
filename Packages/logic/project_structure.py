import os

class ProjectStructure(dict):
    """
    """
    
    def __init__(self, project_directory: str):
        project_structure = self._generate_project_structure(project_directory)
        self.update(project_structure)
        
        self.parent_directory = os.path.dirname(project_directory)
        
    def _generate_project_structure(self, root_directory: str):
        project_structure = {}
        
        for root, dirs, files in os.walk(root_directory):
            if root == root_directory:
                continue
            
            current = project_structure
            path = os.path.relpath(root, root_directory).split(os.path.sep)
            
            for folder in path:
                current = current.setdefault(folder, {})
            
            for file in files:
                current[file] = "file"
        
        project_name = os.path.basename(root_directory)
        return {project_name: project_structure}

    def extract_keys(self, directory: str):
        """
        """
        
        keys = []
        
        def recursive_extract(arg):
            for key, value in arg.items():
                if directory in key:
                    keys.extend(value.keys())
                elif isinstance(value, dict):
                    recursive_extract(value)
                    
        recursive_extract(self)
        return keys
    
    def get_dict_value(self, directory: str):
        """
        """
        
        output = []
        
        def return_parent_dir_value(arg):
            for key, value in arg.items():
                if directory in key:
                    output.append(arg.get(directory))
                elif isinstance(value, dict):
                    return_parent_dir_value(value)
        
        return_parent_dir_value(self)            
        return output[0]
    
    def extract_keys_02(self, parent_directory: str, directory: str):
        """
        """
        
        keys = []
        
        dict_to_inspect = self.get_dict_value(parent_directory)
        print(f'Dicto to inspect : {dict_to_inspect}')
        def recursive_extract(arg):
            for key, value in arg.items():
                if directory in key:
                    keys.extend(value.keys())
                elif isinstance(value, dict):
                    recursive_extract(value)
                    
        recursive_extract(dict_to_inspect)
        return keys
    
    def extract_keys_03(self, parent_directory: str, directory: str, subdir: str):
        """
        """
        
        keys = []
        
        dict_to_inspect = self.get_dict_value(parent_directory)
        dict_to_inspect = dict_to_inspect[directory]
        
        def recursive_extract(arg):
            for key, value in arg.items():
                if subdir in key:
                    keys.extend(value.keys())
                elif isinstance(value, dict):
                    recursive_extract(value)
                    
        recursive_extract(dict_to_inspect)
        return keys
    
if __name__ == '__main__':
    
    # Exemple d'utilisation :
    import json
    
    root_directory = r"E:\__Esma_pipeline\SERVEUR\Coup de Soleil"
    project_structure = ProjectStructure(root_directory)
    #print(json.dumps(project_structure, indent=4))
    
    print(project_structure.extract_keys_03("petru", "maya", "edit"))
import tkinter as tk
from tkinter import filedialog
import os
import json
import html

# Predefined Lorem Ipsum text
Lorem_Ipsum_Text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

datosjson = {}


def select_folder():
    global datosjson
    folder_path = filedialog.askdirectory()
    if folder_path:
        print("Selected folder:", folder_path)
        folder_contents = list_files_recursive(folder_path)
        print("Folder contents (JSON):")
        archivodatosjson = open(folder_path+"/datos.json")
        datosjson = json.load(archivodatosjson)
        print(datosjson)
        print(datosjson['titulo'])
        generate_html(folder_path, folder_contents)

def list_files_recursive(folder, depth=0, encoding="utf-8"):
    contents = []
    for root, dirs, files in os.walk(folder):
        # Filter out directories starting with a dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        folder_structure = {"name": os.path.basename(root).split('-', 1)[-1].strip(), "depth": depth, "type": "Folder", "path": root}
        contents.append(folder_structure)
        
        # Check if 000-Explicación.acomment exists, if not, create it
        explicacion_acomment_path = os.path.join(root, "000-Explicación.acomment")
        if not os.path.exists(explicacion_acomment_path):
            try:
                with open(explicacion_acomment_path, "w", encoding=encoding) as explicacion_acomment_file:
                    explicacion_acomment_file.write(Lorem_Ipsum_Text)
            except Exception as e:
                print(f"Error creating 000-Explicación.acomment file for '{root}': {e}")
        
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            file_name_without_extension = file_name.rsplit('-', 1)[-1].strip()  # Remove initial numbering
            file_path = os.path.join(root, file)
            file_structure = {"name": file_name_without_extension, "depth": depth +1, "type": "File", "path": file_path}
            
            # Check if the file is not already a .acomment file and if a corresponding .acomment file exists, if not, create it
            print(file_name)
            if  not 'acomment' in file.lower():
                acomment_file_path = os.path.join(root, f"{file_name}.acomment{file_extension}")
                if not os.path.exists(acomment_file_path):
                    try:
                        with open(acomment_file_path, "w", encoding=encoding) as acomment_file:
                            acomment_file.write(Lorem_Ipsum_Text)
                    except Exception as e:
                        print(f"Error creating .acomment file for '{file_path}': {e}")
            
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    file_content = f.read()
                if file_extension == ".acomment":
                    file_structure["content"] = html.escape(file_content)  # Escaping HTML tags
                else:
                    file_structure["content"] = html.escape(file_content).replace('\n', '<br>')  # Escaping HTML tags and replacing newlines with <br>
            except UnicodeDecodeError:
                print(f"Error decoding file '{file_path}' with encoding '{encoding}'. Trying different encoding.")
                # Try different encodings if decoding fails
                encodings_to_try = ["utf-8", "latin-1", "cp1252"]  # Add more encodings as needed
                for alt_encoding in encodings_to_try:
                    try:
                        with open(file_path, "r", encoding=alt_encoding) as f:
                            file_content = f.read()
                        if file_extension == ".acomment":
                            file_structure["content"] = html.escape(file_content)  # Escaping HTML tags
                        else:
                            file_structure["content"] = html.escape(file_content).replace('\n', '<br>')  # Escaping HTML tags and replacing newlines with <br>
                        print(f"File '{file_path}' decoded successfully with encoding '{alt_encoding}'.")
                        break
                    except UnicodeDecodeError:
                        print(f"Failed to decode file '{file_path}' with encoding '{alt_encoding}'.")
                else:
                    print(f"All encodings failed for file '{file_path}'. Skipping.")
            except Exception as e:
                print(f"Error reading file '{file_path}': {e}")
            contents.append(file_structure)
        for directory in dirs:
            contents.extend(list_files_recursive(os.path.join(root, directory), depth + 1))
    return contents

def generate_html(folder_path, folder_contents):
    html_filename = "libros/"+os.path.basename(folder_path) + ".html"
    pre_html_content = read_file_content("pre.html")
    post_html_content = read_file_content("post.html")
    
    with open(html_filename, "w", encoding="utf-8") as html_file:
        # Write the pre-HTML content
        html_file.write(pre_html_content)

        html_file.write("<section><h1 class='titulo'>"+datosjson['titulo']+"</h1><h2 class='subtitulo'>"+datosjson['subtitulo']+"</h2><h3 class='autor'>"+datosjson['autor']+"</h3></section><header>"+datosjson['cabecera']+"</header><footer>"+datosjson['piedepagina']+"</footer>")
        
        
        # Generate Table of Contents
        html_file.write("<h1>Tabla de contenido</h1>\n")
        html_file.write("<nav>\n")
        for item in folder_contents:
            if item["type"] == "Folder":
                html_file.write("<h{}><a href='#{}'>{}</a></h{}>\n".format(min(item["depth"] + 1, 6)-1, item["name"], item["name"], min(item["depth"] + 1, 6)-1))
        html_file.write("</nav>\n")
        html_file.write("<section>\n")
        # Write the content of each item in the folder
        for item in folder_contents:
            #print(item)
            if item["type"] == "Folder":
                html_file.write("<h{} id='{}'>{}</h{}>\n".format(min(item["depth"] + 1, 6)-1, item["name"], item["name"], min(item["depth"] + 1, 6)-1))
            else:
                if "content" in item:
                    if "acomment" in item["path"]:  # Check if "acomment" is present in the filename
                        html_file.write("<p class='negrita'>{}</p>\n".format(item["name"]))
                        html_file.write("<p>{}</p>\n".format(item["content"]))  # Place content inside <p> tag for .acomment files
                    else:
                        html_file.write("<p class='archivo'><span class='boton rojo'></span><span class='boton amarillo'></span><span class='boton verde'></span>{}</p>\n".format(item["name"]))  # Place file name inside <p> tag for regular files
                        html_file.write("<pre>{}</pre>\n".format(item["content"]))  # Place content inside <pre> tag for regular files
        html_file.write("</section>")
        # Write the post-HTML content
        html_file.write(post_html_content)
    
    print("HTML file generated successfully.")

def read_file_content(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return ""

# Create the main window
root = tk.Tk() 
root.title("Folder Selector")

# Create a button to trigger folder selection
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()

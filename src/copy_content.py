import os
import shutil
from markdown_blocks import markdown_to_html_node

def clear_public():
    folders = os.listdir(".")
    for folder in folders:
        new_path = os.path.join(".", folder)
        if folder == "public":
            if os.path.exists(new_path):
                shutil.rmtree(new_path)
    os.mkdir("./public")

def copy_content(path = "./static"):
    if os.path.exists(path):
        paths = os.listdir(path)
        for new_path in paths:
            copy_path = os.path.join(path, new_path)
            target_path = copy_path.replace("./static", "./public")
            if os.path.exists(copy_path):
                if os.path.isfile(copy_path):                        
                    print(f"Copy file from: #{copy_path}# to #{target_path}#")
                    test_path = shutil.copy(copy_path, target_path)
                    print(f"path of copied file #{test_path}#")
                elif os.path.isdir(copy_path):
                    print(f"Make dir at #{target_path}#")
                    os.mkdir(target_path)
                    print(f"Enteri nto dir #{copy_path}#")
                    copy_content(copy_path)
            else:
                raise Exception(f"{copy_path} => Path do not exists") 
    else:
        raise Exception(f"{path} => Path do not exists")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("H1 was not founded")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path):
        f = open(from_path)
        from_value = f.read()
        f.close()
        if os.path.exists(template_path):
            template_f = open(template_path)
            tempalte_value = template_f.read()
            template_f.close()

            html_node = markdown_to_html_node(from_value)
            html_string = html_node.to_html()

            title = extract_title(from_value)

            tempalte_value = tempalte_value.replace('{{ Title }}', title)
            tempalte_value = tempalte_value.replace('{{ Content }}', html_string)
            
            #Creating file and directory if not exists
            if not os.path.exists(dest_path):
                path_lines = dest_path.split("/")
                test_path = ""
                for path_line in path_lines[:-1]:
                    test_path += path_line
                    if not os.path.exists(test_path):
                        os.mkdir(test_path)
                    test_path += "/"
            dest_f = open(dest_path, "w")
            dest_f.write(tempalte_value)
            dest_f.close()

        else:
            raise Exception(f"Template path does not exists: {template_path}")
    else:
        raise Exception(f"From path does not exists: {from_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(template_path):
            template_f = open(template_path)
            tempalte_value = template_f.read()
            template_f.close()

            if os.path.exists(dir_path_content):
                entries = os.listdir(dir_path_content)
                for entry in entries:
                    tmp_path = f"{dir_path_content}/{entry}"
                    tmp_dest_path = f"{ dest_dir_path}/{entry}"
                    #copy markdown value
                    if os.path.isfile(tmp_path):
                        print(f"Open file at: {tmp_path}")
                        new_f = open(tmp_path, "r")
                        new_value = new_f.read()
                        new_f.close()

                        html_node = markdown_to_html_node(new_value)
                        html_string = html_node.to_html()

                        title = extract_title(new_value)
                        new_template = tempalte_value.replace('{{ Title }}', title)
                        new_template = new_template.replace('{{ Content }}', html_string)

                        tmp_dest_path = tmp_dest_path.replace(".md", ".html")
                        print(f"Create/write file at: {tmp_dest_path}")
                        new_dest_f = open(tmp_dest_path, "w")
                        new_dest_f.write(new_template)
                        new_dest_f.close()
                    else:
                        print(f"Create dir at: {tmp_dest_path}")
                        os.mkdir(tmp_dest_path)
                        print(f"Enter into dir at: {tmp_path}")
                        generate_pages_recursive(tmp_path, template_path, tmp_dest_path)
            else:
                raise Exception(f"Dir Path Does not exists: {dir_path_content}")
    else:
        raise Exception(f"Template path does not exists: {template_path}")



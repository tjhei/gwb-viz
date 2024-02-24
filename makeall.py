import re
import os
import subprocess

glance_url = "https://f.tjhei.info/glance/"
online_location = "https://f.tjhei.info/gwb"

html_file = open('index.html', 'w')
html_file.write("<html><head><title>Processed Files</title></head><body><h1>Processed Files:</h1><ul>\n")

    
def process_all(directory='.'):
    files_to_process = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.grid'):
                grid_file_path = os.path.join(root, file)
                print(file)
                
                files_to_process.append([root,file])

    for x in files_to_process:
        [path,filename]=x
        convert(path,filename)

base = os.path.dirname(os.path.realpath(__file__))

def convert(path, filename):
    global html_content
    old = os.getcwd()
    basename = filename.replace(".grid","")
    
    wb = filename.replace(".grid",".wb")
    x_file_path = os.path.splitext(path+"/"+filename)[0] + '.vtkjs'

    path_clean = path[2:]
    
    print("processing ",path," ",filename)
    os.chdir(path)

    if not os.path.exists(wb):
        os.chdir(old)
        print("   skipping, as ",wb,"was not found.")
        return

    html_file.write(f"<li><a href=\"{glance_url}?name={basename}.vtkjs&url={online_location}/{path_clean}/{basename}.vtkjs\">{x_file_path}</a></li>\n")
    
    if os.path.exists(x_file_path) and \
       os.path.getmtime(x_file_path) > os.path.getmtime(path+"/"+wb) and \
       os.path.getmtime(x_file_path) > os.path.getmtime(path+"/"+filename):
        os.chdir(old)
        print("already up to date!")
        return
        

        
    command = ["gwb-grid",
               "--by-tag",
               "--filtered",
               wb,
               filename]
    print(command)
    subprocess.run(command, check=True)

    #infiles = [filename.replace(".grid",".filtered.vtu")]
    infiles = []
    pattern = re.compile(r'\.\d+\.vtu$')
    filename_without_ext = filename.replace(".grid",".")

    for file in os.listdir("."):
        if pattern.search(file) and file.startswith(filename_without_ext):
            infiles.append(file)
    
    out = filename.replace(".grid",".vtkjs")

    command = ["pvbatch",
               base+"/makevtkjs.py",
               out]
    command.extend(infiles)
    print(command)
    if (len(infiles)>0):
        subprocess.run(command, check=True)
    
    os.chdir(old)


if __name__ == "__main__":
    process_all()
    html_file.write("</ul></body></html>")


import os
from maya import cmds

def main(file_path):
    count = len(file_path.split('/')) - 2
    search_dir = file_path
    for i in range(count):
        search_dir = os.path.dirname(search_dir)
        work_space = search_dir + '/workspace.mel'
        if os.path.exists(work_space):
            cmds.workspace(search_dir + '/', o=True)
            result = '//Result: Set project to ', search_dir 
            break
    
    if result:
        print(result),
    else:
        print('//Result: Cant find Maya project'),
    
    if any(ext in file_path for ext in ['.mb', '.ma']):
        cmds.file(file_path, o=True, iv=True, f=True)

file_path = 'C:/Users/hoge/Documents/maya/projects/default/scenes/hoge_v0001.ma'
main(file_path)

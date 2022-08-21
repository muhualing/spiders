from multiprocessing.reduction import duplicate
import os
import hashlib
path_of_the_directory= os.path.join(os.getcwd(), "googleSpider")
print(path_of_the_directory)
md5_set = set()
duplicated_files = []
ext = ('.doc','.docx')
for root, dir, files in os.walk("docs"):
    for file in files:
        if file.endswith(ext):
            file_name = os.path.join(root, file)
            with open(file_name, 'rb') as file_to_check:
                # read contents of the file
                data = file_to_check.read()    
                # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
            if md5_returned in md5_set:
                duplicated_files.append(file_name)
            else:
                md5_set.add(md5_returned) 
        else:
            continue
for file in duplicated_files:
    print(file)

# for files in os.listdir(path_of_the_directory):
#     if files.endswith(ext):
#         print(files)
#     else:
#         continue
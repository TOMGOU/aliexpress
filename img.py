import os, time

def file_name(file_dir):   
  L={'file_name': [], 'url_name': []}  
  for root, dirs, files in os.walk(file_dir):
    for file in files:  
      if os.path.splitext(file)[1] == '.jpg':  
        L['url_name'].append(os.path.join(root, file))
        L['file_name'].append(os.path.splitext(file)[0]) 
  L['url_name'] = sorted(L['url_name'])
  return L

upload_imgs = file_name('/Users/dsc/Study/05_selenium/aliexpress/imgs')

# print(upload_imgs['url_name'])
# path_split_by_newline = ''
# for file_path in upload_imgs['url_name']:
#   new_path = '\n' + file_path
#   path_split_by_newline += new_path
# list = [a for file_path in upload_imgs['url_name']]
# path_split_by_newline = ''.join(file_path)
# print('\n'.join(upload_imgs['url_name']))

# print(sorted(upload_imgs['url_name']))

colors = ['1', '2', '3', '4']
# for index, cell in enumerate(colors):
#   time.sleep(2)
#   print(index + 1, cell)
 
for i in range(1, len(colors) + 1):
  print(i)

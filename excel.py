import openpyxl

# 打开文件
workbook = openpyxl.load_workbook('./example.xlsx')

# 选择工作表
worksheet = workbook['Sheet1']

# 第一行分析
# first = []
# for index, cell in enumerate(worksheet['A1:A40']):
#   print(cell[0].value, end="\n")
#   if cell[0].value:
#     first.append(index + 1)

# 读取标题
title = worksheet['B1'].value
print(title)

# 适用机型
models = worksheet['B2'].value
print(models)

# 读取颜色
colors = []
for index, cell in enumerate(worksheet['B3:B12']):
  color_cvalue = cell[0].value
  if color_cvalue is not None:
    print(color_cvalue, end="\n")
    colors.append(color_cvalue)

# 读取材质
materials = []
for index, cell in enumerate(worksheet['B13:B39']):
  material_value = cell[0].value
  if material_value is not None:
    print(material_value, end="\n")
    materials.append(material_value)

# 读取价格
price = worksheet['B40'].value
print(price)

# 读取库存
inventory = worksheet['B41'].value
print(inventory)

# 读取SKU
sku = worksheet['B42'].value
print(sku)

# 读取详描标题
detail_title = worksheet['B43'].value
print(detail_title)

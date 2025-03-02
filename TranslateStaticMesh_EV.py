import csv
import os

PrefabFileName = 'EvaluatedPrefabVariant_EV.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
PrefabFilePath = os.path.join(current_directory, PrefabFileName)
PrefabFileOutputPath = os.path.join(current_directory, 'TranslatedEvaluatedPrefabVariant_EV.csv')

# 定义字段名称替换规则
replacement_rules = {
    "Name Check": "命名检查",
    "Class Check": "分类检查",
    "Classification": "分类",
    "Referenced Check": "有效性检查",
    "Referenced Model Count": "使用到的FBX数量",
    "Referenced Model Count Check": "使用到的FBX数量为1个",
    "Hierarchy Check": "与引用FBX层级结构一致",
    "Hierarchy Transform Check": "每一个节点没有位移缩放",
    "Mesh Render Check": "材质球与Mesh检查",
    "Empty Mesh Filter Check": "Mesh是否有丢失",
    "Empty Mesh Render Check": "材质球是否有丢失",
    "Material Count": "使用材质球数量",
    "Shader Name": "使用到的Shader",
    "Referenced Model Path": "使用到的FBX路径",
    "Abs Path": "绝对路径",
}

with open(PrefabFilePath, mode = 'r', encoding = 'utf-8-sig') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    PrefabRows = list(CsvReader)
    Fieldnames = CsvReader.fieldnames

    modified_fieldnames = [replacement_rules.get(field, field) for field in Fieldnames]

with open(PrefabFileOutputPath, mode = 'w', newline = '', encoding = 'utf-8-sig') as CsvFile:
    CsvWriter = csv.DictWriter(CsvFile, fieldnames = modified_fieldnames)
    CsvWriter.writeheader()

    for row in PrefabRows:
        modified_row = {}
        for field in Fieldnames:
            new_field = replacement_rules.get(field, field)
            modified_row[new_field] = row[field]
        CsvWriter.writerow(modified_row)
import csv
import os

ModelFileName = 'EvaluatedStaticMesh_EV.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
ModelFilePath = os.path.join(current_directory, ModelFileName)
ModelFileOutputPath = os.path.join(current_directory, 'TranslatedEvaluatedStaticMesh_EV.csv.csv')

# 定义字段名称替换规则
replacement_rules = {
    "Name Check": "命名检查",
    "Class Check": "分类检查",
    "Classification": "分类",
    "Hierarchy Check Root": "根节点名",
    "Node Transform Check": "冻结变换检查",
    "LOD Count": "LOD 数量",
    "Decal Count": "贴花数量",
    "Collider Count": "碰撞数量",
    "LOD Mesh MaterialID Count": "LOD 材质球数量",
    "Decal Mesh MaterialID Count": "贴花材质球数量",
    "Invalid UV Count Check": "是否有无效的UV集",
    "UV1 Range": "UV1 范围",
    "Vertex Color Range": "顶点色范围",
    "LOD Triangles Count": "各级 LOD 的三角形数量",
    "Decal Triangles Count": "贴花的三角形数量",
    "Collider Triangles Count": "碰撞的三角形数量",
    "OBB Size": "旋转包围盒大小 (居中)",
    "AABB Size": "包围盒大小 (未居中)",
    "Abs Path": "绝对路径",
}

with open(ModelFilePath, mode = 'r', encoding = 'utf-8-sig') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    PrefabRows = list(CsvReader)
    Fieldnames = CsvReader.fieldnames

    modified_fieldnames = [replacement_rules.get(field, field) for field in Fieldnames]

with open(ModelFileOutputPath, mode = 'w', newline = '', encoding = 'utf-8-sig') as CsvFile:
    CsvWriter = csv.DictWriter(CsvFile, fieldnames = modified_fieldnames)
    CsvWriter.writeheader()

    for row in PrefabRows:
        modified_row = {}
        for field in Fieldnames:
            new_field = replacement_rules.get(field, field)
            modified_row[new_field] = row[field]
        CsvWriter.writerow(modified_row)
import csv
import os

PrefabFileName = 'EvaluatedPrefabVariant_EV.csv'
ModelFileName = 'EvaluatedStaticMesh_EV.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
PrefabFilePath = os.path.join(current_directory, PrefabFileName)
ModelFilePath = os.path.join(current_directory, ModelFileName)
PrefabFileOutputPath = os.path.join(current_directory, 'EvaluatedPrefabVariant_EV_FinalChecked.csv')


with open(PrefabFilePath, mode='r', encoding='utf-8') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    PrefabRows = list(CsvReader)
    Fieldnames = CsvReader.fieldnames

with open(ModelFilePath, mode='r', encoding='utf-8') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    ModelRows = list(CsvReader)

for PrefabRow in PrefabRows:
    PrefabRow["\ufeffFinal Check"] = 'Failed'
    PrefabPath = PrefabRow['Referenced Model Path']
    PrefabFinalCheckResult = True
    PrefabFinalCheckResult &= PrefabRow['Name Check'] == "Passed"
    PrefabFinalCheckResult &= PrefabRow['Referenced Check'] == "Passed"
    PrefabFinalCheckResult &= PrefabRow['Referenced Model Count Check'] == "Passed"
    PrefabFinalCheckResult &= PrefabRow['Hierarchy Check'] == "Passed"
    PrefabFinalCheckResult &= PrefabRow['Empty Mesh Filter Check'] == "Passed"
    PrefabFinalCheckResult &= PrefabRow['Empty Mesh Render Check'] == "Passed"
    PrefabRow["Prefab Variant Check"] = 'Passed' if PrefabFinalCheckResult else 'Failed'

    if PrefabFinalCheckResult:
        ReferencedModelRow = None
        for ModelRow in ModelRows:
            ModelAbsPath = ModelRow['Abs Path']
            AssetsIndex = ModelAbsPath.find("Assets")
            ModifiedModelAbsPath = ModelAbsPath[AssetsIndex:]
            if ModifiedModelAbsPath == PrefabPath:
                ReferencedModelRow = ModelRow
        if ReferencedModelRow is not None:
            ReferencedModelFinalCheckResult = True
            ReferencedModelFinalCheckResult &= ReferencedModelRow['Name Check'] == "Passed"
            ReferencedModelFinalCheckResult &= ReferencedModelRow['Hierarchy Check'] == "Passed"
            ReferencedModelFinalCheckResult &= ReferencedModelRow['Hierarchy Root Name Check'] == "Passed"
            PrefabRow["\ufeffFinal Check"] = 'Passed' if ReferencedModelFinalCheckResult else 'Failed'


with open(PrefabFileOutputPath, mode='w', newline='', encoding='utf-8') as CsvFile:
    CsvWriter = csv.DictWriter(CsvFile, fieldnames=Fieldnames)
    CsvWriter.writeheader()
    CsvWriter.writerows(PrefabRows)
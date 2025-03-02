import csv
import os

PrefabFileName = 'EvaluatedPrefabVariant_EV.csv'
ModelFileName = 'EvaluatedStaticMesh_EV.csv'
current_directory = os.path.dirname(os.path.abspath(__file__))
PrefabFilePath = os.path.join(current_directory, PrefabFileName)
ModelFilePath = os.path.join(current_directory, ModelFileName)
PrefabFileOutputPath = os.path.join(current_directory, 'EvaluatedPrefabVariant_EV_ModelChecked.csv')


with open(PrefabFilePath, mode='r', encoding='utf-8') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    PrefabRows = list(CsvReader)
    Fieldnames = CsvReader.fieldnames

with open(ModelFilePath, mode='r', encoding='utf-8') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    ModelRows = list(CsvReader)

for PrefabRow in PrefabRows:
    if PrefabRow['Result'] == "Passed":
        ReferencedModelPath = PrefabRow['Referenced Model Path']
        ModelCheckResult = "N/A"
        for ModelRow in ModelRows:
            if ModelRow['Abs Path'] == ReferencedModelPath:
                ModelCheckResult = ModelRow['Result']
        if ModelCheckResult == "N/A":
            ModelCheckResult = ModelCheckResult
        PrefabRow["Final Check"] = ModelCheckResult
    else:
        PrefabRow["Final Check"] = "Failed"


with open(PrefabFileOutputPath, mode='w', newline='', encoding='utf-8') as CsvFile:
    CsvWriter = csv.DictWriter(CsvFile, fieldnames=Fieldnames)
    CsvWriter.writeheader()
    CsvWriter.writerows(PrefabRows)
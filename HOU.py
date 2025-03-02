import csv
import os
import datetime
import hou

# String
CsvFilePath = 'D:/StaticMesh_EV.csv'
OutputFilePath = 'D:/StaticMesh_EV_HouChecked.csv'
InvalidString = 'N/A'
LogFilePath = f'D:/QP_Log/BatchStasticMeshChecker/BatchStasticMeshCheckerLog {datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.txt'

# Check Dir Validity
LogDir = os.path.dirname(LogFilePath)
if not os.path.exists(LogDir):
    os.makedirs(LogDir)

# Prepare Node
FileNode = hou.node('../file1')
StaticMeshCheckerNode = hou.node('../WorldXStasticMeshChecker1')
GlobalNode = hou.node('../Global').geometry()
LODNode = hou.node('../LOD').geometry()
DecalNode = hou.node('../Decal').geometry()
ColliderNode = hou.node('../Collider').geometry()
LOD0Node = hou.node('../LOD0').geometry()


# Functions-----------------------------------------------------------------------------------------------------------
def AddWaitTag(content):
    return content + ' Waits Houdini'


def CustomWrite(row, target, content):
    for Key, Value in row.items():
        Row[Key] = Value.replace(AddWaitTag(target), content)


# Read
with open(CsvFilePath, mode='r', encoding='utf-8') as CsvFile:
    CsvReader = csv.DictReader(CsvFile)
    Rows = list(CsvReader)
    Fieldnames = CsvReader.fieldnames

# Open log file
with open(LogFilePath, mode='w', encoding='utf-8') as LogFile:
    # Modify rows
    Index = 0
    for Row in Rows:
        LogFile.write('\n')
        Index += 1
        # Prepare Data
        FbxName = Row['\ufeffFBX Name']
        HierarchyCheck = Row['Hierarchy Check']
        AbsPath = Row['Abs Path']
        LogFile.write(f'Processing FBX: {FbxName} -> {Index}\n')
        # Hierarchy Root Name Check First
        HierarchyRootNameCheck = 0
        if HierarchyCheck == 'Passed':
            FileNode.parm('file').set(AbsPath)
            StaticMeshCheckerNode.parm('ModelName').set(FbxName)
            HierarchyRootNameCheck = GlobalNode.attribValue('HierarchyRootNameCheck')
        else:
            CustomWrite(Row, 'Hierarchy Root Name Check', InvalidString)
        if HierarchyRootNameCheck == 0:
            CustomWrite(Row, 'Hierarchy Root Name Check', 'Failed')
        else:
            CustomWrite(Row, 'Hierarchy Root Name Check', 'Passed')

        if HierarchyCheck == 'Passed' and HierarchyRootNameCheck > 0:
            # Fill Checker
            HierarchyCheckRoot = Row['Hierarchy Check Root'].replace('[', '').replace(']', '')
            LODCount = int(Row['LOD Count'])
            DecalCount = int(Row['Decal Count'])
            ColliderCount = int(Row['Collider Count'])

            StaticMeshCheckerNode.parm('HierarchyCheckRoot').set(HierarchyCheckRoot)
            StaticMeshCheckerNode.parm('LODCount').set(LODCount)
            StaticMeshCheckerNode.parm('DecalCount').set(DecalCount)
            StaticMeshCheckerNode.parm('ColliderCount').set(ColliderCount)
            # Get LOD Data
            LODMeshMaterialIDCount = ''
            for i in range(LODCount):
                c = LODNode.attribValue(f'LOD{i}_Materials')
                LODMeshMaterialIDCount += '[' + str(len(c)) + ']'
                LogFile.write(f'LOD{i} Materials: {c}\n')

            LODTrianglesCount = ''
            for i in range(LODCount):
                c = LODNode.attribValue(f'LOD{i}_TrianglesCount')
                LODTrianglesCount += '[' + str(c) + ']'
                LogFile.write(f'LOD{i} Triangles: {c}\n')

            InvalidUVCountCheck = 1
            for i in range(LODCount):
                c = LODNode.attribValue(f'LOD{i}_InvalidUVCountCheck')
                InvalidUVCountCheck *= c
            LogFile.write(f'InvalidUVCountCheck: {InvalidUVCountCheck}\n')

            UV1Range = LODNode.attribValue(f'LOD0_UV1_Range')
            LogFile.write(f'UV1 Range: {UV1Range}\n')
            # Get Decal Data
            DecalValidity = DecalNode.attribValue(f'Valid')
            DecalMeshMaterialIDCount = ''
            DecalTrianglesCount = ''
            if DecalValidity > 0.5:
                for i in range(DecalCount):
                    c = DecalNode.attribValue(f'Decal{i}_Materials')
                    DecalMeshMaterialIDCount += '[' + str(len(c)) + ']'
                    LogFile.write(f'Decal{i} Materials: {c}\n')

                for i in range(DecalCount):
                    c = DecalNode.attribValue(f'Decal{i}_TrianglesCount')
                    DecalTrianglesCount += '[' + str(c) + ']'
                    LogFile.write(f'Decal{i} Triangles: {c}\n')
            else:
                CustomWrite(Row, 'Decal Mesh MaterialID Count', InvalidString)
                CustomWrite(Row, 'Decal Triangles Count', InvalidString)
            # Get Collider Data
            ColliderValidity = ColliderNode.attribValue(f'Valid')
            ColliderTrianglesCount = 0
            if ColliderValidity > 0.5:
                ColliderTrianglesCount = ColliderNode.attribValue('ColliderTrianglesCount')
                LogFile.write(f'Collider Triangles Count: {ColliderTrianglesCount}\n')
            else:
                CustomWrite(Row, 'Collider Triangles Count', InvalidString)
            # Get Global Data
            OBBSize = GlobalNode.attribValue('OBBSize')
            LogFile.write(f'OBB Size: {OBBSize}\n')
            AABBSize = GlobalNode.attribValue('AABBSize')
            LogFile.write(f'AABB Size: {AABBSize}\n')
            # Get LOD0 Data
            VertexColor = LOD0Node.attribValue('VertexColor')
            LogFile.write(f'Vertex Color: {VertexColor}\n')

            # Write
            CustomWrite(Row, 'LOD Mesh MaterialID Count', LODMeshMaterialIDCount)
            CustomWrite(Row, 'LOD Triangles Count', LODTrianglesCount)
            CustomWrite(Row, 'Invalid UV Count Check', 'Passed' if InvalidUVCountCheck > 0.5 else 'Failed')
            CustomWrite(Row, 'UV1 Range', UV1Range)
            CustomWrite(Row, 'Decal Mesh MaterialID Count', DecalMeshMaterialIDCount)
            CustomWrite(Row, 'Decal Triangles Count', DecalTrianglesCount)
            CustomWrite(Row, 'Collider Triangles Count', str(ColliderTrianglesCount))
            CustomWrite(Row, 'OBB Size', str(OBBSize))
            CustomWrite(Row, 'AABB Size', str(AABBSize))
            CustomWrite(Row, 'Vertex Color', VertexColor)
        else:
            LogFile.write('Failed At <Hierarchy Check> Or <Hierarchy Root Name Check>\n')
            CustomWrite(Row, 'LOD Mesh MaterialID Count', InvalidString)
            CustomWrite(Row, 'Decal Mesh MaterialID Count', InvalidString)
            CustomWrite(Row, 'Invalid UV Count Check', InvalidString)
            CustomWrite(Row, 'UV1 Range', InvalidString)
            CustomWrite(Row, 'Vertex Color', InvalidString)
            CustomWrite(Row, 'LOD Triangles Count', InvalidString)
            CustomWrite(Row, 'Decal Triangles Count', InvalidString)
            CustomWrite(Row, 'Collider Triangles Count', InvalidString)
            CustomWrite(Row, 'OBB Size', InvalidString)
            CustomWrite(Row, 'AABB Size', InvalidString)

    # Save
    with open(OutputFilePath, mode='w', newline='', encoding='utf-8') as CsvFile:
        CsvWriter = csv.DictWriter(CsvFile, fieldnames=Fieldnames)
        CsvWriter.writeheader()
        CsvWriter.writerows(Rows)

    LogFile.write('\n')
    LogFile.write(f'CSV File Has Been Processed And Saved <{datetime.datetime.now()}>\n')

os._exit(0)
"""
Build a two-layer USDZ:
- model.usdc: the original 3D model (binary, compact)
- model.usda: wrapper with ARKit image anchoring schemas (text, tiny)
The USDA references the USDC via sublayers or references.
"""
from pxr import Usd, Sdf
import os, sys, re, zipfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORKSPACE = r'C:\Users\Admin\.qclaw\workspace-2dgx8snjc7h1av5j\arkit-demo'
MODEL_DIR = os.path.join(WORKSPACE, 'model')
SRC_USDZ = os.path.join(MODEL_DIR, 'test.usdz')
REF_IMG = os.path.join(MODEL_DIR, 'reference_image.png')
DST_USDZ = os.path.join(MODEL_DIR, 'test_image_anchored.usdz')

# Step 1: Extract model.usdc from original USDZ
print('Extracting model.usdc from source...')
with zipfile.ZipFile(SRC_USDZ, 'r') as zf:
    model_usdc_data = zf.read('model.usdc')
    other_files = {}
    for name in zf.namelist():
        if name != 'model.usdc':
            other_files[name] = zf.read(name)

print(f'model.usdc: {len(model_usdc_data)} bytes')
print(f'Other files: {list(other_files.keys())}')

# Step 2: Write model.usdc to temp file and inspect its structure
temp_usdc = os.path.join(MODEL_DIR, '_model.usdc')
with open(temp_usdc, 'wb') as f:
    f.write(model_usdc_data)

stage = Usd.Stage.Open(temp_usdc)
root = stage.GetDefaultPrim()
root_name = root.GetName()
print(f'Root prim name: {root_name}')

# Step 3: Build a USDA wrapper that:
# a) Sublayers the original model.usdc
# b) Adds ARKit image anchoring schemas to the root prim
# c) Adds ReferenceImage prim as a child

# Create the USDA text manually for maximum control
usda_content = f'''#usda 1.0
(
    defaultPrim = "{root_name}"
    subLayers = [
        @model.usdc@
    ]
)

over Xform "{root_name}" (
    apiSchemas = ["Preliminary_AnchoringAPI"]
){{
    custom token anchoringType = "image"

    def Xform "ReferenceImage" (
        apiSchemas = ["Preliminary_ReferenceImage"]
    ){{
        custom float physicalWidth = 0.1
        custom asset referenceImageName = @reference_image.png@
    }}
}}
'''

print(f'USDA wrapper size: {len(usda_content)} bytes')
print('USDA content:')
print(usda_content)

# Step 4: Verify the USDA wrapper works by opening it
usda_path = os.path.join(MODEL_DIR, '_wrapper.usda')
with open(usda_path, 'w', encoding='utf-8') as f:
    f.write(usda_content)

os.chdir(MODEL_DIR)
try:
    stage2 = Usd.Stage.Open(usda_path)
    root2 = stage2.GetDefaultPrim()
    at2 = root2.GetAttribute('anchoringType')
    rp2 = stage2.GetPrimAtPath(str(root2.GetPath()) + '/ReferenceImage')
    
    print(f'Wrapper verification:')
    print(f'  Root: {root2.GetPath()}, type: {root2.GetTypeName()}')
    print(f'  anchoringType: {at2.Get()}')
    
    if rp2.IsValid():
        rn2 = rp2.GetAttribute('referenceImageName')
        pw2 = rp2.GetAttribute('physicalWidth')
        print(f'  referenceImageName: {rn2.Get()}')
        print(f'  physicalWidth: {pw2.Get()}')
    else:
        print('  ReferenceImage: NOT FOUND')
    
    # Count total prims (should include all from sublayer + new ones)
    prim_count = len(list(stage2.Traverse()))
    print(f'  Total prims: {prim_count}')
    
except Exception as e:
    print(f'Wrapper verification FAILED: {e}')

# Step 5: Build USDZ
print('Building USDZ...')
with zipfile.ZipFile(DST_USDZ, 'w', zipfile.ZIP_STORED) as zf:
    # USDA wrapper as the root layer (first file)
    zf.writestr('model.usda', usda_content)
    # Original USDC as sublayer
    zf.writestr('model.usdc', model_usdc_data)
    # Reference image
    if os.path.exists(REF_IMG):
        zf.write(REF_IMG, 'reference_image.png')
    # Other assets (textures etc)
    for name, data in other_files.items():
        if name not in ['model.usdc', 'model.usda', 'reference_image.png']:
            zf.writestr(name, data)

print(f'USDZ created: {os.path.getsize(DST_USDZ)/1024/1024:.1f} MB')

# List contents
with zipfile.ZipFile(DST_USDZ, 'r') as zf:
    for info in zf.infolist():
        print(f'  {info.filename} ({info.file_size} bytes)')

# Step 6: Final verification - open the USDZ
try:
    stage3 = Usd.Stage.Open(DST_USDZ)
    root3 = stage3.GetDefaultPrim()
    at3 = root3.GetAttribute('anchoringType')
    rp3 = stage3.GetPrimAtPath(str(root3.GetPath()) + '/ReferenceImage')
    
    print(f'\nFinal verification:')
    print(f'  Root: {root3.GetPath()}, type: {root3.GetTypeName()}')
    print(f'  anchoringType: {at3.Get()}')
    
    if rp3.IsValid():
        rn3 = rp3.GetAttribute('referenceImageName')
        pw3 = rp3.GetAttribute('physicalWidth')
        print(f'  referenceImageName: {rn3.Get()}')
        print(f'  physicalWidth: {pw3.Get()}')
    else:
        print('  ReferenceImage: NOT FOUND')
    
    prim_count3 = len(list(stage3.Traverse()))
    print(f'  Total prims: {prim_count3}')
except Exception as e:
    print(f'Final verification FAILED: {e}')

# Cleanup
os.chdir(r'C:\Users\Admin')
os.remove(temp_usdc)
os.remove(usda_path)
print('Done!')

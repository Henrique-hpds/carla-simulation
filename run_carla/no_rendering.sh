cd ..
# Adiciona a variável de ambiente VK_ICD_FILENAMES
export VK_ICD_FILENAMES='/usr/share/vulkan/icd.d/nvidia_icd.json'

echo "VK_ICD_FILENAMES: $VK_ICD_FILENAMES"

pwd

cd PythonAPI/examples
python3.7 no_rendering_mode.py --no-rendering
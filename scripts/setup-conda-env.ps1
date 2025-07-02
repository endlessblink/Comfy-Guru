# PowerShell script to set up conda environment on Windows
$condaPath = "C:\pinokio\bin\miniconda"
$envName = "comfy-guru"
$projectPath = "D:\APPSNospaces\comfy-guru"

# Activate conda
& "$condaPath\Scripts\conda.exe" init powershell
& "$condaPath\Scripts\conda.exe" activate base

# Check if environment exists
$envList = & "$condaPath\Scripts\conda.exe" env list
if ($envList -notmatch $envName) {
    Write-Host "Creating conda environment '$envName'..."
    & "$condaPath\Scripts\conda.exe" env create -f "$projectPath\environment.yml"
}

# Activate the environment
& "$condaPath\Scripts\conda.exe" activate $envName

# Install fastmcp if not already installed
& python -m pip install fastmcp

Write-Host "Conda environment '$envName' is ready!"
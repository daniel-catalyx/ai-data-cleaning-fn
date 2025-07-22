@echo off
echo Deploying to Azure Function App...
func azure functionapp publish data-cleaning-fn --python --build local
if %errorlevel% neq 0 (
    echo Standard deployment failed, trying ZIP method...
    powershell -Command "Get-ChildItem -Path . -Exclude '.git*', '__pycache__*', '.vscode', 'node_modules', '*.zip' | Compress-Archive -DestinationPath deploy.zip -Force"
    az functionapp deployment source config-zip --resource-group catalyx-data-cleaning-rg --name data-cleaning-fn --src deploy.zip
    del deploy.zip
)
echo Deployment completed!
pause
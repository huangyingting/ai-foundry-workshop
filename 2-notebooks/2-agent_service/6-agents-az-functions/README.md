npm install -g azure-functions-core-tools@4

az functionapp create --resource-group <your-rg> --consumption-plan-location <region> --runtime python --functions-version 4 --name <your-func-app-name> --storage-account <your-storage-account> --os-type linux
  
func azure functionapp publish <your-func-app-name>

func azure functionapp logstream <your-func-app-name>
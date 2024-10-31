from mlflow.tracking import MlflowClient
from Utils.exceptions import NoModelException, ImpossibleIntegration
from Utils.utility import convertTime, extractInfoTags, title, clean
from Utils.utility import extratDatasetName, getPath, templateRender
from Utils.logger import Logger

import os, warnings
warnings.filterwarnings("ignore")

class ModelCardGenerator:
    def __init__(self):
        self.client = MlflowClient()
        self.output = Logger()
        

    def modelLineage(self):
        """
        Returns a list of models stored in MLflow's Model Registry. 
        It prefers versions marked with the alias "champion"; if none exist, 
        it returns the latest available version of each model.
        """
        
        modelRegistry = self.client.search_registered_models()
        
        modelsName = []
        for model in modelRegistry:
            modelsName.append(model.name)

        models = []
        for name in modelsName:
            latest = True
            modelVersions = self.client.search_model_versions(f"name='{name}'")
            for model in modelVersions:
                if "champion" in model.aliases:
                    models.append(model)
                    if not model.version == self.client.get_latest_versions(name)[0].version:
                        modelInfo = f"{model.name} {model.version}"
                        self.output.warning(f" {modelInfo}: Champion model is not the latest")
                    latest = False
            if latest:
                latestVersion = self.client.get_latest_versions(name)[0]
                models.append(latestVersion)

        return models


    def fetchData(self, model):
        """
        Trace information about an experiment tracked in the MLflow Tracking. 
        Once the corresponding run is obtained, retrieve the relevant information.
        """

        #get run_id from model
        runID = model.run_id

        if not runID:
            raise NoModelException()

        # Extract information through the run
        run = self.client.get_run(runID)
        name = model.name
        version = model.version
        
        params = run.data.params
        author = run.info.user_id
        metrics = run.data.metrics
        py, lib, libv = extractInfoTags(run.data.tags)
        startTime = convertTime(run.info.start_time)
        endTime = convertTime(run.info.end_time)
        datasetName = extratDatasetName(run.inputs.dataset_inputs)

        info = f"{name}_v{version}.md"
        if not params:
            self.output.warning(f"{info}: Missing parameters in Model Card generation")
        if not metrics:
            self.output.warning(f"{info}: Missing metrics in Model Card generation")
        if not datasetName:
            self.output.warning(f"{info}: Missing dataset information in Model Card generation")
        if "" in [author, py, lib, libv, startTime, endTime]:
            self.output.warning(f"{info}: Missing info in Model Card generation, check the Model Card for any details.")

        data = {
            "modelName": name,
            "version": version,
            "author": author,
            "modelType": name,
            "library": lib,
            "libraryVersion": libv,
            "pythonVersion": py,
            "datasetName": datasetName,
            "parameters": params,
            "startTime": startTime,
            "endTime": endTime,
            "evaluations": metrics,
        }

        return data


    def ModelCard(self, model, parsedInfo):
        """
        Create a model card by instantiating a predefined 
        template using the retrieved information.
        """
        
        try:
            data = self.fetchData(model)
        except NoModelException as e:
            self.output.error(f"Check if models exist: {str(e)}")
            return None

        instance = templateRender("modelCard_template.md", data)

        path, file = getPath(data)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as modelCard:
            modelCard.write(instance)
            self.output.log(f"Model Card {file} created")
        
        if parsedInfo:
            self.integrate(data, parsedInfo, path)
        
        return None
    
    
    def integrate(self, data, parsedInfo, path):
        """
        Integrate a Model Card immediately after it has been created.
        """
        
        modelName = data.get("modelName")

        if modelName in parsedInfo:
            for file in parsedInfo.get(modelName):
                with open(f"ModelCardsGenerator/Data/{file}", 'r') as part:
                    text = part.read()
                doc = {"title": title(file), "text": text}    
                instance = templateRender("_part.md", doc)
                
                with open(path, 'a') as modelCard:
                    modelCard.write(instance)
        else:
            model = f"{modelName}_v{data.get("version")}"
            self.output.error(f"Could not integrate {model}: check commands in main.md")

        return None


    def forceIntegrate(self, parsedInfo):
        """
        Integrate Model Cards if automated integration didn't work.
        If detect a Model Card already integreted discard changes.
        """

        directory = "ModelCards"
        
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            
            if os.path.isfile(path):
                with open(path, 'r') as modelcard:
                    intro = modelcard.readline()
                
                clean(path)
                model = intro.split("#")[1].split("-")[0].strip()
                if model in parsedInfo:
                    for file in parsedInfo.get(model):
                        with open(f"ModelCardsGenerator/Data/{file}", 'r') as part:
                            text = part.read()
                        doc = {"title": title(file), "text": text}    
                        instance = templateRender("_part.md", doc)
                        
                        with open(path, 'a') as modelCard:
                            modelCard.write(instance)
                            self.output.log(f"Model Card {model} integrated")
                else:
                    raise ImpossibleIntegration(f"Could not integrate {model}: check commands in main.md")
        return None


    def getOutput(self):
        return self.output
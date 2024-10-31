# KNN - v1
## General Information 
- Developed by: donat
- Model Type: KNN
- sklearn version: 1.5.2
- Python version: 3.12.7
## Training Details

- Dataset: brest_cancer.csv
- Parameters: 
    - `weights` uniform
    - `metric` euclidean
    - `algorithm` auto
    - `n_neighbors` 3
    
- Training started at: 08:57:34 2024-10-30
- Training ended at: 08:57:43 2024-10-30
## Evaluation
- `F1_micro score` 0.9649122807017544
- `Recall` 0.9649122807017544
- `F1_macro score` 0.9626596790042581
- `Accuracy` 0.9649122807017544
- `Precision` 0.9649122807017544
## Description
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum. Nulla facilisi. Fusce tincidunt, odio sit amet venenatis tincidunt, justo purus bibendum risus, eu semper urna nisl in libero. Proin euismod risus ac lectus bibendum, id accumsan quam tristique.
## Howtouse
```
trainAndLog(
    dataset = dataset,
    trainer = trainer,
    experimentName = experiment,
    datasetName = "brest_cancer.csv",
    modelName = "Lorem Ipsum",
    tags = {"dolor sit amet": "consectetur adipiscing elit"}
)
```

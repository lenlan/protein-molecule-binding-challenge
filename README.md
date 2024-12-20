# protein-molecule-binding-challenge
There are 3 Jupyter Notebooks:
- Data_Exploration_Preparation
- ML_Pipeline
- Run_Test_Set

# Data_Exploration_Preparation.ipynb
Table of Contents
- Import and inspect dataset
- Protein Embedding
    - Embed Uniprot IDs using ProtT5 model (prottrans_t5_xl_u50)

- Molecule Embedding
    - Get SMILES representation from PubChem
    - Convert SMILES to Embedding
        - RDKit for Morgan Fingerprints
        - Alternative option, using BERT model (not used in current solution)
- Preparing data for Machine Learning Pipeline
    - Normalizing and saving embedded data
 
# ML_Pipeline.ipynb
LGBM model gets trained on 80% of the data and performs as follows on the held out 20%:

- Best number of estimators: 215
- Mean Squared Error: 391223160770.29596
- R^2 Score: 0.1777882974932672

# Run_Test_Set.ipynb
A new test set can be loaded and predictions can be made using the trained model.

# Conclusion and Remarks:
An R² score of 0.177 is relatively low but indicates that the model is capturing some signal from the data. Further optimization and exploration are necessary to improve performance.

## Notes
Cross-validation should be conducted to validate and generalize this performance.
Additional analysis can determine whether using estimated or non-estimated KIBA scores impacts the model's performance.
## Potential Next Steps to Improve Performance
Feature Engineering
- Incorporate additional features such as Kd, Ki, and IC50 scores.
Enhanced Embeddings
Experiment with more informative embeddings, such as:
- PubChem10M_SMILES_BERT
- DeepChem
- AlphaFold embeddings
- ProtTrans
## Explore Advanced Models
Implement deep learning techniques, including:
- Graph Neural Networks (GNNs) for representing molecular and protein structures.
- End-to-end models for drug-target binding prediction, such as DeepAffinity.
By incorporating these strategies, the model's performance can likely be enhanced, leading to more robust predictions.
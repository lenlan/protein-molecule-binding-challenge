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

Best number of estimators: 215
Mean Squared Error: 391223160770.29596
R^2 Score: 0.1777882974932672

# Run_Test_Set.ipynb
A new test set can be loaded and predictions can be made using the trained model.

# Conclusion and Remarks:
An R^2 Score of 0.177 is pretty low but it does show the model is learning something. Further steps can be taken to improve the performance.

Notes:
Cross-validation should be performed to validate this performance.
More work can be done in examining whether training on estimated or non-estimated kiba scores makes a difference

Potential next steps to improve performance:
- Add Kd, Ki, and IC50 scores as features
- Use more sophisticated embbeddings which contain more information (e.g., PubChem10M_SMILES_BERT, DeepChem, AlphaFold embeddings, or ProtTrans)
- Use other drug-target binding affinity prediction tools:
    - Deep Learning with Graph Neural Networks (GNNs)
    - End-to-End Models for Binding Affinity (e.g., DeepAffinity)
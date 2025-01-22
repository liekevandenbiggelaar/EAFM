# EAFM
Exceptional Atrial Fibrillation Mining

## Data
Includes AF related ECG recordings extracted from PhysioNet.
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.

- CPSC 2021: 4th China Physiological Signal Challenge 2021
https://physionet.org/content/cpsc2021/1.0.0/
Wang, X., Ma, C., Zhang, X., Gao, H., Clifford, G. D., & Liu, C. (2021). Paroxysmal Atrial Fibrillation Events Detection from Dynamic ECG Recordings: The 4th China Physiological Signal Challenge 2021 (version 1.0.0). PhysioNet. https://doi.org/10.13026/ksya-qw89.

Training set 1 includes 730 records from 12 AF patients and 42 non-AF patients.
Training set 2 includes 706 records from 37 AF patients and 14 non-AF patients.
In total this comes to 1436 records from 49 AF patients and 56 non-AF patients (total of 105 patients).

## Run experiments
To run the experiments, run python main.py in the terminal. You can set your own parameters. The standard settings are based on the simulation from the paper.

If you are working with your own electronic health records or another descriptor dataset, the attribute types must be changed. This is done in Code/Beam_Search/preprocess.py.

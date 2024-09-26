# EAFM
Exceptional Atrial Fibrillation Mining

## Data: 
Includes several data sources with AF related ECG recordings, all extracted from PhysioNet.
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.

- CPSC 2021: 4th China Physiological Signal Challenge 2021
https://physionet.org/content/cpsc2021/1.0.0/
Wang, X., Ma, C., Zhang, X., Gao, H., Clifford, G. D., & Liu, C. (2021). Paroxysmal Atrial Fibrillation Events Detection from Dynamic ECG Recordings: The 4th China Physiological Signal Challenge 2021 (version 1.0.0). PhysioNet. https://doi.org/10.13026/ksya-qw89.

Training set 1 includes 730 records from 12 AF patients and 42 non-AF patients.
Training set 2 includes 706 records from 37 AF patients and 14 non-AF patients.
In total this comes to 1436 records from 49 AF patients and 56 non-AF patients (total of 105 patients).



- MIT-BIH Atrial Fibrillation Database -> Too little data?
Moody GB, Mark RG. A new method for detecting atrial fibrillation using R-R intervals. Computers in Cardiology. 10:227-230 (1983).

Includes 25 long-term ECG recordings of humans with Atrial Fibrillation. Each recording covers 10 hours sampled at 250 samples per second (bandwidth approximately 0.1 Hz to 40Hz).


- SHDB-AF: a Japanese Holter ECG database of atrial fibrillation
Tsutsui, K., Biton Brimer, S., & Behar, J. (2024). SHDB-AF: a Japanese Holter ECG database of atrial fibrillation (version 1.0.0). PhysioNet. https://doi.org/10.13026/10mk-y852.
Tsutsui, K., Brimer, S.B., Ben-Moshe, N., Sellal, J.M., Oster, J., Mori, H., Ikeda, Y., Arai, T., Nakano, S., Kato, R., & Behar, J.A. (2024). SHDB-AF: a Japanese Holter ECG database of atrial fibrillation.

Includes 100 patients with paroxysmal atrial fibrillation





- Icentia11K: https://github.com/shawntan/icentia-ecg/tree/master/physionet --> 1 TB is toch wel te veel :
https://www.physionet.org/content/icentia11k-continuous-ecg/1.0/#files-panel

Tan, S., Ortiz-Gagné, S., Beaudoin-Gagnon, N., Fecteau, P., Courville, A., Bengio, Y., & Cohen, J. P. (2022). Icentia11k Single Lead Continuous Raw Electrocardiogram Dataset (version 1.0). PhysioNet. https://doi.org/10.13026/kk0v-r952.
Tan, S., Androz, G., Ortiz-Gagné, S., Chamseddine, A., Fecteau, P., Courville, A., Bengio, Y., & Cohen, J. P. (2021, October 21). Icentia11K: An Unsupervised Representation Learning Dataset for Arrhythmia Subtype Discovery. Computing in Cardiology Conference (CinC).

Includes 11000 patients and 2 billion labelled beats. Recorded on 250Hz recorded for up to 2 weeks. The average age is 62.2+-17.4 years. Each beat is labeled based on its rhythm: Sinus (NSR; 16 million), AF (AFib; 800,000), AFl (Aflutter; 300,000).


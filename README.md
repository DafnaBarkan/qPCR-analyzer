# qPCR-analyzer
Quantitative polymerase chain reaction (qPCR) is a routine analysis performed in my lab to measure nucleic acid sequences in real time during PCR amplification. This enables quantification of the targeted sequence and comparison across samples. Currently, the post qPCR-run data analysis involves manual calculations of mean Ct values, delta Ct, delta-delta Ct, normalization, and visualization. Performing these steps manually leaves room for human error.

I propose creating an automated data analysis and reporting tool for qPCR results. The input will be the qPCR machine “results” output file containing raw Ct data for each target and replicate. The output will include a summary table with the calculated data, visualizations of the analyzed results, and a short report summarizing the analysis parameters (number of replicates, normalization method, etc.).

This tool would streamline the qPCR analysis workflow in my lab by automatically performing the calculations, visualizations, and report generation that is currently done manually. Automating these repetitive steps will improve efficiency, reduce human error, and allow for easier comparison across qPCR experiments.

## Example data
The program asks the user to input some information about the data. Here are the answeres regarding the example input data:
qPCR result file name: 2023-12-14_5kbinf_calibration_QuantStudio 12K Flex_export.xls
The name of the relevant worksheet: Results
The control target name is: B2M

Dafna Barkan: https://dafnabarkan.github.io/


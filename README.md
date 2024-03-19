# qPCR-analyzer
Quantitative polymerase chain reaction (qPCR) is a routine analysis performed in my lab to measure nucleic acid sequences in real time during PCR amplification. This enables quantification of the targeted sequence and comparison across samples. Currently, the post qPCR-run data analysis involves manual calculations of mean Ct values, delta Ct, delta-delta Ct, normalization, and visualization. Performing these steps manually leaves room for human error.

I propose creating an automated data analysis and reporting tool for qPCR results. The input will be the qPCR machine results output file containing raw Ct data for each target and replicate.

The output will include in a new folder *("output")*:
* *"Ct analysis"* - A summary table with the calculated data throughout the analysis. <br> 
* *"plots"* - A folder that contains visualizations of the analyzed results. <br>
* *"analysis summary"* - A short report summarizing the analysis parameters (number of samples and targets, number of replicates, etc.). <br>

This tool would streamline the qPCR analysis workflow in my lab by automatically performing the calculations, visualizations, and report generation that is currently done manually. Automating these repetitive steps will improve efficiency, reduce human error, and allow for easier comparison across qPCR experiments.

### Example data
The program asks the user to input some information about the data.

Here are the answeres regarding the example input data:
* qPCR result file name: 2023-12-14_5kbinf_calibration_QuantStudio 12K Flex_export.xls
* The name of the relevant worksheet: Results
* The normalizing gene name: B2M
* The reference sample name: wt30a
* The samples pattern for ploting can be anything, I suggest "wt" or "del"
* The target pattern for ploting can be anything, I suggest "44" or "55"
  
You can download the example input here:
[2023-12-14_5kbinf_calibration_QuantStudio 12K Flex_export.xls](https://github.com/DafnaBarkan/qPCR-analyzer/files/14626571/2023-12-14_5kbinf_calibration_QuantStudio.12K.Flex_export.xls)


Dafna Barkan: https://dafnabarkan.github.io/


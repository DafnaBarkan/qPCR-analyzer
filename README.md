# qPCR-analyzer
Quantitative polymerase chain reaction (qPCR) is a routine analysis performed in my lab to measure nucleic acid sequences in real time during PCR amplification. This enables quantification of the targeted sequence and comparison across samples. Currently, the post qPCR-run data analysis involves manual calculations of mean Ct values, delta Ct, delta-delta Ct, normalization, and visualization. Performing these steps manually leaves room for human error.

I propose creating an automated data analysis and reporting tool for qPCR results. The input will be the qPCR machine results output file containing raw Ct data for each target and replicate.

The output will include in a new folder *("output")*:
* *"Ct analysis"* - A summary table with the calculated data throughout the analysis. <br> 
* *"plots"* - A folder that contains visualizations of the analyzed results. <br>
* *"analysis summary"* - A short report summarizing the analysis parameters (number of samples and targets, number of replicates, etc.). <br>

This tool would streamline the qPCR analysis workflow in my lab by automatically performing the calculations, visualizations, and report generation that is currently done manually. Automating these repetitive steps will improve efficiency, reduce human error, and allow for easier comparison across qPCR experiments.

### Dependencies installations
* Clone this repository to your local machine.<br>
  git clone https://github.com/your-username/your-repository.git
* Navigate to the project directory.<br>
  cd your-repository
* Install the project dependencies.<br>
  pip install -r requirements.txt

#### Python dependencies
* *xlrd* (version 2.0.1)
* *matplotlib* (version 3.6.2)
* *pandas* (version 1.5.2)
  
#### Additional imports
The following modules are also used in the project but are not listed in the requirements.txt file:
* *sys* 
* *importlib.util*
* *datetime*
* *os*

### How to run the program
Before running the program, ensure that the input data file is in the same directory as the *qPCR_analyzer.py* program, and your current directory (cd) is set to that folder.<br>
Additionally, make sure that the input data file is in .xls format.<br>
To run the program:
* Navigate to the directory where the qPCR_analyzer.py program and the input data file are located.
* Run the program with the following command:<br>
  python .\qPCR_analyzer.py    <br>
* Follow the instructions to conduct the analysis by your parameters.

### Example data
The program ask the user to input some information about the data.

Here are the answeres regarding the example input data:
* qPCR result file name: example_input.xls
* The name of the relevant worksheet: Results
* The normalizing gene name: B2M
* The reference sample name: wt30a
* The samples pattern for ploting can be anything, I suggest "wt" or "del"
* The target pattern for ploting can be anything, I suggest "44" or "55"
  
You can download the example input here:
[example_input.xls](https://github.com/DafnaBarkan/qPCR-analyzer/files/14664153/example_input.xls)

### Tests
Ensure that *test_qPCR_analyzer.py* is located in the same directory as the *qPCR_analyzer.py* program, and your current directory (cd) is set to that folder.<br>
* Run the tests with the following command:<br>
  pytest


Dafna Barkan: https://dafnabarkan.github.io/


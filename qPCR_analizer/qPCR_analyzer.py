import xlrd
import importlib.util
import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def check_dependencies():
    missing_dependencies = []
    dependencies = ['xlrd', 'pandas']
    for dependency in dependencies:
        spec = importlib.util.find_spec(dependency)
        if spec is None:
            missing_dependencies.append(dependency)
    return missing_dependencies

def install_dependencies():
    missing_dependencies = check_dependencies()
    if missing_dependencies:
        print("The following dependencies are missing and need to be installed:")
        for dependency in missing_dependencies:
            print(f"- {dependency}")
        print("Please run 'pip install -r requirements.txt' to install the dependencies")
        sys.exit(1)

def load_workbook():
    while True:
        wb_name = input("Please enter the name of the qPCR result file (including .xls extension): ")
        if wb_name.endswith('.xls'):
            try:
                wb = xlrd.open_workbook(filename=wb_name)
                return wb
            except FileNotFoundError:
                print("File not found. Please try again.")
        else:
            print("Invalid file name. Please make sure to include the .xls extension.")

def select_worksheet(wb):
    print(f"These are the Worksheets in the file:\n{wb.sheet_names()}")
    while True:
        ws_name = input("Please enter the name of the relevant worksheet: ")
        if ws_name in wb.sheet_names():
            ws = wb.sheet_by_name(ws_name)
            return ws
        else:
            print("Invalid Worksheet name. Please choose from the available Worksheet names.")

############################# PREPROCESSING ######################################

def preprocess_data(ws):
    start_row = 32
    data = []
    for row in range(start_row, ws.nrows):
        row_data = []
        for col in range(ws.ncols):
            cell_value = ws.cell_value(row, col)
            row_data.append(cell_value)
        data.append(row_data)
    column_names = data[0]
    df = pd.DataFrame(data[1:], columns=column_names)
    df = df[['Sample Name', 'Target Name', 'CT']]
    df = df.dropna()
    df = df[df['CT'] != '']
    df = df[df['Sample Name'] != '']
    return df

def target_fnder(df):
    target_name_levels = df['Target Name'].unique().tolist()
    print(f'These are the target genes in the file:\n{target_name_levels}')
    while True:
        control_target = input('Please enter the normalizing target gene: ')
        if control_target in target_name_levels:
            break
        else:
            print("Invalid input. Please choose from the available target names.")
    return control_target , target_name_levels
    
def replicate_avg(df):
    avg_df = pd.pivot_table(df,values = 'CT', index = 'Sample Name', columns = 'Target Name', aggfunc = 'mean')
    return avg_df

def delta_calculator(avg_df,control_target, target_name_levels):
    delta = {sample_name: [] for sample_name in avg_df.index}
    sample_names = []
    for sample_name, row in avg_df.iterrows():
        sample_names.append(sample_name)
        for target_level in target_name_levels:
            if target_level != control_target:
                delta_value = row[target_level] - row[control_target]
                delta[sample_name].append(delta_value)
    delta_df = pd.DataFrame(delta, index = target_name_levels[:-1]).T
    return delta_df , sample_names

def deltadelta_calculator(sample_names, delta_df):
    print(f'These are the samples in the file:\n{sample_names}')
    reference_sample = input('Please enter the reference sample name: ')
    while reference_sample not in sample_names:
        print("Invalid reference sample name. Please choose from the available sample names.")
        reference_sample = input('Please enter the reference sample name: ')
    delta_delta_df = delta_df.sub(delta_df.loc[reference_sample])
    return delta_delta_df , reference_sample

def expression_calculator(delta_delta_df):
    exp_df = 2**(-delta_delta_df)
    return exp_df

def output_folder_setup():
    current_time = datetime.now().strftime("%d%m%y")
    output_dir = f'qPCRanalyzer_output_{current_time}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def analysis_output_save(avg_df, delta_df, delta_delta_df, exp_df,output_dir):
    delta_df.columns = [f"{col}_delta" for col in delta_df.columns]
    delta_delta_df.columns = [f"{col}_delta_delta" for col in delta_delta_df.columns]
    exp_df.columns = [f"{col}_exp" for col in exp_df.columns]
    Ct_analysis_df = pd.concat([avg_df, delta_df, delta_delta_df, exp_df], axis=1)
    Ct_analysis_df.to_excel(os.path.join(output_dir, 'Ct analysis.xlsx'))
    print("Analysis is complete!")

############################# SUGGESTED PLOTS ######################################

def plots_folder_setup(output_dir):
    plots_dir = os.path.join(output_dir, 'plots')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    return plots_dir

def find_test_targets(exp_df):
    targets = exp_df.columns.tolist()  
    return targets

def get_plot_samples(sample_names, substring_samples):
    if substring_samples:
        plot_samples = [sample for sample in sample_names if substring_samples in sample]
        if not plot_samples:
            plot_samples = sample_names 
    else:
        plot_samples = sample_names
    return plot_samples

def get_plot_targets(targets, substring_targets):
    if substring_targets:
        plot_targets = [target for target in targets if substring_targets in target]
        if not plot_targets:
            plot_targets = targets 
    else:
        plot_targets = targets
    return plot_targets

def plot_expression(filtered_df, plot_samples, plot_count, plots_dir, substring_samples):
    ax = filtered_df.plot.bar(rot=0)
    ax.set_xticklabels(plot_samples, rotation=90)
    plt.xlabel('Sample Name')
    plt.ylabel('Expression')
    plt.title(f'{substring_samples} Relative Expression')
    plt.savefig(os.path.join(plots_dir, f'expression_plot_{plot_count}.png'))
    print("Close the plot window to continue...")
    plt.show()

def ask_plot_again():
    while True:
        plot_again = input("Do you want to plot anything else? (yes/no): ").lower() 
        if plot_again == 'yes' or plot_again == 'no':
            return plot_again
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def plot_qpcr_data(sample_names, targets, exp_df, plots_dir):
    plot_count = 1
    while True:
        substring_samples = input("Please enter the substring/pattern of the samples you want to plot (press Enter to plot all samples): ")
        plot_samples = get_plot_samples(sample_names, substring_samples)
        print("Samples to plot: ", plot_samples)
        substring_targets = input("Please enter the substring/pattern of the targets you want to plot (press Enter to plot all targets): ")
        plot_targets = get_plot_targets(targets, substring_targets)
        print("Targets to plot: ", plot_targets)
        filtered_df = exp_df.loc[plot_samples, plot_targets]
        plot_expression(filtered_df, plot_samples, plot_count, plots_dir, substring_samples)
        plot_count += 1
        plot_again = ask_plot_again()
        if plot_again == 'no':
            break

############################# ANALYSIS SUMMERY ######################################

def replicates_summary_generator(df):
    replicates = []
    for sample in df['Sample Name'].unique():
        for target in df['Target Name'].unique():
            filtered_df = df[(df['Sample Name'] == sample) & (df['Target Name'] == target)]
            count = filtered_df.shape[0]
            replicates.append((sample, target, count))
    return replicates

def analysis_summary_generator(df, sample_names, reference_sample, targets, control_target):
    replicates = replicates_summary_generator(df)
    analysis_summary = [
        ["samples analyzed after avg" , sample_names],
        ["reference sample", reference_sample],
        ["targets used for analysis" , targets],
        ["normalizing gene", control_target],
        ["number of replicates analyzed in each target", str(replicates)]
    ]
    return analysis_summary
    
def analysis_summary_save(analysis_summary, output_dir):
    summary_df = pd.DataFrame(analysis_summary)
    summary_df.to_excel(os.path.join(output_dir, 'analysis summary.xlsx'), index=False, header=False, engine='openpyxl')
    print("\n**** The qPCR is analyzed! check the output folder ****\n")


def main():
    install_dependencies()
    wb = load_workbook()
    ws = select_worksheet(wb)
    df = preprocess_data(ws)
    control_target , target_name_levels = target_fnder(df)
    avg_df = replicate_avg(df)
    delta_df , sample_names = delta_calculator(avg_df,control_target, target_name_levels)
    delta_delta_df , reference_sample = deltadelta_calculator(sample_names, delta_df)
    exp_df = expression_calculator(delta_delta_df)
    output_dir = output_folder_setup()
    analysis_output_save(avg_df, delta_df, delta_delta_df, exp_df,output_dir)
    plots_dir = plots_folder_setup(output_dir)
    targets = find_test_targets(exp_df)
    plot_qpcr_data(sample_names, targets, exp_df, plots_dir)
    analysis_summary = analysis_summary_generator(df, sample_names, reference_sample, targets, control_target)
    analysis_summary_save(analysis_summary, output_dir)

if __name__ == "__main__":
    main()

import pandas as pd
import os
import re 
import subprocess 
import pandas as pd 
from src.config import PATH_PROJECT


df = pd.read_excel(os.path.join(PATH_PROJECT, "data/") + "dataset.xlsx").fillna("Non renseigne")
df_instructions = pd.read_excel(os.path.join(PATH_PROJECT, "data/") + "instructions.xlsx")
disorders_str = ''
for i, row in df_instructions.iterrows():
    disorders_str += f'{row["Disorder"]} : {row["Description"]}\n'
system = f'You are an expert at diagnosing patients according to the ICD-11 Clinical Descriptions and Diagnostic Requirements(CDDR). The patient data are represented by a list of current symptoms denoted as Observed and a list of history denoted as History. Observed matches the patient with the symptom and the number of weeks it has been observed. History matches the patient with the condition and the number of times it existed. No record for a patient means that there is no related data for them. The considered disorders are: {disorders_str}'

def get_prompt_patient_data(patient_id):
    patient_data = df[df['PatientID'] == patient_id]
    observed = []
    for symptom, value in zip(patient_data["Observed_Symptom"].values.tolist(), patient_data["Observed_Week"].values.tolist()):
        observed.append(f'Symptom : {symptom} has been observed for {value} weeks')
    observed = "Observed : " + "; ".join(observed)
    history_conditions = []
    for condition, count in zip(patient_data["History_Condition"].values.tolist(), patient_data["History_Count"].values.tolist()):
        if condition != "Non renseigne":
            history_conditions.append(f'happened {count} times : {condition}')
    history_conditions = "History : " + "; ".join(history_conditions)
    mood_episodes = []
    for episode in patient_data["Mood_Episode"].values.tolist():
        if episode != "Non renseigne":
            mood_episodes.append(episode)
    mood_episodes = "Mood episodes : " + "; ".join(mood_episodes)
    return observed, history_conditions, mood_episodes

def preproc_df(path = PATH_PROJECT):
    df = pd.read_excel(os.path.join(path, "data/") + "dataset.xlsx").fillna("Non renseigne")
    df.loc[df['History_Count']=="Non renseigne", 'History_Count'] = None
    df['History_Count'] = df['History_Count'].astype(float)

    df_grouped = df.groupby(['PatientID', 'Disorder'], as_index=False).agg({
        'Observed_Symptom': lambda x: list(x),
        'Observed_Week': lambda x: list(x),
        'History_Condition': lambda x: list(x),
        'History_Count': lambda x: list(x),
        'Mood_Episode': lambda x: list(x),
    })

    df_grouped['Observed_Symptoms_Weeks'] = df_grouped.apply(
        lambda row: list(zip(row['Observed_Symptom'], row['Observed_Week'])), axis=1
    )

    df_grouped.drop(columns=['Observed_Symptom', 'Observed_Week'], inplace=True)

    return df_grouped

# def run_souffle(dl_file, input_dir, output_dir):
#     command = ["souffle", "-F", input_dir, "-D", output_dir, dl_file]
#     subprocess.run(command, check=True)
#     print("Soufflé execution completed.")

# def read_output_csv(output_dir, relation_name):
#     csv_path = f"{output_dir}/{relation_name}.csv"
#     df = pd.read_csv(csv_path, delimiter='\t')
#     return df



import pandas as pd
from itertools import chain

# Define relevant symptom and condition names
symptoms = [
    'depressed_mood', 
    'reduced_concentration', 
    'reduced_energy',
    'increased_talkativeness', 
    'diminished_interest_pleasure', 
    'low_self_worth',
    'psychomotor_disturbances', 
    'increased_activity_energy',
    'euphoria_irritability_expansiveness', 
    'racing_thoughts',
    'increased_self_esteem', 
    'disrupted_excessive_sleep',
    'change_in_appetite_weight', 
    'decreased_need_for_sleep', 
    'distractibility',
    'recurrent_thoughts_death_suicide', 
    'impulsive_reckless_behavior',
    'increased_sexual_sociability_goal_directed_activity', 
    'hopelessness',
    'delusions', 
    'passivity_experiences', 
    'disorganized_behavior'
]

conditions = [
    'depressive', 
    'hypomanic', 
    'Non renseigné', 
    'mixed', 
    'manic'
]

# Function to check for Manic Episode
def has_manic_episode(row):
    return (row['increased_activity_energy'] == 1 or 
            row['euphoria_irritability_expansiveness'] == 1 or 
            row['racing_thoughts'] == 1 or 
            row['increased_self_esteem'] == 1)

# Function to check for Hypomanic Episode
def has_hypomanic_episode(row):
    return (row['increased_activity_energy'] == 2 or 
            row['euphoria_irritability_expansiveness'] == 2 or 
            row['racing_thoughts'] == 2 or 
            row['increased_self_esteem'] == 2)

# Function to check for Depressive Episode
def has_depressive_episode(row):
    return (row['depressed_mood'] == 1 or 
            row['reduced_concentration'] == 1 or 
            row['reduced_energy'] == 1 or 
            row['low_self_worth'] == 1 or 
            row['psychomotor_disturbances'] == 1 or 
            row['hopelessness'] == 1)

# Function to check for Mixed Episode
def has_mixed_episode(row):
    return (row['delusions'] == 1 or 
            row['passivity_experiences'] == 1)

# Function to check for Bipolar I Disorder
def is_bipolar_i(row):
    return row['manic_or_mixed_episodes'] > 0

# Function to check for Bipolar II Disorder
def is_bipolar_ii(row):
    return row['hypomanic_episodes'] > 0 and row['depressive_episodes'] > 0

# Function to check for Single Episode Depressive Disorder
def is_single_episode_depressive(row):
    return (row['depressive_episodes'] == 1 and 
            row['manic_or_mixed_episodes'] == 0 and 
            row['hypomanic_episodes'] == 0)

# Function to check for Recurrent Depressive Disorder
def is_recurrent_depressive(row):
    return row['depressive_episodes'] > 1

# Create DataFrame with symptoms
symptoms_df = pd.DataFrame({'Symptom': symptoms}, index=[0])

# Create DataFrame with conditions
conditions_df = pd.DataFrame({'Condition': conditions}, index=[0])

# Define mood episode data
mood_episode_data = {
    'increased_activity_energy': [1, 0, 0, 0],
    'euphoria_irritability_expansiveness': [1, 0, 0, 0],
    'racing_thoughts': [1, 0, 0, 0],
    'increased_self_esteem': [1, 0, 0, 0],
    'disrupted_excessive_sleep': [0, 0, 0, 0],
    'change_in_appetite_weight': [0, 0, 0, 0],
    'decreased_need_for_sleep': [0, 1, 0, 0],
    'distractibility': [0, 0, 0, 0],
    'recurrent_thoughts_death_suicide': [0, 0, 0, 0],
    'impulsive_reckless_behavior': [0, 0, 0, 0],
    'increased_sexual_sociability_goal_directed_activity': [0, 0, 0, 0],
    'hopelessness': [1, 0, 0, 0],
    'delusions': [0, 0, 1, 0],
    'passivity_experiences': [0, 0, 1, 0],
    'disorganized_behavior': [0, 0, 1, 0]
}

mood_episode_df = pd.DataFrame(mood_episode_data)

# Define Bipolar I Disorder data
bipolar_i_data = {
    'manic_or_mixed_episodes': [1, 0, 0, 0],
    'depressive_episodes': [0, 1, 0, 0],
    'hypomanic_episodes': [0, 0, 0, 0]
}

bipolar_i_df = pd.DataFrame(bipolar_i_data)

# Define Bipolar II Disorder data
bipolar_ii_data = {
    'manic_or_mixed_episodes': [0, 0, 0, 0],
    'depressive_episodes': [1, 0, 0, 0],
    'hypomanic_episodes': [1, 0, 0, 0]
}

bipolar_ii_df = pd.DataFrame(bipolar_ii_data)

# Define Single Episode Depressive Disorder data
single_episode_depressive_data = {
    'manic_or_mixed_episodes': [0, 0, 0, 0],
    'depressive_episodes': [1, 0, 0, 0],
    'hypomanic_episodes': [0, 0, 0, 0]
}

single_episode_depressive_df = pd.DataFrame(single_episode_depressive_data)

# Define Recurrent Depressive Disorder data
recurrent_depressive_data = {
    'manic_or_mixed_episodes': [0, 0, 0, 0],
    'depressive_episodes': [2, 0, 0, 0]
}

recurrent_depressive_df = pd.DataFrame(recurrent_depressive_data)

# Concatenate DataFrames
all_symptoms_df = pd.concat([symptoms_df, mood_episode_df, bipolar_i_df, bipolar_ii_df, single_episode_depressive_df, recurrent_depressive_df], ignore_index=True)
conditions_df['Symptom'] = conditions_df['Condition']
bipolar_i_df['Symptom'] = bipolar_i_df['manic_or_mixed_episodes']
bipolar_ii_df['Symptom'] = bipolar_ii_df['hypomanic_episodes']

# Create condition symptoms DataFrame
condition_symptoms_df = pd.concat([symptoms_df, conditions_df], ignore_index=True)

# Check for Manic Episodes
mood_episode_df.loc[mood_episode_df['increased_activity_energy'] == 1, 'Symptom'] = 'Manic Episode'
mood_episode_df.loc[mood_episode_df['euphoria_irritability_expansiveness'] == 1, 'Symptom'] = 'Manic Episode'
mood_episode_df.loc[mood_episode_df['racing_thoughts'] == 1, 'Symptom'] = 'Manic Episode'
mood_episode_df.loc[mood_episode_df['increased_self_esteem'] == 1, 'Symptom'] = 'Manic Episode'

# Check for Hypomanic Episodes
mood_episode_df.loc[mood_episode_df['increased_activity_energy'] == 2, 'Symptom'] = 'Hypomanic Episode'
mood_episode_df.loc[mood_episode_df['euphoria_irritability_expansiveness'] == 2, 'Symptom'] = 'Hypomanic Episode'
mood_episode_df.loc[mood_episode_df['racing_thoughts'] == 2, 'Symptom'] = 'Hypomanic Episode'
mood_episode_df.loc[mood_episode_df['increased_self_esteem'] == 2, 'Symptom'] = 'Hypomanic Episode'

# Check for Depressive Episodes
all_symptoms_df.loc[all_symptoms_df['depressed_mood'] == 1, 'Symptom'] = 'Depressive Episode'
all_symptoms_df.loc[all_symptoms_df['reduced_concentration'] == 1, 'Symptom'] = 'Depressive Episode'
all_symptoms_df.loc[all_symptoms_df['reduced_energy'] == 1, 'Symptom'] = 'Depressive Episode'
all_symptoms_df.loc[all_symptoms_df['low_self_worth'] == 1, 'Symptom'] = 'Depressive Episode'
all_symptoms_df.loc[all_symptoms_df['psychomotor_disturbances'] == 1, 'Symptom'] = 'Depressive Episode'
all_symptoms_df.loc[all_symptoms_df['hopelessness'] == 1, 'Symptom'] = 'Depressive Episode'

# Check for Mixed Episodes
mood_episode_df.loc[mood_episode_df['delusions'] == 1, 'Symptom'] = 'Mixed Episode'
mood_episode_df.loc[mood_episode_df['passivity_experiences'] == 1, 'Symptom'] = 'Mixed Episode'

# Create symptoms DataFrame with conditions
symptoms_condition_df = pd.concat([all_symptoms_df, condition_symptoms_df], ignore_index=True)

print(symptoms_condition_df)
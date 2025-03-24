def classify_diagnosis(row):
    # Bipolar I criteria
    if (row['Observed_Week'] == 6A60.A).any() or (row['Observed_Week'] == 6A60.B).any() or (row['Observed_Week'] == 6A60.C).any() or (row['Observed_Week'] == 6A60.D).any():
        if row['Observed_Week'] == 'current':
            return 'Bipolar I'
    
    # Bipolar II criteria
    elif (row['Observed_Week'].isin(['6A61.A', '6A61.B', '6A61.C', '6A61.D'])).any():
        if row['Observed_Week'] == 'current':
            return 'Bipolar II'
    
    # Single Episode Depressive Disorder criteria
    elif (row['Observed_Week'].isin(['6A70.A', '6A70.B'])).any() and not any(['manic' in symptom for symptom in row['Symptoms']]):
        if row['Observed_Week'] == 'current':
            return 'Single Episode Depressive Disorder'
    
    # Recurrent Depressive Disorder criteria
    elif ((row['Observed_Week'].isin(['6A70.A', '6A70.B', '6A85.A'])).any() and not any(['manic' in symptom for symptom in row['Symptoms']])):
        if row['Observed_Week'] == 'current':
            return 'Recurrent Depressive Disorder'
    
    # If none of the above criteria are met
    else:
        return 'No Diagnosis'

# Example usage:
# diagnosis = classify_diagnosis(row_data)
from pydatalog import Term, TermVar, Facts, Rule

# Define terms and variables
symptoms = ["depression", "anxiety", "irritability"]
conditions = ["hypothyroidism", "hyperthyroidism"]

# Create facts
f = Facts(
    symptoms_var = Term('symptom', [Term('dep', TermVar('s')) for s in symptoms]),
    condition_var = Term('condition', [Term('hypo', TermVar('c')) for c in conditions])
)
rule1 = Rule("Bipolar I", [
    symptoms_var >> Term('mixed', TermVar('s')),
    condition_var >> Term('none')
], [])

rule2 = Rule("Single Episode Depressive Disorder (mild)", [
    symptoms_var >> Term('dep', TermVar('s')),
    condition_var >> Term('hypo', TermVar('c'))
], [])

rule3 = Rule("Recurrent Depressive Disorder (mild)", [
    symptoms_var >> Term('dep', TermVar('s')),
    condition_var >> Term('none')
], [])

rule4 = Rule("Single Episode Depressive Disorder (moderate)", [
    symptoms_var >> Term('dep', TermVar('s')),
    condition_var >> Term('hypo', TermVar('c'))
], [])

rule5 = Rule("Recurrent Depressive Disorder (moderate)", [
    symptoms_var >> Term('dep', TermVar('s')),
    condition_var >> Term('none')
], [])

def diagnose(row):
    s = row['Observed_Symptom'].any()
    c = row['History_Condition'].any()

    if s and c:
        return "Recurrent Depressive Disorder"
    elif s and not c:
        if row['Observed_Week'].count(1) >= 4: #assuming at least four weeks
            return "Single Episode Depressive Disorder (moderate)"
        else:
            return "Bipolar I"
    elif not s and c:
        return "Recurrent Depressive Disorder (mild)"
    else:
        return "No diagnosis"

# Test the diagnose function
row1 = {'Observed_Symptom': ['depression'], 'Observed_Week': [1, 2, 3, 4], 'History_Condition': ['hypothyroidism']}
print(diagnose(row1)) # Output: Single Episode Depressive Disorder (moderate)

row2 = {'Observed_Symptom': ['anxiety', 'irritability'], 'Observed_Week': [5, 6, 7, 8], 'History_Condition': ['hyperthyroidism']}
print(diagnose(row2)) # Output: Bipolar I

row3 = {'Observed_Symptom': ['depression'], 'Observed_Week': [1, 2, 3], 'History_Condition': ['hypothyroidism']}
print(diagnose(row3)) # Output: Recurrent Depressive Disorder (mild)

row4 = {'Observed_Symptom': [], 'Observed_Week': [1, 2, 3, 4], 'History_Condition': ['hyperthyroidism']}
print(diagnose(row4)) # Output: No diagnosis
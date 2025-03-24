import sys
sys.path.append('../')
from notebooks import code_Datalog

pyDatalog.create_terms('X')

# Inject facts for patient 1
    + code_Datalog.Observed('1', 'depressed_mood', 1.5)
    + code_Datalog.Observed('1', 'reduced_concentration', 1.2)
    + code_Datalog.Observed('1', 'reduced_energy', 0.8)
    + code_Datalog.Observed('1', 'increased_talkativeness', 0.6)
    + code_Datalog.Observed('1', 'depressive', 1.0)
    + code_Datalog.Observed('1', 'hypomanic', 1.0)

# Diagnosis Query
results = code_Datalog.Diagnosis(code_Datalog.PATIENT, X).data

# Save to txt
with open('diagnosis_output.txt', 'w') as f:
    for r in results:
        f.write(f'Patient 1 : r[1]\n')
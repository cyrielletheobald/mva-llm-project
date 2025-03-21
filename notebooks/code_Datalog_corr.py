from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, ManicEpisode')

# Define symptoms for Observed relation
Observed(PATIENT, 'Depressive', WEEKS) <= (WEEKS > 0.0) # Depressive Episode criterion from ICD-11 CDDR
Observed(PATIENT, 'Mania', WEEKS) <= (WEEKS > 0.0) # Manic Episode criterion from ICD-11 CDDR
Observed(PATIENT, 'Mixed', WEEKS) <= (WEEKS > 0.0) # Mixed Episode criterion from ICD-11 CDDR
Observed(PATIENT, 'Hypomanic', WEEKS) <= (WEEKS > 0.0) # Hypomanic Episode criterion from ICD-11 CDDR

# Manic Episode rules
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (WEEKS >= 3.0)
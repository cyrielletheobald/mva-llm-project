from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, History, Diagnosis')

# Define the sup function for comparison
sup = lambda x,y : x >= y 

# Bipolar I Disorder - Mood Episode (Depressive, Manic, Mixed) Criteria
Diagnosis(PATIENT, 'Bipolar I') <= \
    (Observed(PATIENT, 'Mania', WEEKS) & (WEEKS >= 7.0)) | \
    (Observed(PATIENT, 'Mixed', WEEKS) & (WEEKS >= 7.0)) | \
    (History(PATIENT, 'Depressive Episode', COUNT) & (COUNT >= 2))

# Bipolar II Disorder - Mood Episode (Depressive and Hypomanic) Criteria
Diagnosis(PATIENT, 'Bipolar II') <= \
    (Observed(PATIENT, 'Hypomania', WEEKS) & (WEEKS >= 7.0)) | \
    (History(PATIENT, 'Depressive Episode', COUNT) & (COUNT >= 1))

# Single Episode Depressive Disorder - Criteria for at least one depressive episode without any manic or mixed episodes
Diagnosis(PATIENT, 'Single Episode Depressive Disorder') <= \
    History(PATIENT, 'Depressive Episode', COUNT) & (COUNT == 1) & \
    ((Observed(PATIENT, 'Mania', WEEKS) == 0) | (WEEKS < 7.0)) & \
    ((Observed(PATIENT, 'Mixed', WEEKS) == 0) | (WEEKS < 7.0))

# Recurrent Depressive Disorder - Criteria for at least two depressive episodes, regardless of the presence of mania or hypomania
Diagnosis(PATIENT, 'Recurrent Depressive Disorder') <= \
    History(PATIENT, 'Depressive Episode', COUNT) & (COUNT >= 2)
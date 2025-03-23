from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, ManicEpisode, DepressiveEpisode, MixedEpisode, HypomanicEpisode',
                      'BipolarI, BipolarII, SingleEPDD, RecurrentDepressive')

# Mood Episode rules
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (WEEKS >= 3.0)
HypomanicEpisode(PATIENT) <= Observed(PATIENT, 'Hypomania', WEEKS)

# Bipolar I diagnosis
BipolarI(PATIENT) <= Diagnosis(PATIENT, 'BipolarI')
BipolarI(PATIENT) :- ManicEpisode(PATIENT)

# Bipolar II diagnosis
BipolarII(PATIENT) <= Diagnosis(PATIENT, 'BipolarII')
BipolarII(PATIENT) :- HypomanicEpisode(PATIENT), DepressiveEpisode(PATIENT)

# Single Episode Depressive Disorder diagnosis
SingleEPDD(PATIENT) <= Diagnosis(PATIENT, 'SingleEPDD')
SingleEPDD(PATIENT) :- DepressiveEpisode(PATIENT)

# Recurrent Depressive Disorder diagnosis
RecurrentDepressive(PATIENT) <= Diagnosis(PATIENT, 'RecurrentDepressive')
RecurrentDepressive(PATIENT) :- DepressiveEpisode(PATIENT), DepressiveEpisode(PATIENT, Weeks: W2)
W2 >= 3

# Symptom names for Observed relation (assuming a list of relevant symptoms here for simplicity)
ObservedSymptoms = ['Mania', 'Hypomania', 'Depression']
for symptom in ObservedSymptoms:
    rule(f'DepressiveEpisode(PATIENT) <= Observed(PATIENT, "{symptom}", WEEKS)')
    rule(f'ManicEpisode(PATIENT) <= Observed(PATIENT, "{symptom}", WEEKS)')

# Condition names for History relation (assuming a list of relevant conditions here for simplicity)
HistoryConditions = ['Depression', 'Hypomania', 'Mania']
for condition in HistoryConditions:
    rule(f'History(PATIENT, "{condition}")')

# Output the Diagnosis relation
rule('Diagnosis(PATIENT, Disorder) :- BipolarI(PATIENT)')
rule('Diagnosis(PATIENT, Disorder) :- BipolarII(PATIENT)')
rule('Diagnosis(PATIENT, Disorder) :- SingleEPDD(PATIENT)')
rule('Diagnosis(PATIENT, Disorder) :- RecurrentDepressive(PATIENT)')
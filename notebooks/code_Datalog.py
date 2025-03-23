from pyDatalog import pyDatalog
pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, History, Diagnosis')
sup = lambda x,y : x >= y 
# Symptom definitions
Observed(PATIENT, 'DepressiveEpisode', WEEKS) <= Observed(PATIENT, 'Depression', WEEKS) & (WEEKS > 14.0)
Observed(PATIENT, 'ManicEpisode', WEEKS) <= Observed(PATIENT, 'Mania', WEEKS) & (WEEKS >= 7.0)
Observed(PATIENT, 'MixedEpisode', WEEKS) <= (Observed(PATIENT, 'Depression', WEEKS) | Observed(PATIENT, 'Hypomanic', WEEKS)) & (WEEKS > 14.0)
Observed(PATIENT, 'HypomanicEpisode', WEEKS) <= Observed(PATIENT, 'Hypomania', WEEKS) & (WEEKS >= 7.0)
# Condition definitions
History(PATIENT, 'BipolarI', Count) <= (Observed(PATIENT, 'ManicEpisode', _) | Observed(PATIENT, 'MixedEpisode', _)) & sup(Count, 4)
History(PATIENT, 'BipolarII', Count) <= (Observed(PATIENT, 'HypomanicEpisode', _) | Observed(PATIENT, 'DepressiveEpisode', _)) & sup(Count, 2)
History(PATIENT, 'SingleDepression', Count) <= Observed(PATIENT, 'DepressiveEpisode', _) & (Count == 1)
History(PATIENT, 'RecurrentDepression', Count) <= Observed(PATIENT, 'DepressiveEpisode', _) & sup(Count, 2)
# Diagnosis rules
Diagnosis(PATIENT, 'BipolarI') <= History(PATIENT, 'BipolarI', Count) & (Count >= 1)
Diagnosis(PATIENT, 'BipolarII') <= History(PATIENT, 'BipolarII', Count) & (Count >= 2)
Diagnosis(PATIENT, 'SingleDepression') <= History(PATIENT, 'SingleDepression', Count)
Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= History(PATIENT, 'RecurrentDepression', Count)
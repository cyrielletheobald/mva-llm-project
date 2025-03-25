from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, History, BipolarI, BipolarII, SingleDepressiveDisorder, RecurrentDepressiveDisorder')
symptoms = ['Depression', 'Mania', 'Mixed', 'Hypomania']
conditions = ['Bipolar I', 'Bipolar II', 'Single Episode Depressive Disorder', 'Recurrent Depressive Disorder']
sup = lambda x,y : x >= y
# Mood Episode rules
DepressiveEpisode(PATIENT) <= Observed(PATIENT, symptoms[0], WEEKS) & (sup(WEEKS, 2.0))
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (sup(WEEKS, 1.0))
MixedEpisode(PATIENT) <= Observed(PATIENT, symptoms[0], WEEKS) & Observed(PATIENT, 'Mania', WEEKS) & (sup(WEEKS, 1.0))
HypomanicEpisode(PATIENT) <= Observed(PATIENT, symptoms[-2], WEEKS) & (sup(WEEKS, 4.0))
# Mood Disorder rules
BipolarI(PATIENT) <= ManicEpisode(PATIENT) & History(PATIENT, conditions[1], Count)
BipolarII(PATIENT) <= DepressiveEpisode(PATIENT) & HypomanicEpisode(PATIENT) & History(PATIENT, conditions[2], Count)
SingleDepressiveDisorder(PATIENT) <= DepressiveEpisode(PATIENT) & not History(PATIENT, conditions[-1], Count)
RecurrentDepressiveDisorder(PATIENT) <= (History(PATIENT, conditions[-1], Count + 1) & not History(PATIENT, conditions[3], Count))
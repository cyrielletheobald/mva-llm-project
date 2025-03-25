from pyDatalog import pyDatalog

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, ManicEpisode, sup')
sup = lambda x,y : x >= y 
# Manic Episode rules
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (sup(WEEKS, 3.0))
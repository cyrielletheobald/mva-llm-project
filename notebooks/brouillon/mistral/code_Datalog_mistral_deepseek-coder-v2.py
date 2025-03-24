from pyDatalog import pyDatalog, sup

pyDatalog.clear()
pyDatalog.create_terms('PATIENT, WEEKS, Observed, History, MajorDepressiveEpisode, ManicEpisode, HypomanicEpisode, BipolarI, BipolarII,\
SingleEpisodeDepressiveDisorder, RecurrentDepressiveDisorder')

# Symptoms for Major Depressive Episode
Symptom_MajorDepressiveEpisode = ['depressed mood', 'decreased interest or pleasure', 'significant weight loss or gain',\
                             'insomnia or hypersomnia', 'psychomotor agitation or retardation', 'fatigue or loss of energy',\
                             'feelings of worthlessness or excessive or inappropriate guilt', 'diminished ability to think or concentrate', 'recurrent thoughts of death']

# Manic Episode rules
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (sup(WEEKS, 1.0))

# Hypomanic Episode rules
HypomanicEpisode(PATIENT) <= Observed(PATIENT, 'Hypomania', WEEKS) & (sup(WEEKS, 4.0))

# Major Depressive Episode rules
MajorDepressiveEpisode(PATIENT) <= (len(Observed({'Patient': PATIENT, 'Symptom': Symptom_MajorDepressiveEpisode})) >= 5) & (sup(WEEKS, 2.0))

# Bipolar I criteria
BipolarI(PATIENT) <= History(PATIENT, 'ManicEpisode', _) & MajorDepressiveEpisode(PATIENT)

# Bipolar II criteria
BipolarII(PATIENT) <= History(PATIENT, 'HypomanicEpisode', _) & MajorDepressiveEpisode(PATIENT)

# Single Episode Depressive Disorder criteria
SingleEpisodeDepressiveDisorder(PATIENT) <= MajorDepressiveEpisode(PATIENT) & (not History(_, 'MajorDepressiveEpisode', _))

# Recurrent Depressive Disorder criteria
RecurrentDepressiveDisorder(PATIENT) <= (History(_, 'MajorDepressiveEpisode', Count=Count) for Count > 1)
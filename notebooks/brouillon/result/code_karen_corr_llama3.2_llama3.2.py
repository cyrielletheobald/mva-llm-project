from kanren import Relation, facts, var, run, conde

# Declare relations
Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Variables
PATIENT, WEEKS = var(), var()
SYM1, SYM2, SYM3, SYM4 = var(), var(), var(), var()
COND1, COND2, COND3, COND4 = var(), var(), var(), var()

# Define conditions as facts
facts([PATIENT, 'DepressionCount'], ['Depression', 2])
facts([PATIENT, 'HypomaniaCount'], ['Hypomania', 1])

# Relevant symptom names for Observed relation
symptoms = ['DepressiveEpisode', 'ManicEpisode', 'MixedEpisode', 'HypomanicEpisode']

# Define a reusable condition for mood episode duration
mood_episode_duration = (WEEKS >= 2)

# Rule logic

# Bipolar I
Diagnosis(PATIENT, 'BipolarI') <= conde(
    Observed(PATIENT, 'ManicEpisode', WEEKS),
    mood_episode_duration,
)

# Bipolar II
Diagnosis(PATIENT, 'BipolarII') <= conde(
    Observed(PATIENT, 'HypomanicEpisode', WEEKS),
    mood_episode_duration,
)

# Single Episode Depressive Disorder
Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') <= conde(
    Observed(PATIENT, 'DepressiveEpisode', WEEKS),
    mood_episode_duration,
)

# Recurrent Depressive Disorder
Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= conde(
    Observed(PATIENT, 'DepressiveEpisode', WEEKS),
    History(PATIENT, 'DepressionCount', 2), # No Depression episodes in the past
    & History(PATIENT, 'ManiaCount', 0), # No Mania episodes in the past
    & History(PATIENT, 'HypomaniaCount', 0) # No Hypomania episodes in the past
)

# Relevant condition names for History relation
conditions = ['Depression', 'Mania', 'Hypomania']

# Repeated conjunctions for mood disorder condition
for cond in conditions:
    Diagnosis(PATIENT, 'BipolarI') | Diagnosis(PATIENT, 'BipolarII') | Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') | Diagnosis(PATIENT, 'RecurrentDepressiveDisorder')
    & conde(
        History(PATIENT, cond, 1),
        History(PATIENT, 'ManiaCount', 0),
        History(PATIENT, 'HypomaniaCount', 0)
    )

# Relevant symptom names for Observed relation
for sym in symptoms:
    Diagnosis(PATIENT, 'BipolarI') | Diagnosis(PATIENT, 'BipolarII') | Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') | Diagnosis(PATIENT, 'RecurrentDepressiveDisorder')
    & membero(SYM1, symptoms)
    & mood_episode_duration
    | Diagnosis(PATIENT, 'Depressive') | Diagnosis(PATIENT, 'Manic') | Diagnosis(PATIENT, 'Mixed') | Diagnosis(PATIENT, 'Hypomanic')

# Run the queries
run(Disagnosis, [(PATIENT, cond)]) for cond in ['BipolarI', 'BipolarII', 'SingleEpisodeDepressiveDisorder', 'RecurrentDepressiveDisorder'])
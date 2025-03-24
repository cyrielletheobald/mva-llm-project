from kanren import Relation, facts, var, run, conde, membero

# Declare relations
Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Variables
PATIENT, WEEKS = var(), var()
SYM1, SYM2, SYM3, SYM4 = var(), var(), var(), var()
COND1, COND2, COND3, COND4 = var(), var(), var(), var()

# Rule logic

# Bipolar I
Diagnosis(PATIENT, 'BipolarI') <= conde(
    Observed(PATIENT, 'ManicEpisode', WEEKS),
    (WEEKS >= 7), # Note: 7 days is the minimum duration for Mania in ICD-11 CDDR
)

# Bipolar II
Diagnosis(PATIENT, 'BipolarII') <= conde(
    Observed(PATIENT, 'HypomanicEpisode', WEEKS),
    (WEEKS >= 4), # Note: 4 days is the minimum duration for Hypomania in ICD-11 CDDR
)

# Single Episode Depressive Disorder
Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') <= conde(
    Observed(PATIENT, 'DepressiveEpisode', WEEKS),
    (WEEKS >= 2), # Note: 2 weeks is the minimum duration for Depression in ICD-11 CDDR
)

# Recurrent Depressive Disorder
Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= conde(
    Observed(PATIENT, 'DepressiveEpisode', WEEKS),
    History(PATIENT, 'DepressionCount', 2), # Note: Count >= 2 for past episodes
)

# Common mood episode types
Diagnosis(PATIENT, 'Depressive') <= conde(
    Observed(PATIENT, 'DepressiveEpisode', WEEKS),
    (WEEKS >= 2), # Note: 2 weeks is the minimum duration for Depression in ICD-11 CDDR
)

Diagnosis(PATIENT, 'Manic') <= conde(
    Observed(PATIENT, 'ManicEpisode', WEEKS),
    (WEEKS >= 7), # Note: 7 days is the minimum duration for Mania in ICD-11 CDDR
)

Diagnosis(PATIENT, 'Mixed') <= conde(
    Observed(PATIENT, 'MixedEpisode', WEEKS),
    (WEEKS >= 2), # Note: 2 weeks is the minimum duration for Mixed Episode in ICD-11 CDDR
)

Diagnosis(PATIENT, 'Hypomanic') <= conde(
    Observed(PATIENT, 'HypomanicEpisode', WEEKS),
    (WEEKS >= 4), # Note: 4 days is the minimum duration for Hypomania in ICD-11 CDDR
)

# Common condition names for History relation
facts([PATIENT, 'DepressionCount'], ['Depression', 2]) | facts([PATIENT, 'ManiaCount'], ['Mania', 1])
fats([PATIENT, 'HypomaniaCount'], ['Hypomania', 1])

# Relevant symptom names for Observed relation
symptoms = ['DepressiveEpisode', 'ManicEpisode', 'MixedEpisode', 'HypomanicEpisode']

# Repeated conjunctions for mood episode condition
for sym in symptoms:
    Diagnosis(PATIENT, 'BipolarI') | Diagnosis(PATIENT, 'BipolarII') | Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') | Diagnosis(PATIENT, 'RecurrentDepressiveDisorder')
    & membero(SYM1, symptoms) & (WEEKS >= 2)
    | Diagnosis(PATIENT, 'Depressive') | Diagnosis(PATIENT, 'Manic') | Diagnosis(PATIENT, 'Mixed') | Diagnosis(PATIENT, 'Hypomanic')

# Relevant condition names for History relation
conditions = ['Depression', 'Mania', 'Hypomania']

# Repeated conjunctions for mood disorder condition
for cond in conditions:
    Diagnosis(PATIENT, 'BipolarI') | Diagnosis(PATIENT, 'BipolarII') | Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') | Diagnosis(PATIENT, 'RecurrentDepressiveDisorder')
    & conde(
        History(PATIENT, cond, 1),
        History(PATIENT, 'ManiaCount', 0), # Note: No Mania episodes in the past
        History(PATIENT, 'HypomaniaCount', 0) # Note: No Hypomania episodes in the past
    )
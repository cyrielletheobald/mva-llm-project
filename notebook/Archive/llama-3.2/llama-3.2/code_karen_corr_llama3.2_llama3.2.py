from kanren import Relation, facts, var, run, conde, membero

# Declare relations
Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Variables
PATIENT, WEEKS = var(), var()
SYM1, SYM2, SYM3, SYM4, SYM5, SYM6 = var(), var(), var(), var(), var(), var()
MANIC, MIXED, HYPOMANIC = var(), var(), var()

# Rule logic
# Bipolar I
Diagnosis(PATIENT, 'BipolarI') <= conde(
    (
        Observed(PATIENT, 'Manic', WEEKS),
        (WEEKS >= 7)
    ),
    Observed(PATIENT, 'Mixed', WEEKS), (WEEKS >= 3) # OR condition
) & membero(SYM1, ['DepressedMood', 'Anhedonia', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])

Diagnosis(PATIENT, 'BipolarII') <= conde(
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    Observed(PATIENT, 'Hypomanic', WEEKS), (WEEKS >= 4) # OR condition
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])

# Single Episode Depressive Disorder
Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') <= conde(
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    History(PATIENT, 'DepressiveEpisode')
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])

# Recurrent Depressive Disorder
Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= conde(
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    History(PATIENT, 'DepressiveEpisode')
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
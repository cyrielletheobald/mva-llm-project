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
    # Mood Episode criterion: Manic episode
    (
        Observed(PATIENT, 'Manic', WEEKS),
        (WEEKS >= 7)
    ),
    # Mood Episode criterion: Mixed episode
    (
        Observed(PATIENT, 'Mixed', WEEKS),
        (WEEKS >= 3)
    ),
    # Mood Episode criterion: Hypomanic episode
    (
        Observed(PATIENT, 'Hypomanic', WEEKS),
        (WEEKS >= 4)
    )
) & membero(SYM1, ['DepressedMood', 'Anhedonia', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
# Bipolar II
Diagnosis(PATIENT, 'BipolarII') <= conde(
    # Mood Episode criterion: Depressive episode
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    # Mood Episode criterion: Hypomanic episode
    (
        Observed(PATIENT, 'Hypomanic', WEEKS),
        (WEEKS >= 4)
    )
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])

# Single Episode Depressive Disorder
Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') <= conde(
    # Mood Disorder criterion: DepressedMood episode
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    # History relation for relevant condition names
    (
        History(PATIENT, 'DepressiveEpisode')
    )
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])

# Recurrent Depressive Disorder
Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= conde(
    # Mood Disorder criterion: DepressedMood episode
    (
        Observed(PATIENT, 'DepressedMood', WEEKS),
        (WEEKS >= 2)
    ),
    # History relation for relevant condition names
    (
        History(PATIENT, 'DepressiveEpisode')
    )
) & membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
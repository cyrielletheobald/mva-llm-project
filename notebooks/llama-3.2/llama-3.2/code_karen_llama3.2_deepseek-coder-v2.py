from kanren import Relation, facts, var, run, conde, membero

# Declare relations
Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Variables
PATIENT, WEEKS = var(), var()
SYM1, SYM2, SYM3, SYM4, SYM5, SYM6 = var(), var(), var(), var(), var(), var()

# Rule logic for Bipolar I
BipolarI = Diagnosis(PATIENT, 'BipolarI') <= conde(
    # Mood Episode criterion: Depressive Episode with WEEKS >= 2
    Observed(PATIENT, 'DepressedMood', WEEKS) & (WEEKS >= 2),
    # Additional symptom criteria for Bipolar I
    membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM2, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM3, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
)

# Rule logic for Bipolar II
BipolarII = Diagnosis(PATIENT, 'BipolarII') <= conde(
    # Mood Episode criterion: Hypomanic Episode with WEEKS >= 2
    Observed(PATIENT, 'ManicHypomania', WEEKS) & (WEEKS >= 2),
    # Additional symptom criteria for Bipolar II
    membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM2, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM3, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
)

# Rule logic for Single Episode Depressive Disorder
SingleEpisodeDepressiveDisorder = Diagnosis(PATIENT, 'SingleEpisodeDepressiveDisorder') <= conde(
    # Mood Episode criterion: Depressive Episode with WEEKS >= 2
    Observed(PATIENT, 'DepressedMood', WEEKS) & (WEEKS >= 2),
    # Additional symptom criteria for Single Episode Depressive Disorder
    membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM2, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM3, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
)

# Rule logic for Recurrent Depressive Disorder
RecurrentDepressiveDisorder = Diagnosis(PATIENT, 'RecurrentDepressiveDisorder') <= conde(
    # Mood Episode criterion: Depressive Episode with WEEKS >= 2 in the last 3 months
    Observed(PATIENT, 'DepressedMood', WEEKS) & (WEEKS >= 2) & (observed_in_last_3_months(PATIENT, 'DepressedMood')),
    # Additional symptom criteria for Recurrent Depressive Disorder
    membero(SYM1, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM2, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation']) & membero(SYM3, ['Fatigue', 'SleepDisturbance', 'AppetiteChange', 'FeelingsOfWorthlessness', 'DifficultyConcentrating', 'SuicidalIdeation'])
)

# Function to check if an event occurred in the last 3 months
def observed_in_last_3_months(PATIENT, EVENT):
    return facts(PATIENT).count_EVENT(Event, WEEKS, 0, 3) > 0

# History relation for past conditions
History(PATIENT) <= conde(
    BipolarI & conde(observed_in_last_3_months(PATIENT, 'BipolarI')),
    BipolarII & conde(observed_in_last_3_months(PATIENT, 'BipolarII')),
    SingleEpisodeDepressiveDisorder & conde(observed_in_last_3_months(PATIENT, 'SingleEpisodeDepressiveDisorder')),
    RecurrentDepressiveDisorder & conde(observed_in_last_3_months(PATIENT, 'RecurrentDepressiveDisorder'))
)
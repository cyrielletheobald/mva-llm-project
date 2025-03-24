from kanren import Relation, facts, var, run, conde, membero

# Declare relations
Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Variables
PATIENT, WEEKS = var(), var()
SYM1, SYM2, SYM3, SYM4 = var(), var(), var(), var()
DISORDER = var()

# Rule logic for mood episodes
mood_episodes = conde(
    # DepressiveEpisode
    Observed(PATIENT, 'DepressedMood', WEEKS),
    (WEEKS >= 2),
), membero(mood_episodes, ['DepressiveEpisode'])

mood_episodes = conde(
    # ManicEpisode
    Observed(PATIENT, 'ManicMood', WEEKS),
    (WEEKS >= 4),
), membero(mood_episodes, ['ManicEpisode'])

mood_episodes = conde(
    # MixedEpisode
    Observed(PATIENT, 'MixedMood', WEEKS),
    (WEEKS >= 2),
), membero(mood_episodes, ['MixedEpisode'])

mood_episodes = conde(
    # HypomanicEpisode
    Observed(PATIENT, 'HypomanicMood', WEEKS),
    (WEEKS >= 4),
), membero(mood_episodes, ['HypomanicEpisode'])

# Rule logic for mood disorders
bipolar_i = conde(
    mood_episodes,
    History(PATIENT, 'BipolarIHistory'),
    Facts(PATIENT, 'MoodStable')
) & Observed(PATIENT, 'MoodStability', WEEKS)

bipolar_ii = conde(
    mood_episodes,
    History(PATIENT, 'BipolarIIHistory'),
    Facts(PATIENT, 'MoodStability')
) & membero(Observed(PATIENT, 'MoodStability', WEEKS), ['MoodStable'])

single_episode_depressive_disorder = conde(
    mood_episodes,
    History(PATIENT, 'SingleEpisodeDepressiveHistory'),
    Facts(PATIENT, 'MoodStable')
) & Observed(PATIENT, 'MoodStability', WEEKS)

recurrent_depressive_disorder = conde(
    mood_episodes,
    History(PATIENT, 'RecurrentDepressiveHistory'),
    Facts(PATIENT, 'MoodStable')
) & membero(Observed(PATIENT, 'MoodStability', WEEKS), ['MoodStable'])

# Rule for diagnosis
Diagnosis(PATIENT, 'BipolarI') == conde(
    (bipolar_i & Facts(PATIENT, 'PreviousManicEpisode') & Facts(PATIENT, 'HypomanicEpisode')),
    History(PATIENT, 'BipolarIHistory')
)

Diagnosis(PATIENT, 'BipolarII') == conde(
    (bipolar_ii),
    History(PATIENT, 'BipolarIIHistory')
)

Diagnosis(PATIENT, 'Single Episode Depressive Disorder') == conde(
    single_episode_depressive_disorder,
    History(PATIENT, 'SingleEpisodeDepressiveHistory')
)

Diagnosis(PATIENT, 'Recurrent Depressive Disorder') == conde(
    recurrent_depressive_disorder,
    History(PATIENT, 'RecurrentDepressiveHistory')
)
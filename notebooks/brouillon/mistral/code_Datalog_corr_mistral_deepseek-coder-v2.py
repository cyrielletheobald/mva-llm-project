from pyDatalog import *

# Declare relations
Observed = Relation('observed')
History = Relation('history')
Diagnosis = Relation('diagnosis')
EpisodeDuration = Relation('episode_duration')

# Define rules for each mood episode
def depressive_episode(P, WEEKS): rule(DepressiveEpisod, P, WEEKS) <= (Observed(P, 'Depressive', WEEKS), WEEKS >= 3)
def manic_episode(P, WEEKS): rule(ManicEpisod, P, WEEKS) <= (Observed(P, 'Manic', WEEKS), WEEKS >= 3)
def mixed_episode(P, WEEKS): rule(MixedEpisod, P, WEEKS) <= (Observed(P, 'Mixed', WEEKS), WEEKS >= 3)
def hypomanic_episode(P, WEEKS): rule(HypomanicEpisod, P, WEEKS) <= (Observed(P, 'Hypomanic', WEEKS), WEEKS >= 3)

# Define rules for each disorder
def bipolar_I(P): rule(Diagnosis(P, 'Bipolar I')) <= and_(duration_requirement('Bipolar I'), at_least_one_episode(['Depressive', 'Manic', 'Mixed'], P))
def bipolar_II(P): rule(Diagnosis(P, 'Bipolar II')) <= and_(duration_requirement('Bipolar II'), at_least_one_episode(['Depressive', 'Manic'], P), has_history('Recurrent Depressive Disorder', P))
def single_episode_depressive_disorder(P): rule(Diagnosis(P, 'Single Episode Depressive Disorder')) <= and_(duration_requirement('Single Episode Depressive Disorder'), at_least_one_episode(['Depressive'], P))
def recurrent_depressive_disorder(P): rule(Diagnosis(P, 'Recurrent Depressive Disorder')) <= and_(duration_requirement('Recurrent Depressive Disorder'), has_history('Depressive Episode', P))

# Duration requirements for each disorder
fact(duration_requirement('Bipolar I'), 6)
fact(duration_requirement('Bipolar II'), 6)
fact(duration_requirement('Single Episode Depressive Disorder'), 6)
fact(duration_requirement('Recurrent Depressive Disorder'), 12)

# Helper functions to check if a patient has at least one episode of the required type(s)
def at_least_one_episode(types, P): rule(*[EpisodeType == types for EpisodeType in types]) <= (Observed(P, EpisodeType, var()) for EpisodeType in types)

# Helper function to check if a patient has a history of a specific condition
def has_history(condition, P): rule() <= History(P, condition)

# Example usage:
# run(100, *[P, D] for D in Diagnosis.factbase for P in Person.factbase if bipolar_I(P) or bipolar_II(P))
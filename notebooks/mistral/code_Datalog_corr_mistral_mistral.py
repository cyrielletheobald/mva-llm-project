from kanren import Relation, var, run, and_, conde

   # Declare relations
   Observed = Relation('observed')
   History = Relation('history')
   Diagnosis = Relation('diagnosis')
   EpisodeDuration = Relation('episode_duration')

   # Define rules for each mood episode
   def depressive_episode(P, WEEKS): rule(EpisodeDuration((P, 'Depressive'), WEEKS))
   def manic_episode(P, WEEKS): rule(EpisodeDuration((P, 'Manic'), WEEKS))
   def mixed_episode(P, WEEKS): rule(EpisodeDuration((P, 'Mixed'), WEEKS))
   def hypomanic_episode(P, WEEKS): rule(EpisodeDuration((P, 'Hypomanic'), WEEKS))

   # Define rules for each disorder
   P, WEEKS = var(), var()

   def bipolar_I(P): rule(Diagnosis(P, 'Bipolar I'), and_(
       (duration_requirement('Bipolar I')),
       (at_least_one_episode(['Depressive', 'Manic', 'Mixed'], P))
   ))
   def bipolar_II(P): rule(Diagnosis(P, 'Bipolar II'), and_(
       (duration_requirement('Bipolar II')),
       (at_least_one_episode(['Depressive', 'Manic'], P)),
       (has_history('Recurrent Depressive Disorder', P))
   ))
   def single_episode_depressive_disorder(P): rule(Diagnosis(P, 'Single Episode Depressive Disorder'), and_(
       (duration_requirement('Single Episode Depressive Disorder')),
       (at_least_one_episode(['Depressive'], P))
   ))
   def recurrent_depressive_disorder(P): rule(Diagnosis(P, 'Recurrent Depressive Disorder'), and_(
       (duration_requirement('Recurrent Depressive Disorder')),
       (has_history('Depressive Episode', P))
   ))

   # Duration requirements for each disorder
   def duration_requirement(disorder): fact()

   # Helper functions to check if a patient has at least one episode of the required type(s)
   def at_least_one_episode(types, P): rule(EpisodeDuration((P, _), _) for _ in types)

   # Helper function to check if a patient has a history of a specific condition
   def has_history(condition, P): rule(History((P, condition)))
from kanren import Relation, facts, var, conj, conde

Observed = Relation()
History = Relation()
Diagnosis = Relation()

# Create facts
facts(Observed, [(var('PATIENT'), 'Mania', 2)]) # Create a fact for mania episode with patient and duration of 2 weeks
facts(Diagnosis) # Create an empty set of diagnoses

PATIENT, WEEKS = var(), var()
Diagnosis(PATIENT, 'ManicEpisode') # rule definition to be completed depending on logic
Observed(PATIENT, 'Mania', WEEKS)

# Define the rule using conde()
conde(
    conj(Observed(var('P'), 'Mania', 2), 
         conj(Diagnosis(var('P')), 
              conj(Var(), 'ManicEpisode'))),
    conj(Observed(var('P'), 'Depression', 3)),
    conj(Diagnosis(var('P')), 'Depressed')
)
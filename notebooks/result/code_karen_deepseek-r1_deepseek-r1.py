# Bipolar I Disorder (MDD)
Diagnosis(PATIENT, 'Bipolar I Disorder') & (
    # Mood Episode criterion: Manic or Hypomanic episode with at least 2 weeks of occurrence
    conde(
        ([
            (MoodEpisode(EpisodeType='Manic', Duration=2),
            (MoodEpisode(EpisodeType='Hypomanic', Duration=2))
        ], 'Mood Episode Duration >=2 weeks')
        
        # Mood Disorder criterion: Bipolar I-specific features
        & membero(
            # 1 manic episode or hypomanic episode with two items from Manic-like symptoms (A, B, C, D)
            item1=one_of(['Manic Episode', 'Hypomanic Episode']),
            item2=two_from(['Manic-like features', 'Hypomanic-like features'])
        )
        
        # Total mood disorder criteria: 3 items from Manic-like symptoms (A,B,C), two items from manic-like features, one item from hypomanic-like features
        & three_from(['Manic-like features', 'Hypomanic-like features'])
        
        # Combined symptom count for mood episode and mood disorder
        SymptomCount=4
    )
)

# Bipolar II Disorder (MDD)
Diagnosis(PATIENT, 'Bipolar II Disorder') & (
    # Mood Episode criterion: Manic-like symptoms with at least 2 weeks of occurrence
    conde(
        [
            MoodEpisode(EpisodeType='Manic-like', Duration=2)
        ],
        'Mood Episode Duration >=2 weeks'
        
        # Mood Disorder criterion: Bipolar II-specific features
        & membero(
            item1=two_from(['Manic-like features']),
            item2=one_from(['Hypomanic-like features']), 
            item3=one_from(['Depressive-like features'])
        )
        
        # Combined mood disorder criteria: 4 items from Manic-like and hypomanic-like symptoms
        SymptomCount=4
    )

# Single Episode Depressive Disorder (SED)
Diagnosis(PATIENT, 'Single Episode Depressive Disorder') & (
    # Mood Episode criterion: Depressive episode with at least 2 weeks of duration
    conde(
        [
            MoodEpisode(EpisodeType='Depressive', Duration=2)
        ],
        'Mood Episode Duration >=2 weeks'
        
        # Mood Disorder criterion: Single episode with four auxiliary symptoms and no manic episodes
        & membero(
            item1=one_from(['Depressive-like features']),
            item2=four_from(['Symptom A', 'Symptom B', 'Symptom C', 'Symptom D'])
        )
        
        # No manic or hypomanic episodes (implicit in SED criteria)
    )

# Recurrent Depressive Disorder (RDD) 
Diagnosis(PATIENT, 'Recurrent Depressive Disorder') & (
    # Mood Episode criterion: Two or more depressive episodes each with at least 2 weeks of duration
    conde(
        [
            # First depressive episode
            conde([MoodEpisode(EpisodeType='Depressive', Duration=2)], 'Duration >=2 weeks'),
            
            # Second depressive episode (after at least one week)
            conde([
                MoodEpisode(EpisodeType='Depressive', StartTime>?1),
                MoodEpisode(EpisodeType='Depressive', Duration=2)
            ], 'Duration >=2 weeks')
        ],
        'Mood Episode Duration criteria met for both episodes'
        
        # Additional symptoms
        SymptomCount=3
    )

# Helper functions (not actual code, but used to represent logic):
# conde(conditionals) - Creates a condition from an array of conditions
# membero(item1, item2,...) - Checks if the input matches any value in the list
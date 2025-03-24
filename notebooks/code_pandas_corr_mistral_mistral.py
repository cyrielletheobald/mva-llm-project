```python
   def diagnose(row):
       symptoms = row['Observed_Symptom'].tolist()
       history_conditions = row['History_Condition'].to_list()
       history_counts = row['History_Count'].to_list()

       conditions_map = {'Depression': True, 'Mood Swings': True}
       symptoms_filtered = [sym for sym in symptoms if cond in conditions_map and sym != 'Cond']  # Ignore the 'Cond' value

       if sum(history_counts) >= 4:
           if len(set(history_conditions)) == 1:
               return ['RecurrentDepressiveDisorder']
           else:
               return ['BipolarI']
       elif any([sym in ['Mania', 'Hypomania'] for sym in symptoms]):
           if any([history_conditions.count(cond) > 0 for cond in ['Depression']]):
               return ['BipolarII']
           elif len(set(history_conditions)) == 1:
               return ['SingleEpisodeDepressiveDisorder']
       else:
           return ['No diagnosis']
   ```
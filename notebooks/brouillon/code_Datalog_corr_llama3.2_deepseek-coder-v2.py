from pyDatalog import pyDatalog

# Clear any previously defined terms or rules
pyDatalog.clear()

# Define terms used in the rule
pyDatalog.create_terms('PATIENT, WEEKS, Observed, ManicEpisode')

# Define a custom function for comparison since pyDatalog does not support float comparisons directly
def sup(x, y):
    return x >= y

# Register the custom function with pyDatalog
pyDatalog.create_operator('>=', 2, infix=sup)

# Rule to define ManicEpisode
ManicEpisode(PATIENT) <= Observed(PATIENT, 'Mania', WEEKS) & (WEEKS >= 3.0)

from pomegranate import *

B = DiscreteDistribution({'burglary':0.001, '~burglary': 0.999})
E = DiscreteDistribution({'earth':0.002, '~earth': 0.998})

A = ConditionalProbabilityTable([['burglary', 'earth', 'alarm', 0.95], ['burglary', '~earth', 'alarm', 0.94], 
['~burglary', 'earth', 'alarm', 0.29], ['~burglary', '~earth', 'alarm', 0.001],
['burglary', 'earth', '~alarm', 0.05], ['burglary', '~earth', '~alarm', 0.06], 
['~burglary', 'earth', '~alarm', 0.71], ['~burglary', '~earth', '~alarm', 0.999]], 
[B, E])

J = ConditionalProbabilityTable([['alarm', 'john', 0.90], ['~alarm', 'john', 0.05],['alarm', '~john', 0.10], ['~alarm', '~john', 0.95]], 
# ['~burglary', 'earth', 'alarm', 0.29], ['~burglary', '~earth', '~alarm', 0.001]],
# ['sunny', '~raise', 'happy', 0.7], ['sunny', '~raise', '~happy', 0.3], 
# ['~sunny', '~raise', 'happy', 0.1], ['~sunny', '~raise', '~happy', 0.9]], 
[A])

M = ConditionalProbabilityTable([['alarm', 'mary', 0.70], ['~alarm', 'mary', 0.01],['alarm', '~mary', 0.3], ['~alarm', '~mary', 0.99]], 
#['~burglary', 'earth', 'alarm', 0.29], ['~burglary', '~earth', '~alarm', 0.001]],
# ['sunny', '~raise', 'happy', 0.7], ['sunny', '~raise', '~happy', 0.3], 
# ['~sunny', '~raise', 'happy', 0.1], ['~sunny', '~raise', '~happy', 0.9]], 
[A])

s_burg = State(B, 'burg')
s_earth = State(E, 'ear')
s_alarm = State(A, 'ala')
s_john = State(J, 'joh')
s_mary = State(M, 'mar')

modela = BayesianNetwork('Day4 Pop Quiz')

modela.add_states(s_burg, s_earth, s_alarm, s_john, s_mary)

modela.add_transition(s_burg, s_alarm)
modela.add_transition(s_earth, s_alarm)
modela.add_transition(s_alarm, s_john)
modela.add_transition(s_alarm, s_mary)

modela.bake()  #finalize

print ('The number of nodes:', modela.node_count())
print ('The number of edges:', modela.edge_count())

#given John and Mary, find Burglary
print(modela.predict_proba({'joh':'john', 'mar':'mary'})[0].parameters[0]['burglary'])
from pomegranate import *

Burglary = DiscreteDistribution({'burglary':.001, 'noburglary':.999})
Earthquake = DiscreteDistribution({'earthquake': 0.02, 'noearthquake': 0.998})


Alarm = ConditionalProbabilityTable([
['burglary', 'earthquake', 'alarm', .95],
['burglary', 'earthquake', 'noalarm', .05],
['burglary', 'noearthquake', 'alarm', .94],
['burglary', 'noearthquake', 'noalarm', .06],
['noburglary', 'earthquake', 'alarm', .29],
['noburglary', 'earthquake', 'noalarm', .61],
['noburglary', 'noearthquake', 'alarm', .001],
['noburglary', 'noearthquake', 'noalarm', .999],], [Burglary, Earthquake])

s_burglary = State(Burglary, ' got burglary')
s_earthquake = State(Earthquake, 'got earthquake')
s_alarm = State(Alarm, 'got alarm')


model = BayesianNetwork('topnetwork')


model.add_states(s_burglary, s_earthquake, s_alarm)


model.add_transition(s_burglary, s_alarm)
model.add_transition(s_earthquake, s_alarm)

model.bake() 

print()

print('The number of nodes:', model.node_count())
print('The number of edges:', model.edge_count())


# P(r | s)
print('P(r | s): ', model.predict_proba({'earthquake': 'earthquake'})[1].parameters[0]['earthquake'])



Graduated = DiscreteDistribution({'graduated':0.9, 'no-graduated':0.1})

Offer1 = ConditionalProbabilityTable([
['graduated', 'offer', 0.5],
['graduated', 'no-offer', 0.5],
['no-graduated', 'offer', 0.05],
['no-graduated', 'no-offer', 0.95]], [Graduated])

Offer2 = ConditionalProbabilityTable([
['graduated', 'offer', 0.75],
['graduated', 'no-offer', 0.25],
['no-graduated', 'offer', 0.25],
['no-graduated', 'no-offer', 0.75]], [Graduated])

s_graduated = State(Graduated, 'graduated-offer')
s_offer_1 = State(Offer1, 'offer_1')
s_offer_2 = State(Offer2, 'offer_2')

model = BayesianNetwork('graduated-offer')

model.add_states(s_graduated, s_offer_1, s_offer_2)

model.add_transition(s_graduated, s_offer_1)
model.add_transition(s_graduated, s_offer_2)

model.bake()

print()
print('The number of nodes:', model.node_count())
print('The number of edges:', model.edge_count())

# P(o2 | g, ~o1)
print('P(o2 | g, ~o1): ', model.predict_proba({'graduated-offer': 'graduated', 'offer_1': 'no-offer'})[2].parameters[0]['offer'])


# P(g | o1, o2)
print('P(g | o1, o2): ', model.predict_proba({'offer_1': 'offer', 'offer_2': 'offer'})[0].parameters[0]['graduated'])


# P(g | ~o1, o2)
print('P(g | ~o1, o2): ', model.predict_proba({'offer_1': 'no-offer', 'offer_2': 'offer'})[0].parameters[0]['graduated'])


# P(g | ~o1, ~o2)
print('P(g | ~o1, ~o2): ', model.predict_proba({'offer_1': 'no-offer', 'offer_2': 'no-offer'})[0].parameters[0]['graduated'])


# P(o2 | o1)
print('P(o2 | o1): ', model.predict_proba({'offer_1': 'offer'})[2].parameters[0]['offer'])

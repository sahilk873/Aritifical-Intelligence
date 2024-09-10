from pomegranate import *


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

Sunny = DiscreteDistribution({'sunny':0.7, 'not-sunny':0.3})
Raise = DiscreteDistribution({'raise': 0.01, 'no-raise': 0.99})


Happiness = ConditionalProbabilityTable([
['sunny', 'raise', 'happy', 1],
['sunny', 'raise', 'not-happy', 0],
['sunny', 'no-raise', 'happy', 0.7],
['sunny', 'no-raise', 'not-happy', 0.3],
['not-sunny', 'raise', 'happy', 0.9],
['not-sunny', 'raise', 'not-happy', 0.1],
['not-sunny', 'no-raise', 'happy', 0.1],
['not-sunny', 'no-raise', 'not-happy', 0.9]], [Sunny, Raise])

s_sunny = State(Sunny, 'is-sunny')
s_raise = State(Raise, 'got-raise')
s_happiness = State(Happiness, 'happiness')


model = BayesianNetwork('happiness-network')


model.add_states(s_sunny, s_raise, s_happiness)


model.add_transition(s_sunny, s_happiness)
model.add_transition(s_raise, s_happiness)

model.bake() 

print()

print('The number of nodes:', model.node_count())
print('The number of edges:', model.edge_count())


# P(r | s)
print('P(r | s): ', model.predict_proba({'is-sunny': 'sunny'})[1].parameters[0]['raise'])


# P(r | h, s)
print('P(r | h, s): ', model.predict_proba({'is-sunny': 'sunny', 'happiness': 'happy'})[1].parameters[0]['raise'])


# P(r | h)
print('P(r | h): ', model.predict_proba({'happiness': 'happy'})[1].parameters[0]['raise'])


# P(r | h, ~s)
print('P(r | h, ~s): ', model.predict_proba({'is-sunny': 'not-sunny', 'happiness': 'happy'})[1].parameters[0]['raise'])
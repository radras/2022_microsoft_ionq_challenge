# Quantum Marcher

Adventurous way of learning about training variational circuits.
Challenge: march down the hill before the storm strikes. 

# Team Hike

#Concepts Players can Learn from Quantum Macrher

Variational quantum algorithms are a promising tool for near term quantum computers to achieve quantum advantage. By nature they are hybrid: partly quantum and partly classical. Quantum Macher is a game that essentially helps the user visualize the training of the variational circuit's parameters when gradient descent is used as the classical optimizer. 

Gradient descent is essentially the process of finding a local minimum. In our case however, the main difference is that the player can see the entire landscape instead of just the possible "steps" (or gradients) immediately around them. The purpose of this is to show the user how they can find a more direct path for a low number of parameters, but how doing so becomes increasingly difficult.


# How to Play 


Essentially, the player has to navigate a terrain (top down view) that ranges in height. Their goal is to get to the maximum height (1). If they run out of time, the game is over. While the beginning levels seem easy, finding the global maximum is quite challenging as the numbers of parameters increase.
For example, for training 3 parameters, the following process is followed: 

Next Steps: 

Adding the following features woul



## Running the project

To install required packages run

`pip install -r requirements.txt`

Run the game using

`python ./QuantumMarcher/hike.py`


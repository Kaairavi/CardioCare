import pickle
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# 1. Create a simple dummy model (looks for a pattern y = 2x)
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

model = LinearRegression()
model.fit(X, y)

# 2. Create the 'model' folder if it doesn't exist
if not os.path.exists('model'):
    os.makedirs('model')

# 3. Save the model
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Success! model/model.pkl has been created.")
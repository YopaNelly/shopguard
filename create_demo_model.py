import numpy as np
import pickle
import os

# Create a simple rule-based "model" that works for demonstration
class DemoModel:
    def __init__(self):
        self.input_shape = (16, 128, 128, 3)
        
    def predict(self, sequences, verbose=0):
        """Simulate predictions based on motion detection logic"""
        predictions = []
        for seq in sequences:
            # Calculate "motion intensity" as simple demo logic
            motion_score = np.std(seq) * 10
            # Simulate probability (biased towards normal behavior)
            prob = min(0.9, max(0.1, motion_score * 0.3 + np.random.rand() * 0.2))
            predictions.append([prob])
        return np.array(predictions)

# Save the demo model
os.makedirs('models', exist_ok=True)
model = DemoModel()
with open('models/demo_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Demo model created successfully!")

import pickle
import pandas as pd
import sklearn.compose._column_transformer as ct

class _RemainderColsList(list):
    def __setstate__(self,state):
        self.__dict__.update(state)
        
ct._RemainderColsList = _RemainderColsList

with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)
    
class_labels = model.classes_.tolist()

def predict_output(user_input: dict):
    
    input_df = pd.DataFrame([user_input])
    
    predicted_class = model.predict(input_df)[0]
    
    # Get probabilities of all classes
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)
    
    # create mapping  : {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
    
    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence,4),
        "class_probabilities": class_probs 
    }
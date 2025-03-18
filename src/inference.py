import ollama
from src.dataprep import get_prompt_patient_data, system

def get_answer(patient_id, model='mistral'):
    observed, history_conditions, mood_episodes = get_prompt_patient_data(patient_id) 
    user = f'For brevity, please output only the diagnosis for the following patients. Patients with no clear diagnosis should be indicated as such. {observed}, {history_conditions}'
    response = ollama.chat(
    model=model,
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ])
    return response['message'].content
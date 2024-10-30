import pickle
from collections import defaultdict




simple_motor_list = []
for rl in ['R','L']:
    for bd in ['Finger','Hand','Elbow','Arm','Foot','Ankle','Knee','Hip','Flank','Chest','Lip','Cheek','Eyebrow']:
        for mv in ['Myoclonus','Clonus','Tonic']:
            simple_motor_list.append('-'.join([rl,bd,mv]))
            
            
complex_motor_list = []
for rl in ['R','L']:
    for bd in ['Finger','Hand','Elbow','Arm','Foot','Ankle','Knee','Hip','Flank','Chest','Lip','Cheek','Eyebrow']:
        for mv in ['Automatism','Voluntary movement']:
            complex_motor_list.append('-'.join([rl,bd,mv]))
                     
sensory_list = []
for rl in ['R','L']:
    for bd in ['Finger','Hand','Elbow','Arm','Foot','Ankle','Knee','Hip','Flank','Chest','Lip','Cheek','Eyebrow']:
        for sn in ['Numbness','Tingling','Bubbly','Tightness','Burning','Pressure','Warmth','Cold','Pain','Itchiness','Vibration','Electric','Tickle','Deep Pressure','Light Touch']:
            sensory_list.append('-'.join([rl,bd,sn]))
            

language_list = ['Comprehension','Naming']

speech_list = ['Repetition']

vision_list = ['Phosphenes', 'Evoked Color','Suppressed Color']

emotion_list = ['Euphoria','Laughter','Sense of peace','Anxiety','Fear','Sadness','Anger',]

cognitive_list = ['Flashbacks of specific memories','Deja Vu', 'Jamais Vu','Amnesia']

consciousness_list = ['Out of body experience','Lethary','Loss of consciousness','Dissociation','Altered sense of self']

autonomic_list = ['Tachycardia','Bradycardia','Tachypnea','Bradypnea','Deep breath','Respiratory arrest','Nausea','Hyperhidrosis','Pupil dilation','Pupil constriction']

auditory_list = ['Change in pitch perception','Hearing simple sounds','Hearing words']

vestibular_list = ['Being pulled','Being_pushed','Vertigo','Impaired proprioception']

olfactory_list = ['Olfactory hallucination']

gustatory_list = ['Gustatory hallucination']


behaviors_dict = {
    '':[],
    'Speech':speech_list,
    'Language':language_list,
    'Simple Motor': simple_motor_list,
    'Complex Motor': complex_motor_list,
    'Sensory':sensory_list, 
    'Consciousness':consciousness_list,
    'Emotion':emotion_list,
    'Cognitive':cognitive_list,
    'Vision':vision_list,
    'Auditory':auditory_list,
    'Vestibular':vestibular_list,
    'Olfactory':olfactory_list,
    'Gustatory':gustatory_list,
    'Autonomic':autonomic_list,
    }


with open('behaviors_dict.pickle','wb') as f:
    pickle.dump(behaviors_dict,f)
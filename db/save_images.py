import os
from models.chat_models import AnalyseLCRequest
from models.state import State
import base64



def save_images(state:State):
    doc_id = state['documents'].id
    os.makedirs(f'output/{doc_id}', exist_ok=True)
    paths = list[str]
    for index,image in enumerate(state['images']):
        image_data = base64.b64decode(image)
        path = f'output/{doc_id}/{index}.png'
        paths.append(path)
        with open(path,'wb') as f:
            f.write(image_data)
    return paths       
    
 
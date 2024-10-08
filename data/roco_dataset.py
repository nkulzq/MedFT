import os
import json

from torch.utils.data import Dataset
from torchvision.datasets.utils import download_url

from PIL import Image

from data.utils import pre_caption

class  roco_caption_train(Dataset):
    def __init__(self, transform, image_root, ann_root, max_words=30, prompt=''):        
        filename = 'ann_train.json'
        ann_ori = json.load(open(os.path.join(ann_root,filename),'r'))
        anns = []
        for ann in ann_ori:
            image_path = os.path.join(image_root,ann['image'])
            try:   
                image = Image.open(image_path).convert('RGB')
                anns.append(ann)
            except:
                print(ann['image'])
        self.annotation = anns
        self.transform = transform
        self.image_root = image_root
        self.max_words = max_words      
        self.prompt = prompt   
        
    def __len__(self):
        return len(self.annotation)
    
    def __getitem__(self, index):    
        
        ann = self.annotation[index]
        
        image_path = os.path.join(self.image_root,ann['image'])        
        image = Image.open(image_path).convert('RGB')   
        image = self.transform(image)
        
        caption = self.prompt+pre_caption(ann['caption'], self.max_words)
        img_id = ann['image'].split('/')[-1].strip('.jpg').split('_')[-1]
         
        return image, caption, int(img_id)
    
    
class roco_caption_eval(Dataset):
    def __init__(self, transform, image_root, ann_root, split):  
        filenames = {'val':'ann_validation.json','test':'ann_test.json'}        
        ann_ori = json.load(open(os.path.join(ann_root,filenames[split]),'r'))
        anns = []
        for ann in ann_ori:
            image_path = os.path.join(image_root,ann['image'])
            try:       
                image = Image.open(image_path).convert('RGB')
                anns.append(ann)
            except:
                print(ann['image'])
        self.annotation = anns
        self.transform = transform
        self.image_root = image_root
        
    def __len__(self):
        return len(self.annotation)
    
    def __getitem__(self, index):    
        
        ann = self.annotation[index]
        
        image_path = os.path.join(self.image_root,ann['image'])        
        image = Image.open(image_path).convert('RGB')   
        image = self.transform(image)          
        
        img_id = ann['image'].split('/')[-1].strip('.jpg').split('_')[-1]
        
        return image, int(img_id)   
import torch
from torchvision import datasets, transforms
import torch.utils.data as data
import os
from PIL import Image

base_transform = transforms.Compose([
    transforms.ToTensor(),
    #transforms.Normalize([0.5]*3, [0.5]*3)
    ])

def image_loader(path):
    img = Image.open(path)
    img_tensor = base_transform(img)
    return img_tensor

class FRDataset(data.Dataset):

    def __init__(self,dir,height,weight):
        self.file_dir = dir
        self.transform = base_transform
        #self.image_loader = image_loader()
        self.frames_set = os.listdir(self.file_dir)
        self.height = height
        self.weight = weight

    def __getitem__(self, index):

        frames = self.frames_set[index] #0266
        frame_tensor = torch.Tensor(size=(frame_counter, 3, self.height, self.weight))
        for img in frames:
            #file_dir_frames = self.file_dir + frames
            file_dir_frames = os.path.join(self.file_dir,frames)
            imgs_path = os.listdir(file_dir_frames)
            imgs_path.sort()
            i = 0
            for img in imgs_path:
                final_path = file_dir_frames + "/" + img
                #final_path = '/'.os.listdir(file_dir_frames,img)
                img_tensor = image_loader(final_path)
                #print(img_tensor.size())
                frame_tensor[i] = img_tensor
                i = i + 1
        return frame_tensor

    def __len__(self):
        return len(self.frames_set)

batch = 4 # batch size of the data every time for training
batch_number = 100000  # number of batches, so we totally have batch_number * batch images
frame_counter = 7 # number of frames per folder
LR_height = 64
LR_weight = 112
HR_height = 256
HR_weight = 448

train_dir_LR = 'Data/LR'
train_dir_HR = 'Data/HR'

FRData_LR = FRDataset(dir=train_dir_LR,weight=LR_weight,height=LR_height)
FRData_HR = FRDataset(dir=train_dir_HR,weight=HR_weight,height=HR_height)

data_loader_LR = data.DataLoader(FRData_LR, batch_size = batch, shuffle = True)
data_loader_HR = data.DataLoader(FRData_HR, batch_size = batch, shuffle = True)

#print(data_loader[0].size())

for i_batch, sample_batched in enumerate(zip(data_loader_LR,data_loader_HR)):
       #print(sample_batched)
       #print(data_loader_HR[i_batch].size())
       permuted_LR_data = sample_batched[0].permute(1, 0, 2, 3, 4)
       permuted_HR_data = sample_batched[1].permute(1, 0, 2, 3, 4) #labels
       #print(permuted_data.contiguous())
       print("LR:",permuted_LR_data.size())
       print("HR:",permuted_LR_data.size())


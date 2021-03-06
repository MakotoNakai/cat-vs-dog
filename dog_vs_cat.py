# -*- coding: utf-8 -*-
"""dog_vs_cat.ipynb

Automatically generated by Google Colaboratory.

I used 50,000 pics(dog.0.jpg~dog.25000.jpg,cat.0.jpg-cat.25000.jpg) 
from https://www.kaggle.com/c/dogs-vs-cats/data as the train data,
and 250 pics(1.jpg-100.jpg) as test data.
    
The file structure should be 

gdrive/  
        train6_25000pics.zip(the folder which contains data for training)
             /dog
                /dog.0.jpg
                 ...
                dog.25000.jpg
             /cat
                /cat.0.jpg
                ...
                /cat.25000.jpg
         
          test5_100pics.zip(the folder which contains data for testing)
            /dog
                /1.jpg
                ...
                50.jpg
            /cat
                /51.jpg
                ...
                /100.jpg
      
"""
#Get a connection between this program and Google Drive itself
from google.colab import drive
drive.mount('/content/gdrive')


#import libraries you are going to  use
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D,Activation, Dropout, Flatten, Dense
from keras.layers.normalization import BatchNormalization
from keras import backend as K

#Make sure that you are using GPU. You can go ahead if the output says "/device:GPU:0"
# You can start using GPU by Edit -> Network settings -> Hardware accelerator:GPU
print(tf.test.gpu_device_name())

#import libraries for get authorization
!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

#Get authorization to use data in your Google Drive
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

id1 = 'Put the share link of the training-data-folder '
id2 = 'Put the share link of the testing-data-folder '# 共有リンクで取得した id= より後の部分
downloaded1 = drive.CreateFile({'id': id1})
downloaded2 = drive.CreateFile({'id': id2})
downloaded1.GetContentFile('train6_25000pics.zip')
downloaded2.GetContentFile('test5_100pics.zip')


#Unzip these folders
!unzip train6_25000pics.zip
!unzip test5_100pics.zip

# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = "/content/train6(25000pics)"
validation_data_dir = "/content/test5(100pics)"
nb_train_samples = 25000
nb_validation_samples = 100
epochs = 250
batch_size = 100

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# In[3]:

#Create the model of the neural network
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2))
model.add(BatchNormalization())
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

#Save the model 
model.save_weights('ninth_25000pics_try.h5')

#Get the accracy of the model you've created.  You will get more than 99%
_,acc = model.evaluate_generator(validation_generator,steps=nb_validation_samples // batch_size)
print("accuracy:{:2f}".format(acc))




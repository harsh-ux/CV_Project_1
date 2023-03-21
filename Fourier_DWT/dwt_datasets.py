# -*- coding: utf-8 -*-
"""dwt_datasets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FPZr22w5GZfqIa6QJtjc1yVfKYIfLXSa
"""

import cv2
import numpy as np
import os
from scipy.fftpack import dct
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

import cv2
import numpy as np
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split

lfw_dataset = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
X = lfw_dataset.data
y = lfw_dataset.target
n_samples, height, width = lfw_dataset.images.shape
n_features = X.shape[1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

import pywt

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

def hu_moments(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return hu_moments.flatten()

X_train_processed = []
for img in X_train:
    img = img.reshape(height, width)
    LL, LH, HL, HH = dwt(img)
    features = np.hstack((cv2.HuMoments(cv2.moments(LL)).flatten(),
                          cv2.HuMoments(cv2.moments(LH)).flatten(),
                          cv2.HuMoments(cv2.moments(HL)).flatten(),
                          cv2.HuMoments(cv2.moments(HH)).flatten()))
    X_train_processed.append(features)

X_test_processed = []
for img in X_test:
    img = img.reshape(height, width)
    LL, LH, HL, HH = dwt(img)
    features = np.hstack((cv2.HuMoments(cv2.moments(LL)).flatten(),
                          cv2.HuMoments(cv2.moments(LH)).flatten(),
                          cv2.HuMoments(cv2.moments(HL)).flatten(),
                          cv2.HuMoments(cv2.moments(HH)).flatten()))
    X_test_processed.append(features)

def euclidean_distance(a, b):
    return np.sqrt(np.sum(np.square(a - b)))

correct = 0
for i in range(len(X_test_processed)):
    distances = []
    for j in range(len(X_train_processed)):
        distance = euclidean_distance(X_test_processed[i], X_train_processed[j])
        distances.append((distance, y_train[j]))
    distances.sort()
    prediction = distances[0][1]
    if prediction == y_test[i]:
        correct += 1

accuracy = (correct / len(X_test)) * 100
print("Accuracy: {:.2f}%".format(accuracy))

import matplotlib.pyplot as plt

n_images = 10
fig, axes = plt.subplots(nrows=1, ncols=n_images, figsize=(20, 20))
for i in range(n_images):
    axes[i].imshow(X_test[i].reshape(height, width), cmap='gray')
    axes[i].set_title("Prediction: {}".format(lfw_dataset.target_names[y_test[i]]), fontsize=10)
    axes[i].axis('off')

plt.subplots_adjust(wspace=0.8, hspace=0.5)
plt.show()

import cv2
import numpy as np
from sklearn.datasets import fetch_lfw_people
from matplotlib import pyplot as plt

lfw_dataset = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

height, width = lfw_dataset.images.shape[1:]

import pywt

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

def hu_moments(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return np.ravel(hu_moments)

n_images = 10
X_processed = []
fig, axes = plt.subplots(nrows=2, ncols=n_images, figsize=(20, 10))
for i in range(n_images):
    img = lfw_dataset.images[i]
    LL, LH, HL, HH = dwt(img)
    hu_LH = hu_moments(LH)
    hu_HL = hu_moments(HL)
    hu_HH = hu_moments(HH)
    X_processed.append(np.hstack((hu_LH, hu_HL, hu_HH)))
    axes[0, i].imshow(img, cmap='gray')
    axes[0, i].axis('off')
    axes[1, i].imshow(HH, cmap='gray')
    axes[1, i].axis('off')
plt.show()

# Print the processed images
print('Processed images:', X_processed)

!unzip /content/custom_dataset.zip

import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

path = 'custom_dataset'

height, width = 256, 256

import pywt

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

def hu_moments(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return np.ravel(hu_moments)

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pywt

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

def hu_moments(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return np.ravel(hu_moments)

custom_dataset_path = '/content/custom_dataset'

subfolder_names = os.listdir(custom_dataset_path)

X_processed = []
for name in subfolder_names:
    subfolder_path = os.path.join(custom_dataset_path, name)
    image_names = os.listdir(subfolder_path)
    if len(image_names) == 0:
        continue  
    for img_name in image_names:
        img_path = os.path.join(subfolder_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        LL, LH, HL, HH = dwt(img)
        hu_LH = hu_moments(LH)
        hu_HL = hu_moments(HL)
        hu_HH = hu_moments(HH)
        X_processed.append(np.hstack((hu_LH, hu_HL, hu_HH)))

n_images = min(len(X_processed), 5)
fig, axes = plt.subplots(nrows=2, ncols=n_images, figsize=(20, 10))
for i in range(n_images):
    subfolder_path = os.path.join(custom_dataset_path, subfolder_names[i])    image_names = os.listdir(subfolder_path)
    img_path = os.path.join(subfolder_path, image_names[0])
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    LL, LH, HL, HH = dwt(img)
    axes[0, i].imshow(img, cmap='gray')
    axes[0, i].axis('off')
    axes[1, i].imshow(HH, cmap='gray')
    axes[1, i].axis('off')
plt.show()

print('Processed images:', X_processed)

!mv /content/custom_dataset/collage /content

"""# minicelebA dataset"""

import numpy as np
import os
import cv2
import tarfile
from urllib.request import urlretrieve
from sklearn.model_selection import train_test_split

filename = "/content/ miniCelebA.tar.gz"
with tarfile.open(filename, "r:gz") as tar:
    tar.extractall()

X = []
y = []
for subject in os.listdir("att_faces"):
    for img_file in os.listdir(os.path.join("att_faces", subject)):
        img = cv2.imread(os.path.join("att_faces", subject, img_file), cv2.IMREAD_GRAYSCALE)
        X.append(img)
        y.append(int(subject[1:]) - 1) 

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

def hu_moments(img):
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments)
    return hu_moments.flatten()

X_train_processed = []
for img in X_train:
    LL, LH, HL, HH = dwt(img)
    features = np.hstack((hu_moments(LH), hu_moments(HL), hu_moments(HH)))
    X_train_processed.append(features)

X_test_processed = []
for img in X_test:
    LL, LH, HL, HH = dwt(img)
    features = np.hstack((hu_moments(LH), hu_moments(HL), hu_moments(HH)))
    X_test_processed.append(features)

def euclidean_distance(a, b):
    return np.sqrt(np.sum(np.square(a - b)))

correct = 0
for i in range(len(X_test_processed)):
    distances = []
    for j in range(len(X_train_processed)):
        distance = euclidean_distance(X_test_processed[i], X_train_processed[j])
        distances.append((distance, y_train[j]))
    distances.sort()
    prediction = distances[0][1]
    if prediction == y_test[i]:
        correct += 1

accuracy = (correct / len(X_test)) * 100
print("Accuracy: {:.2f}%".format(accuracy))

import matplotlib.pyplot as plt
import numpy as np
import tarfile

data = np.load("/content/minicelebA.npz")
X = data['X']
y = data['y']

unique_labels, counts = np.unique(y, return_counts=True)
plt.bar(unique_labels, counts)
plt.xlabel("Label")
plt.ylabel("Count")
plt.title("Label Distribution in minicelebA Dataset")
plt.show()

import cv2
import numpy as np
import pywt
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt

lfw_dataset = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
height, width = lfw_dataset.images.shape[1:]

def dwt(img):
    LL, (LH, HL, HH) = pywt.dwt2(img, 'haar')
    return LL, LH, HL, HH

idx = np.random.randint(len(lfw_dataset.images))
img = lfw_dataset.images[idx]
LL, LH, HL, HH = dwt(img)
features = np.hstack((LH.flatten(), HL.flatten(), HH.flatten()))

n_features = features.shape[0] // 3
features = features.reshape(3, n_features)
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 10))
titles = ['LH', 'HL', 'HH']
for i in range(3):
    f = features[i].reshape(HH.shape)
    axes[i].imshow(f, cmap='gray')
    axes[i].set_title(titles[i], fontsize=10)
    axes[i].axis('off')

fig, ax = plt.subplots()
ax.imshow(img, cmap='gray')
ax.set_title('Original image', fontsize=10)
ax.axis('off')
plt.show()
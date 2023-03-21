# -*- coding: utf-8 -*-
"""fourier_datasets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YMo2r4bCrG0-Gl98h1CD8qjS7_f2KvRv

#LFW Fourier Transform
"""

import numpy as np
  import cv2
  from sklearn.datasets import fetch_lfw_people
  from sklearn.model_selection import train_test_split
  from sklearn.svm import SVC
  from sklearn.metrics import accuracy_score
  lfw_people = fetch_lfw_people(min_faces_per_person=100, resize=0.5)
  X = lfw_people.data
  y = lfw_people.target

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

  from skimage.feature import local_binary_pattern

  X_train_lbp = local_binary_pattern(X_train, P=8, R=1)
  X_test_lbp = local_binary_pattern(X_test, P=8, R=1)

  X_train_fft = np.fft.fft2(X_train_lbp)
  X_test_fft = np.fft.fft2(X_test_lbp)

  X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
  X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])


  model = SVC(kernel='rbf')
  model.fit(X_train_features, y_train)


  X_train_fft = np.fft.fft2(X_train)
  X_test_fft = np.fft.fft2(X_test)

  X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
  X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])

  model = SVC(kernel='rbf')
  model.fit(X_train_features, y_train)

  y_pred = model.predict(X_test_features)

  accuracy = accuracy_score(y_test, y_pred)
  print('Accuracy:', accuracy)

import os
import numpy as np
from PIL import Image
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

dataset_path = "/content/custom_dataset"

file_paths = []
labels = []
for folder_name in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder_name)
    if os.path.isdir(folder_path):
        image_names = os.listdir(folder_path)
        for i in range(len(image_names) - 1):
            file_paths.append((os.path.join(folder_path, image_names[i]), os.path.join(folder_path, image_names[i+1])))
            labels.append(folder_name)

X = []
for file_path_pair in file_paths:
    image1 = Image.open(file_path_pair[0]).convert('L')
    image2 = Image.open(file_path_pair[1]).convert('L')
    X1 = np.fft.fft2(image1)
    X2 = np.fft.fft2(image2)
    X.append(np.hstack((np.abs(X1.flatten()), np.abs(X2.flatten()))))

X_train, X_test, y_train, y_test = train_test_split(X, labels, random_state=42)

model = SVC(kernel='linear')
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy}")

import numpy as np
import cv2
import matplotlib.pyplot as plt

images = []
for i in range(1, 6):
    img = cv2.imread(path, 0)
    images.append(img)

fft_images = []
for img in images:
    fft_img = np.fft.fft2(img)
    fft_images.append(fft_img)

fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(10, 20))
for i, (img, fft_img) in enumerate(zip(images, fft_images)):
    axs[i][0].imshow(img, cmap='gray')
    axs[i][0].set_title(f'Image {i+1}')
    axs[i][1].imshow(np.log(1+np.abs(fft_img)), cmap='gray')
    axs[i][1].set_title(f'Fourier Transform {i+1}')
plt.show()

import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_lfw_people

lfw_dataset = fetch_lfw_people(min_faces_per_person=70)

random_indexes = np.random.randint(0, lfw_dataset.data.shape[0], size=5)
images = lfw_dataset.data[random_indexes].reshape(-1, 62, 47)

fft_images = []
for img in images:
    fft_img = np.fft.fft2(img)
    fft_images.append(fft_img)

fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(10, 20))
for i, (img, fft_img) in enumerate(zip(images, fft_images)):
    axs[i][0].imshow(img, cmap='gray')
    axs[i][0].set_title(f'Image {i+1}')
    axs[i][1].imshow(np.log(1+np.abs(fft_img)), cmap='gray')
    axs[i][1].set_title(f'Fourier Transform {i+1}')
plt.show()

import numpy as np
import cv2
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from skimage.io import imread_collection

image_path = '/content/minicelebA/*.jpg'
image_collection = imread_collection(image_path)

X = []
y = []
for i, image in enumerate(image_collection):
    image = cv2.resize(image, (62, 62))
    X.append(image)
    y.append(i)
X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

from skimage.feature import local_binary_pattern

X_train_lbp = np.zeros_like(X_train)
X_test_lbp = np.zeros_like(X_test)
for i in range(X_train.shape[0]):
    X_train_lbp[i] = local_binary_pattern(X_train[i], P=8, R=1)
for i in range(X_test.shape[0]):
    X_test_lbp[i] = local_binary_pattern(X_test[i], P=8, R=1)

X_train_fft = np.fft.fft2(X_train_lbp)
X_test_fft = np.fft.fft2(X_test_lbp)

X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])

model = SVC(kernel='rbf')
model.fit(X_train_features, y_train)

X_train_fft = np.fft.fft2(X_train)
X_test_fft = np.fft.fft2(X_test)

X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])

model = SVC(kernel='rbf')
model.fit(X_train_features, y_train)

y_pred = model.predict(X_test_features)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

dataset_path = '/content/custom/'

X = []
y = []
for i in range(50):
    folder_path = dataset_path + 'folder' + str(i) + '/'
    for j in range(2):
        # Load the image
        image_path = folder_path + 'image' + str(j) + '.jpg'
        image = cv2.imread(image_path)
        image = cv2.resize(image, (62, 62))
        X.append(image)
        y.append(i)
X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

from skimage.feature import local_binary_pattern

X_train_lbp = np.zeros_like(X_train)
X_test_lbp = np.zeros_like(X_test)
for i in range(X_train.shape[0]):
    X_train_lbp[i] = local_binary_pattern(X_train[i], P=8, R=1)
for i in range(X_test.shape[0]):
    X_test_lbp[i] = local_binary_pattern(X_test[i], P=8, R=1)

X_train_fft = np.fft.fft2(X_train_lbp)
X_test_fft = np.fft.fft2(X_test_lbp)

X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])

model = SVC(kernel='rbf')
model.fit(X_train_features, y_train)

X_train_fft = np.fft.fft2(X_train)
X_test_fft = np.fft.fft2(X_test)

X_train_features = np.abs(X_train_fft[:, :X_train_fft.shape[1]//2])
X_test_features = np.abs(X_test_fft[:, :X_test_fft.shape[1]//2])
model = SVC(kernel='rbf')
model.fit(X_train_features, y_train)

y_pred = model.predict(X_test_features)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize


class DatasetVisualizer:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def visualize_dataset(self):
        lfw_people = fetch_lfw_people(min_faces_per_person=100, resize=0.5)
        fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(10, 6),
                                 subplot_kw={'xticks': [], 'yticks': []})

        for i, ax in enumerate(axes.flat):
            ax.imshow(lfw_people.images[i], cmap='gray')
            ax.set_title(lfw_people.target_names[lfw_people.target[i]])
        plt.tight_layout()
        plt.show()

        fig, axes = plt.subplots(nrows=10, ncols=10, figsize=(12, 12),
                                 subplot_kw={'xticks': [], 'yticks': []})
        for i in range(50):
            folder_path = os.path.join(self.dataset_dir, f'subfolder_{i}')
            image_files = os.listdir(folder_path)[:2] 
            for j, image_file in enumerate(image_files):
                image_path = os.path.join(folder_path, image_file)
                image = plt.imread(image_path)
                image = resize(image, output_shape=(64, 64), anti_aliasing=True)
                row = i // 5 * 2 + j // 5
                col = i % 5 * 2 + j % 5
                axes[row, col].imshow(image)
                axes[row, col].set_title(f'subfolder_{i}')
        plt.tight_layout()
        plt.show()

dataset_visualizer = DatasetVisualizer('/content/custom')
dataset_visualizer.visualize_dataset()

"""Visualize fourier components"""

import numpy as np
import cv2
from skimage.feature import local_binary_pattern
from sklearn.datasets import fetch_lfw_people
import matplotlib.pyplot as plt

lfw_people = fetch_lfw_people(min_faces_per_person=100, resize=0.5)

X = lfw_people.data
y = lfw_people.target

X_lbp = local_binary_pattern(X, P=8, R=1)

X_fft = np.fft.fft2(X_lbp)

X_magnitudes = np.abs(X_fft)

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
axes = axes.ravel()
for i, ax in enumerate(axes):
    if i == 0:
        ax.imshow(X[0].reshape(50, 37), cmap='gray')
        ax.set_title('Original')
    else:
        X_i = np.zeros_like(X_fft)
        X_i[:, i-1] = X_fft[:, i-1]
        X_i_magnitude = np.abs(np.fft.ifft2(X_i))
        ax.imshow(X_i_magnitude[0].reshape(50, 37), cmap='gray')
        ax.set_title(f'{i}-th Fourier coefficient')
plt.tight_layout()
plt.show()

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
path = '/content/custom'

def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith('.jpg'):
            img = cv2.imread(os.path.join(folder, filename), cv2.IMREAD_GRAYSCALE)
            img_resized = cv2.resize(img, (37, 50))
            images.append(img_resized)
    return images

X = []
for i in range(1, 51):
    folder_path = os.path.join(path, f'{i:02d}')
    images = load_images(folder_path)
    X.extend(images)

X = np.array(X)
X_fft = np.fft.fft2(X)
X_magnitudes = np.abs(X_fft)

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
axes = axes.ravel()
for i, ax in enumerate(axes):
    if i == 0:
        ax.imshow(X[0], cmap='gray')
        ax.set_title('Original')
    else:
        X_i = np.zeros_like(X_fft)
        X_i[:, i-1] = X_fft[:, i-1]
        X_i_magnitude = np.abs(np.fft.ifft2(X_i))
        ax.imshow(X_i_magnitude[0], cmap='gray')
        ax.set_title(f'{i}-th Fourier coefficient')
plt.tight_layout()
plt.show()

import numpy as np
import cv2
from skimage.feature import local_binary_pattern
from scipy.io import loadmat
import matplotlib.pyplot as plt
data = loadmat('miniceleba.mat')
X = data['X']
X_lbp = local_binary_pattern(X, P=8, R=1)
X_fft = np.fft.fft2(X_lbp)

X_magnitudes = np.abs(X_fft)

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
axes = axes.ravel()
for i, ax in enumerate(axes):
    if i == 0:
        ax.imshow(X[0], cmap='gray')
        ax.set_title('Original')
    else:
        X_i = np.zeros_like(X_fft)
        X_i[:, i-1] = X_fft[:, i-1]
        X_i_magnitude = np.abs(np.fft.ifft2(X_i))
        ax.imshow(X_i_magnitude[0], cmap='gray')
        ax.set_title(f'{i}-th Fourier coefficient')
plt.tight_layout()
plt.show()
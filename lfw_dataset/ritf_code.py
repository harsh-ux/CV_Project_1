# -*- coding: utf-8 -*-
"""ritf_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B5sfhWmHrez7MuzeFdvjR8V1tZ_dHwU0
"""

import os

import numpy as np
import pandas as pd 

import cv2

import matplotlib.pyplot as plt
from datetime import datetime
import io
import itertools
from packaging import version

import sklearn.metrics

from tensorflow.keras.preprocessing.image import ImageDataGenerator

def normalize_mean_var(arr):
    arr -= np.mean(arr)
    arr /= np.var(arr)
    return arr

number_of_images = 1

df = pd.read_csv("/content/allname_custom.csv")

topNames = set([x for x in df['name']])
len(topNames)

train_data_dir = "/content/custom_dataset"

img_width = img_height = 224
batch_size = 10

train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.7)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    classes=topNames,
    class_mode='categorical',
    subset='training')

validation_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    classes=topNames,
    class_mode='categorical',
    subset='validation')

print("Found", train_generator.samples, "images belonging to", len(train_generator.class_indices), "classes in the training set")
print("Found", validation_generator.samples, "images belonging to", len(validation_generator.class_indices), "classes in the validation set")

from skimage import feature
import numpy as np
class LocalBinaryPatterns:
    def __init__(self, numPoints, radius):
        self.numPoints = numPoints
        self.radius = radius
    def describe(self, image, eps=1e-7):
        lbp = feature.local_binary_pattern(image, self.numPoints,
        self.radius, method="ror")
        (hist, _) = np.histogram(lbp.ravel(),
        bins=np.arange(0, self.numPoints + 3),
        range=(0, self.numPoints + 2))
        hist = hist.astype("float")
        hist /= (hist.sum() + eps)
        return hist

import math
D = math.sqrt(224**2 + 224**2)
r = 16
m = 32
ritf_desc = LocalBinaryPatterns(m-2, r)

def get_image_histogram(img, ritf_desc):

   
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ritf = ritf_desc.describe(gray)
    
    return ritf

from IPython.display import clear_output

def preprocess(gen, ritf_desc):
    res = []
    for i in range(len(gen)):
        clear_output(wait=True)
        print("{}/{}".format(i, len(gen)))
        x, y = gen[i]
        res.append([x, y])
    return np.asarray(res)

training_data = preprocess(train_generator, ritf_desc)
valid_data = preprocess(validation_generator, ritf_desc)

train_path = "/content/Train_imc_50.npy"
valid_path = "/content/valid_imc_50.npy"

np.save(train_path, training_data)
np.save(valid_path, valid_data)

training_data[0][0].shape

def label_converter(arr):
    for i in range(len(arr)):
        if arr[i] == 1:
            return i
    return -1

def remove_batches(arr):
    X = []
    y = []
    for j in range(len(arr)):
        batch = arr[j]
        for i in range(len(batch[0])):
            gray = cv2.cvtColor(batch[0][i], cv2.COLOR_BGR2GRAY)
            X.append(gray)
            y.append(label_converter(batch[1][i]))
        
    return np.asarray(X), np.asarray(y)

X_training, y_training = remove_batches(training_data)

X_validation, y_validation = remove_batches(valid_data)

from skimage.feature import hog

X_training_hists = []
for image in X_training:
    hog_features = hog(image, orientations=8, pixels_per_cell=(8, 8),
                        cells_per_block=(1, 1), visualize=False, multichannel=False)
    X_training_hists.append(hog_features)
    
X_training_hists = np.asarray(X_training_hists)

X_valid_hists = []
for image in X_validation:
    hog_features = hog(image, orientations=8, pixels_per_cell=(8, 8),
                        cells_per_block=(1, 1), visualize=False, multichannel=False)
    X_valid_hists.append(hog_features)
    
X_valid_hists = np.asarray(X_valid_hists)

from sklearn.ensemble import GradientBoostingClassifier

gbc = GradientBoostingClassifier(n_estimators=100, max_depth=3)
gbc.fit(X_training_hists, y_training)

pred = gbc.predict(X_valid_hists)
cnf_matrix = confusion_matrix(y_validation, pred)
GB_acc = accuracy_score(y_validation, pred)

print("Gradient Boosting Accuracy:", GB_acc)
confusion_matrix_display(gbc, X_valid_hists, y_validation, "Gradient Boosting")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_training_hists, y_training)

pred = clf.predict(X_valid_hists)
cnf_matrix = confusion_matrix(y_validation, pred)
RF_acc = accuracy_score(y_validation, pred)

print("Random Forest Accuracy:", RF_acc)
confusion_matrix_display(clf, X_valid_hists, y_validation, "Random Forest")

from sklearn.svm import LinearSVC
from sklearn import metrics


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

model = LinearSVC(C=100.0)
model.fit(X_training_hists, y_training)

pred = model.predict(X_valid_hists)
cnf_matrix = confusion_matrix(y_validation, pred)
RF_acc = metrics.accuracy_score(y_validation, pred)

print("Linear SVM Accuracy:", RF_acc)
disp = ConfusionMatrixDisplay(confusion_matrix=cnf_matrix, display_labels=[x for x in range(len(topNames))])
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion matrix: Linear SVM')
plt.show()

imgs = train_generator[0][0]
fig=plt.figure(figsize=(3, 3))
plt.imshow(imgs[0])
plt.show()

model = cv2.face.LBPHFaceRecognizer_create(radius=16, neighbors=1)
model.train(X_training, y_training)

len(X_training)

model.getHistograms()[0].shape

from sklearn import metrics

def getHistogramss(X_data, y_data, rad, neig):
    model = cv2.face.LBPHFaceRecognizer_create(radius=rad, neighbors=neig)
    model.train(X_data, y_data)
    X = []
    arr = model.getHistograms()
    for i, h in enumerate(arr):
        hist = h[0]
        X.append(hist)
    return X

d = {}
for i in range(1, 10):
    for j in range(1, 10):
        X_training_hists = getHistogramss(X_training, y_training, j, i)     
        X_valid_hists = getHistogramss(X_validation, y_validation, j, i)

        model = LinearSVC(C=100.0)
        model.fit(X_training_hists, y_training)

        pred = model.predict(X_valid_hists)
        RF_acc = metrics.accuracy_score(y_validation, pred)
        d[(j, i)] = RF_acc
        print("Random Forest Accuracy in rad={}, neig={}: {}".format(j, i, RF_acc))

i, j = 8, 9
X_training_hists = getHistogramss(X_training, y_training, j, i)     
X_valid_hists = getHistogramss(X_validation, y_validation, j, i)
X_training_hists_concat = np.stack(X_training_hists, axis=0)
X_valid_hists_concat = np.stack(X_valid_hists, axis=0)
from sklearn.svm import LinearSVC
model = LinearSVC(C=100.0)
model.fit(X_training_hists_concat, y_training)

pred = model.predict(X_valid_hists_concat)
cnf_matrix = metrics.confusion_matrix(y_validation, pred)
RF_acc = metrics.accuracy_score(y_validation, pred)
d[(j, i)] = RF_acc
print("Random Forest Accuracy in rad={}, neig={}: {}".format(j, i, RF_acc))

len(X_training_hists[0])

from sklearn.feature_selection import RFE
estimator = LinearSVC(C=100.0, random_state=42, max_iter=2000)
selector = RFE(estimator, n_features_to_select=128, step=64, verbose=1)
selector = selector.fit(X_training_hists, y_training)
print(selector.support_)
print(selector.ranking_)

from sklearn.feature_selection import SelectKBest, chi2

selector = SelectKBest(chi2, k=500)
X_training_hists_reduced = selector.fit_transform(X_training_hists, y_training)
X_valid_hists_reduced = selector.transform(X_valid_hists)

from sklearn.svm import LinearSVC
model = LinearSVC(C=100.0, random_state=42, max_iter=10000)
model.fit(X_training_hists_reduced, y_training)

pred = model.predict(X_valid_hists_reduced)
cnf_matrix = metrics.confusion_matrix(y_validation, pred)
RF_acc = metrics.accuracy_score(y_validation, pred)
print("LinearSVC Accuracy: {}".format(RF_acc))
confusion_matrix_display(model, X_valid_hists_reduced, y_validation, "LinearSVC")

ritf_hist_train_path = "/content/RITF_hist_reduced_128_train_imc_50.npy"
ritf_hist_valid_path = "/content/RITF_hist_reduced_128_valid_imc_50.npy"

np.save(ritf_hist_train_path, X_training_hists_reduced)
np.save(ritf_hist_valid_path, X_valid_hists_reduced)

from sklearn.feature_selection import mutual_info_classif
selector = SelectKBest(mutual_info_classif, k=100)
selector.fit(X_training_hists, y_training)
feature_sel = selector.get_support()
ritf_feature_selection_path = "/content/RITF_feature_selection_128_valid_imc_50.npy"
np.save(ritf_feature_selection_path, feature_sel)

train_path = "/content/Train_imc_50.npy"
valid_path = "/content/valid_imc_50.npy"

np.save(train_path, training_data)
np.save(valid_path, valid_data)

y_train_path = "/content/y_train_imc_50.npy"
y_valid_path = "/content/y_valid_imc_50.npy"

np.save(y_train_path, y_training)
np.save(y_valid_path, y_validation)

ritf_hist_train_path = "/content/RITF_hist_reduced_128_train_imc_50.npy"
ritf_hist_valid_path = "/content/RITF_hist_reduced_128_valid_imc_50.npy"

X_training_hists_reduced = np.load(ritf_hist_train_path)
X_valid_hists_reduced = np.load(ritf_hist_valid_path)

y_train_path = "/content/y_train_imc_50.npy"
y_valid_path = "/content/y_valid_imc_50.npy"

y_training = np.load(y_train_path)
y_validation = np.load(y_valid_path)

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

def confusion_matrix_display(model, X_test, y_test, title):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    labels = np.unique(y_test)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap=plt.cm.Blues)
    disp.ax_.set_title('Confusion matrix: ' + title)

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

clf = RandomForestClassifier(n_estimators = 100)
clf.fit(X_training_hists_reduced, y_training)

pred = clf.predict(X_valid_hists_reduced)
cnf_matrix = metrics.confusion_matrix(y_validation, pred)
RF_acc = metrics.accuracy_score(y_validation, pred)

print("Random Forest Accuracy:", RF_acc)
confusion_matrix_display(clf, X_valid_hists_reduced, y_validation, "Random Forest")

def SVM_classification(X_train, X_test, y_train, y_test):
    #SVM
    from sklearn.svm import SVC

    for kernel in ('rbf', 'sigmoid'):
        svc= SVC(kernel = kernel)

        svc.fit(X_train, y_train)
        svcpred = svc.predict(X_test)
        cnf_matrix = metrics.confusion_matrix(y_test, svcpred)
        SVC_acc = metrics.accuracy_score(y_test, svcpred)

        print('SVC (kernel = {}): '.format(kernel),SVC_acc)
        title = 'SVC (kernel = {}): '.format(kernel)
        confusion_matrix_display(svc, X_test, y_test, title)
        
SVM_classification(X_training_hists_reduced, X_valid_hists_reduced, y_training, y_validation)
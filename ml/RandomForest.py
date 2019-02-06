import operator
# import pydot
import numpy as np
import pandas as pd
# from fancyimpute import KNN
from joblib import dump, load
from sklearn import preprocessing
# from sklearn.tree import export_graphviz
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt


class RandomForest:

    features = pd.read_csv("./ml/raw.csv")
    n_estimators = 500
    file_path = "./ml"
    dump_path = "./ml/rf.joblib"
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    def __init__(self):

        self.labels = np.array(self.features["class"])
        self.features = self.features.drop("class", axis=1)
        self.feature_list = list(self.features.columns)
        self.features_np = np.array(self.features)

        self.train_features = None
        self.test_features = None
        self.train_labels = None
        self.test_labels = None

        self.rf = None
        self.scaler = None
        self.predictions = None  # this is given in percentage for each class
        self.predictions_s = []  # this is 0 or 1 for each class
        self.orders = ['eight', 'five', 'four', 'nine',
                       'one', 'seven', 'six', 'three', 'two']
        self.importances = None

    def scale(self):
        self.scaler = preprocessing.StandardScaler().fit(self.features_np)
        self.features_np = self.scaler.transform(self.features_np)

    def impute(self):
        # self.features_np = KNN(k=5).fit_transform(self.features_np)
        self.imputer = self.imputer.fit(self.features_np)
        self.features_np = self.imputer.transform(self.features_np)

    def split(self):
        self.train_features, self.test_features, self.train_labels, self.test_labels = train_test_split(
            self.features_np, self.labels, test_size=0.1, random_state=42)

        # self.train_labels = pd.get_dummies(self.train_labels)
        # self.orders = list(self.train_labels.columns)
        self.train_labels = np.array(self.train_labels)
        self.test_labels = np.array(self.test_labels)

    def train(self):
        self.rf = RandomForestClassifier(
            n_estimators=self.n_estimators, random_state=42)
        self.rf.fit(self.train_features, self.train_labels)

    def dump(self):
        dump(self.rf, self.dump_path)

    def load(self):
        self.rf = load(self.dump_path)

    def predict(self):
        # self.predictions = self.rf.predict_proba(self.test_features)
        self.predictions = self.rf.predict(self.test_features)

    def predict_s(self, metrics):

        predictions = []

        _test = self.scaler.transform(np.array(metrics))
        _test = self.imputer.transform(_test)
        summary = self.rf.predict_proba(_test)

        for s in summary:
            index, _ = max(enumerate(s), key=operator.itemgetter(1))
            pred = {"class": self.orders[index], "summary": {}}
            for i, key in enumerate(self.rf.classes_):
                pred["summary"][key] = s[i]
            predictions.append(pred)

        return predictions

    def get_prediction_error(self):
        accuracy_list = []
        for (p, t) in zip(self.predictions, self.test_labels):
            accuracy_list.append(1) if p == t else accuracy_list.append(0)

        accu_perc = sum(accuracy_list)/len(accuracy_list)
        print('Accuracy:', round(accu_perc, 4), '%.')

    # def get_tree(self, num):
    #     tree = self.rf.estimators_[num]
    #     dot_path = self.file_path + "/tree.dot"
    #     png_path = self.file_path + "/tree.png"

    #     export_graphviz(tree, out_file=dot_path,
    #                     feature_names=self.feature_list, rounded=True, precision=1)
    #     (graph, ) = pydot.graph_from_dot_file(dot_path)
    #     graph.write_png(png_path)

    def get_importance_factor(self):
        self.importances = list(self.rf.feature_importances_)
        feature_importances = [(feature, round(importance, 2))
                               for feature, importance in zip(self.feature_list, self.importances)]
        feature_importances = sorted(
            feature_importances, key=lambda x: x[1], reverse=True)
        [print('Variable: {:20} Importance: {}'.format(*pair))
         for pair in feature_importances]

    # def plot_importance(self):

    #     png_path = self.file_path + "/imp.png"
    #     y_pos = np.arange(len(self.importances))
    #     plt.barh(y_pos, self.importances)
    #     plt.yticks(y_pos, self.feature_list)

    #     plt.ylabel('Variable ')
    #     plt.xlabel('Importance')
    #     plt.title('Variable Importances')
    #     plt.savefig(png_path, bbox_inches="tight")


rf = RandomForest()
rf.scale()
rf.impute()
rf.split()
rf.train()
rf.dump()
# rf.load()
rf.predict()
rf.get_prediction_error()
# rf.get_tree(5)
rf.get_importance_factor()
# rf.plot_importance()

import pydot
import numpy as np
import pandas as pd
from fancyimpute import KNN
from joblib import dump, load
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.tree import export_graphviz
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


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
        self.predictions = None
        self.importances = None

    def impute(self):
        self.features_np = preprocessing.scale(self.features_np)
        self.features_np = KNN(k=5).fit_transform(self.features_np)

    def split(self):
        self.train_features, self.test_features, self.train_labels, self.test_labels = train_test_split(
            self.features_np, self.labels, test_size=0.1, random_state=42)

    def train(self):
        self.rf = RandomForestRegressor(
            n_estimators=self.n_estimators, random_state=42)
        self.rf.fit(self.train_features, self.train_labels)

    def dump(self):
        dump(self.rf, self.dump_path)

    def load(self):
        self.rf = load(self.dump_path)

    def predict(self):
        self.predictions = self.rf.predict(self.test_features)
        # predictions = self.rf.predict(self.train_features)
        print([int(round(p)) - self.test_labels[i]
               for i, p in enumerate(self.predictions)])

    def get_prediction_error(self):
        errors = abs(self.predictions - self.test_labels)

        # Print out the mean absolute error (mae)
        print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')

        mape = np.mean(100 * (errors / self.test_labels))
        accuracy = 100 - mape
        print('Accuracy:', round(accuracy, 2), '%.')

    def get_tree(self, num):
        tree = self.rf.estimators_[num]
        dot_path = self.file_path + "/tree.dot"
        png_path = self.file_path + "/tree.png"

        export_graphviz(tree, out_file=dot_path,
                        feature_names=self.feature_list, rounded=True, precision=1)
        (graph, ) = pydot.graph_from_dot_file(dot_path)
        graph.write_png(png_path)

    def get_importance_factor(self):
        self.importances = list(self.rf.feature_importances_)
        feature_importances = [(feature, round(importance, 2))
                               for feature, importance in zip(self.feature_list, self.importances)]
        feature_importances = sorted(
            feature_importances, key=lambda x: x[1], reverse=True)
        [print('Variable: {:20} Importance: {}'.format(*pair))
         for pair in feature_importances]

    def plot_importance(self):
        png_path = self.file_path + "/imp.png"
        plt.style.use('fivethirtyeight')
        x_values = list(range(len(self.importances)))
        plt.bar(x_values, self.importances, orientation='vertical')
        plt.xticks(x_values, self.feature_list, rotation='vertical')
        plt.ylabel('Importance')
        plt.xlabel('Variable')
        plt.title('Variable Importances')
        plt.savefig(png_path, bbox_inches="tight")


rf = RandomForest()
rf.impute()
rf.split()
rf.train()
rf.dump()
# rf.load()
rf.predict()
rf.get_prediction_error()
rf.get_tree(5)
rf.get_importance_factor()
rf.plot_importance()

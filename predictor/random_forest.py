import numpy as np
from collections import Counter

class DecisionTree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y, depth=0):
        n_samples, n_features = X.shape
        unique_labels = np.unique(y)

        if len(unique_labels) == 1 or depth == self.max_depth:
            return Counter(y).most_common(1)[0][0]

        best_feature, best_threshold = self.best_split(X, y, n_features)

        if best_feature is None:
            return Counter(y).most_common(1)[0][0]

        left_indices = X[:, best_feature] < best_threshold
        right_indices = X[:, best_feature] >= best_threshold

        left_subtree = self.fit(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self.fit(X[right_indices], y[right_indices], depth + 1)

        return {"feature": best_feature, "threshold": best_threshold,
                "left": left_subtree, "right": right_subtree}

    def best_split(self, X, y, n_features):
        best_gini = 1.0
        best_feature, best_threshold = None, None

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_indices = y[X[:, feature] < threshold]
                right_indices = y[X[:, feature] >= threshold]

                if len(left_indices) == 0 or len(right_indices) == 0:
                    continue

                gini = self.gini_index(left_indices, right_indices)

                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def gini_index(self, left, right):
        total = len(left) + len(right)

        def gini(group):
            counts = np.bincount(group)
            probs = counts / len(group)
            return 1 - np.sum(probs ** 2)

        return (len(left) / total) * gini(left) + (len(right) / total) * gini(right)

    def predict(self, X):
        return np.array([self._predict(sample, self.tree) for sample in X])

    def _predict(self, sample, tree):
        if not isinstance(tree, dict):
            return tree

        feature, threshold = tree["feature"], tree["threshold"]

        if sample[feature] < threshold:
            return self._predict(sample, tree["left"])
        else:
            return self._predict(sample, tree["right"])


class RandomForest:
    def __init__(self, n_trees=10, max_depth=None, sample_size=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.sample_size = sample_size
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        n_samples = X.shape[0]
        sample_size = self.sample_size or n_samples

        for _ in range(self.n_trees):
            indices = np.random.choice(n_samples, sample_size, replace=True)
            X_sample, y_sample = X[indices], y[indices]

            tree = DecisionTree(max_depth=self.max_depth)
            tree.tree = tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        return np.apply_along_axis(lambda x: Counter(x).most_common(1)[0][0], axis=0, arr=tree_predictions)

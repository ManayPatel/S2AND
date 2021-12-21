from os.path import join
from s2and.data import ANDData
from s2and.model import PairwiseModeler
from s2and.featurizer import FeaturizationInfo
from s2and.featurizer import featurize
from s2and.eval import pairwise_eval
from s2and.model import Clusterer, FastCluster
from hyperopt import hp
from s2and.eval import cluster_eval
import pickle

with open("clusterer.pkl", "rb") as _pkl_file:
    clusterer = pickle.load(_pkl_file)

with open("pairwise.pkl", "rb") as _pkl_file:
    pairwise_model = pickle.load(_pkl_file)

#Test Data
dataset_name = "patent"
parent_dir = "data/data/patent/is/"
test_dataset = ANDData(
    signatures=join(parent_dir, f"{dataset_name}_signatures.json"),
    papers=join("data/data/patent/", f"{dataset_name}_papers.json"),
    mode="only_test",
#    specter_embeddings=join(parent_dir, f"{dataset_name}_specter.pickle"),
    clusters=join(parent_dir, f"{dataset_name}_clusters.json"),
    block_type="s2",
    train_ratio=0.0,
    val_ratio=0.0,
    test_ratio=1.0,
    train_pairs_size=100000,
    val_pairs_size=10000,
    test_pairs_size=10000,
    name=dataset_name,
    n_jobs=24,
)

#Pairwise eval:
featurization_info = FeaturizationInfo()
_, _, test = featurize(test_dataset, featurization_info, n_jobs=24, use_cache=True)
X_test, y_test, _ = test

pairwise_metrics = pairwise_eval(X_test, y_test, pairwise_model.classifier, figs_path='figs/', title='example', shap_feature_names = ['x_test', 'y_test'], skip_shap = True)
print(pairwise_metrics)

#Cluster eval:
metrics, metrics_per_signature = cluster_eval(test_dataset, clusterer)
print(metrics)

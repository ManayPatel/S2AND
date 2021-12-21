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

with open("saved_model.pkl", "rb") as _pkl_file:
    clusterer = pickle.load(_pkl_file)

dataset_name = "patent"
parent_dir = "data/data/patent/"
#    signatures=join(parent_dir, f"{dataset_name}_signatures.json"),
#   papers=join(parent_dir, f"{dataset_name}_papers.json"),
#    specter_embeddings=join(parent_dir, f"{dataset_name}_specter.pickle"),
#    clusters=join(parent_dir, f"{dataset_name}_clusters.json"),
anddata = ANDData(
    signatures=join(parent_dir, f"{dataset_name}_signatures.json"),
    papers=join(parent_dir, f"{dataset_name}_papers.json"),
    specter_embeddings=join(parent_dir, f"{dataset_name}_specter.pickle"),
    name="John F. Spalding",
    mode="inference",
    block_type="s2",
)
pred_clusters, pred_distance_matrices = clusterer.predict(anddata.get_blocks(), anddata)

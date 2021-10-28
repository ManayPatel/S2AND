
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

dataset_name = "patent"
parent_dir = "data/data/patent/"
dataset = ANDData(
    signatures=join(parent_dir, f"{dataset_name}_signatures.json"),
    papers=join(parent_dir, f"{dataset_name}_papers.json"),
    mode="train",
    specter_embeddings=join(parent_dir, f"{dataset_name}_specter.pickle"),
    clusters=join(parent_dir, f"{dataset_name}_clusters.json"),
    block_type="s2",
    train_ratio=0.85,
    val_ratio=0.1,
    test_ratio=0.05,
    train_pairs_size=100000,
    val_pairs_size=10000,
    test_pairs_size=10000,
    name=dataset_name,
    n_jobs=24,
)


featurization_info = FeaturizationInfo()
# the cache will make it faster to train multiple times - it stores the features on disk for you
train, val, test = featurize(dataset, featurization_info, n_jobs=24, use_cache=True)
X_train, y_train, _ = train
X_val, y_val, _ = val
X_test, y_test, _ = test

# calibration fits isotonic regression after the binary classifier is fit
# monotone constraints help the LightGBM classifier behave sensibly
pairwise_model = PairwiseModeler(
    n_iter=25, monotone_constraints=featurization_info.lightgbm_monotone_constraints
)
# this does hyperparameter selection, which is why we need to pass in the validation set.
pairwise_model.fit(X_train, y_train, X_val, y_val)

# this will also dump a lot of useful plots (ROC, PR, SHAP) to the figs_path
pairwise_metrics = pairwise_eval(X_test, y_test, pairwise_model.classifier, figs_path='figs/', title='example', shap_feature_names = ['x_test', 'y_test'], skip_shap = True)
print(pairwise_metrics)

clusterer = Clusterer(
    featurization_info,
    pairwise_model,
    cluster_model=FastCluster(linkage="average"),
    search_space={"eps": hp.uniform("eps", 0, 1)},
    n_iter=25,
    n_jobs=24,
)
clusterer.fit(dataset)

# the metrics_per_signature are there so we can break out the facets if needed
dataset_name = "patent"
parent_dir = "data/data/patent/"
test_dataset = ANDData(
    signatures=join(parent_dir, f"testing_signatures.json"),
    papers=join(parent_dir, f"{dataset_name}_papers.json"),
    mode="inference",
#    specter_embeddings=join(parent_dir, f"{dataset_name}_specter.pickle"),
    clusters=join(parent_dir, f"testing_clusters.json"),
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
metrics, metrics_per_signature = cluster_eval(test_dataset, clusterer)
print(metrics)

with open("saved_model.pkl", "wb") as _pkl_file:
	pickle.dump(clusterer, _pkl_file)

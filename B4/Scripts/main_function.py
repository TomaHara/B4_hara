# ライブラリのインポート
# 可視化系
import matplotlib.pyplot as plt
import seaborn as sns

# 特徴量エンジニアリング・モデル評価系
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import SplineTransformer

# 次元圧縮系
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap.umap_ import UMAP

# サブ関数のインポート
from sub_function import run_model, reduction_models, plot_reduced_space, show_loading, plot_reduced_score_vs_features    

# 実際に次元削減、可視化を行っていく（PCA・t-SNE・UMAP用）
def summary_reducing(summary_sleep_df, model_name, N, feature_cols, score_col):
    X = summary_sleep_df[feature_cols]
    score_txt = summary_sleep_df[score_col]
    
    reduced_cols = [f"PC{i+1}" for i in range(N)]

    # 次元削減
    model, reduced_df = run_model(X=X, model_name=model_name, N=N, reduced_cols=reduced_cols, score_txt=score_txt)
    
    # 次元削減後の可視化
    plot_reduced_space(model_name=model_name, reduced_df=reduced_df)
    print("#"*200)
    
    # スコアと特徴量の可視化（PCAの場合はローディング、それ以外は相関係数＋散布図）
    if model_name == "PCA":
        show_loading(model=model, feature_cols=feature_cols, reduced_cols=reduced_cols)
    else:
        plot_reduced_score_vs_features(summary_sleep_df=summary_sleep_df, reduced_df=reduced_df, feature_cols=feature_cols, reduced_cols=reduced_cols)
    print("#"*200)

# 実際に次元削減、可視化を行っていく（PCA＋UMAP用）
def summary_reducing_pca_umap(summary_sleep_df, model_name, pca_N, umap_N, feature_cols, score_col):
    X = summary_sleep_df[feature_cols]
    score_txt = summary_sleep_df[score_col]
    
    pca_reduced_cols = [f"PC{i+1}" for i in range(pca_N)]
    reduced_cols = [f"PC{i+1}" for i in range(umap_N)]

    # 次元削減
    pca_model, pca_reduced_df = run_model(X=X, model_name="PCA", N=pca_N, reduced_cols=pca_reduced_cols, score_txt=score_txt)
    model, reduced_df = run_model(X=pca_reduced_df[pca_reduced_cols], model_name="UMAP", N=umap_N, reduced_cols=reduced_cols, score_txt=score_txt)
    
    # 次元削減後の可視化
    plot_reduced_space(model_name=model_name, reduced_df=reduced_df)
    print("#"*200)
        
    # スコアと特徴量の可視化（PCAの場合はローディング、それ以外は相関係数＋散布図）
    if model_name == "PCA":
        show_loading(model=model, feature_cols=X.columns, reduced_cols=reduced_cols)
    else:
        plot_reduced_score_vs_features(summary_sleep_df=summary_sleep_df, reduced_df=reduced_df, feature_cols=feature_cols, reduced_cols=reduced_cols)
    print("#"*200)
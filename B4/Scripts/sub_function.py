# ライブラリのインポート
# 可視化系
import matplotlib.pyplot as plt
import seaborn as sns

# 計算系
import pandas as pd
import numpy as np

# 特徴量エンジニアリング・モデル評価系
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import SplineTransformer

# 次元圧縮系
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap.umap_ import UMAP


# 次元削減モデルを設定する
def reduction_models(model_name, N):
    reduction_model_dict = {
        "PCA": PCA(n_components=N, random_state = 42),
        "tSNE": TSNE(n_components=N, random_state = 42),
        "UMAP": UMAP(n_components=N, random_state = 42)
    }
    return reduction_model_dict[model_name]

def run_model(X, model_name, N, reduced_cols, score_txt):
    model = reduction_models(model_name, N)
    X_reduced = model.fit_transform(X)
    reduced_df = pd.DataFrame(X_reduced, columns=reduced_cols)
    reduced_df.insert(0, 'score', score_txt)
    return model, reduced_df

# 次元削減した結果をプロットする
def plot_reduced_space(model_name, reduced_df):
    print("次元削減空間の可視化")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='PC1', y='PC2', data=reduced_df, hue=reduced_df["score"], palette='viridis')

    
    plt.title(model_name)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.show()


# 次元削減した結果をチームごとに棒グラフで表示する
# def show_reduced_score(reduced_df, reduced_cols):
    # reduced_df = pl.from_pandas(reduced_df)[["score"]+reduced_cols]
    # 
    # print("スコア")
    # display(reduced_df)
    # 
    # plt.figure(figsize=(6, 20))
    # reduced_df = reduced_df.melt(id_vars="score", value_vars=reduced_cols).to_pandas()
    # sns.barplot(x="value", y="score", data=reduced_df, hue="variable", palette=sns.color_palette("deep"))
    # plt.axvline(x=0, color="lightgray", linestyle="--")
    # plt.show()

# （PCAのみ）次元削減した結果と各スタッツの関係性（係数/ローディング）を表示・プロットする
def show_loading(model, feature_cols, reduced_cols):
    loading_df = pd.DataFrame(model.components_, index=reduced_cols, columns=feature_cols)
    x_col = reduced_cols[0]
    y_col = reduced_cols[1]

    print("ローディング")
    display(loading_df)
    
    plt.figure(figsize=(8, 8))
    sns.scatterplot(x=x_col, y=y_col, data=loading_df.T)
    for x, y, txt in zip(loading_df.T[x_col], loading_df.T[y_col], loading_df.T.index):
        plt.text(x, y, txt, size=10)
    
    plt.show()
        
# （PCA以外）次元削減した結果と、各スタッツの関係性を相関係数、散布図で可視化する
# def plot_reduced_score_vs_features(summary_team_df, reduced_df, feature_cols, reduced_cols):
    # tmp_df = reduced_df.merge(summary_team_df, on="score", how="left")
    # 
    # n_rows = 5
    # n_cols = 4
    # 
    # for embedded in reduced_cols:
        # 相関係数
        # corr_cols = feature_cols + [embedded]
        # corr_df = (pl.from_pandas(tmp_df[corr_cols])
        #    .corr()
        #    .with_columns(INDEX_COL=pl.Series(corr_cols))
        #    .to_pandas()
        #    .set_index("INDEX_COL")
        # )
        # plt.figure(figsize=(12, 8))
        # sns.heatmap(corr_df, cmap="coolwarm", vmin=-1, vmax=1, square=True, annot=True, fmt=".2f")
        # plt.show()
        
    # （PCA以外）次元削減した結果と、各スタッツの関係性を相関係数、散布図で可視化する
def plot_reduced_score_vs_features(summary_sleep_df, reduced_df, feature_cols, reduced_cols):
    tmp_df = pd.merge(left=reduced_df, right=summary_sleep_df, on="score", how="left")
    
    for Principal_Components in reduced_cols:
        # 相関係数
        corr_cols = feature_cols + [Principal_Components]
        corr_df = tmp_df[corr_cols].corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_df, cmap="coolwarm", vmin=-1, vmax=1, square=True, annot=True, fmt=".2f")
        plt.show()
 
        # 散布図で可視化
        # fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(24, 24), tight_layout=True)
        # for idx, feature in enumerate(feature_cols):
            # i = idx // n_cols
            # j = idx % n_cols
            # sns.scatterplot(x=feature, y=embedded, data=tmp_df, hue=tmp_df["score"], palette=sns.color_palette("coolwarm", 32), ax=axes[i, j])
            # for x, y, txt in zip(tmp_df[feature], tmp_df[embedded], tmp_df["score"]):
                # axes[i, j].text(x, y, txt, size=8)
            # axes[i, j].set_title(f"{embedded} X {feature}")
            # axes[i, j].get_legend().remove()
        # plt.show()
        # print("-"*100)


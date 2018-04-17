# Unity_RL
## このリポジトリについて
技術書典4 き19 Rosenblock Chainersにて頒布を行った，【進化計算と強化学習の本３】の"Unityで強化学習を始めよう ~ML-AgentsでCartPole作成~"で用いたコードを公開しています．

[Unity ML-Agents](https://github.com/Unity-Technologies/ml-agents)を用いて作成したCartPole環境シーン，および学習に用いるpythonコードを公開しています．

![CartPoleSample](images/cartpole.png)


## 【進化計算と強化学習の本３】を持っている方向け
CartPole環境シーンを自分で作成する場合，【進化計算と強化学習の本３】に詳細な手順が示されているので，そちらを参考に進めてください．

このリポジトリ内に入っているCartPoleSampleシーンを使って実験を行いたい場合は，「【進化計算と強化学習の本３】を持っていない方向け」章を参考に進めてください．


## 【進化計算と強化学習の本３】を持っていない方向け
### 動作環境
#### Unity
CartPoleシーンを動かすためには，Unity 2017.1以降のバージョンが必要になります．

Unityは，[公式サイト](https://unity3d.com/jp)からダウンロードしてください．

#### Python
学習アルゴリズムは，Python3系で動作します．
主に，以下のライブラリが必要になります．

* Tensorflow
* Numpy
* Pillow

また，学習ログの推移を出来るようにするためには，以下のライブラリが必要になります．

* Tensorboard

以上のライブラリをインストールためには，以下の`python`フォルダに移動して，以下のコマンドを実行してください．

```
cd python
pip3 install -r requirement.txt
```


## 学習実行
CartPoleSample環境でエージェントの学習を実行させる場合，以下の手順を行ってください．

### CartPoleSample環境シーンのビルド
#### CartPoleSample環境シーンの起動
1. Unityを起動します．
2. Projectsダイアログで，ウィンドウの上部にある**Open**オプションを選択します．
3. ファイルダイアログを使用して，Unity_RLフォルダ内の`unity-environment`フォルダを探し，**Open**をクリックします．
4. `Project`ウィンドウで，`Assets/ML-Agents/Examples/CartPoleSample/`フォルダに移動します．
5. `CartPoleSample`ファイルをダブルクリックして，CartPoleSample環境シーンをロードします．

![CartPoleSample Scene](images/scene.png)


#### BrainをExternalに設定
1. **Scene**ウィンドウで，CartPoleAcademyオブジェクトの横にある三角形のアイコンをクリックします．
2. その子オブジェクト`CartPoleBrain`を選択します．
3. Inspectorウィンドウで，**Brain Type**を`External`に設定します．

![Set Brain to External](images/brain_external.png)

#### 環境をビルド
1. プレイヤー設定（menu: **Edit** > **Project Settings** > **Player**）を開きます．
2. **Resolution and Presentation**:
    - **Run in Background**がチェックされていることを確認します．
    - **Display Resolution Dialog**がDisabledに設定されていることを確認します．
3. ビルド設定ウィンドウ（menu:**File** > **Build Settings**）を開きます．
4. ターゲットプラットフォームを選択します．
5. **Scenes in Build**リストにシーンが表示されている場合は，CartPoleSampleシーンだけがチェックされていることを確認してください（リストが空の場合，現在のシーンのみがビルドに含まれます）．
6. *Build*をクリックします:
    a. ファイルダイアログで，ML-Agentsディレクトリの`python`に移動します．
    b. ファイル名を付けて**Save**をクリックします．

![Build Window 0](images/build_0.png)
![Build Window](images/build.png)

### 学習を実行
学習を実行するためには，以下のコマンドを実行してください．

```python
python3 python/run_hill_climbing.py <env_file_path> --run_id=<run-identifier> --train
```

`--train`フラグはML-Agentsに学習モードで実行するように指定します．
`env_file_path`はさきほどビルドした実行ファイルへのパスでなければなりません．


### 学習ログの推移確認
TensorBoardを利用することで，学習時に累積報酬やエピソードの長さがどのように変動しているかを確認することができます．
以下のコマンドを実行すると，tensorboardが起動します．

```
tensorboard --logdir=summaries
```

その後，`localhost:6006`を立ち上げて下さい．

TensorBoardによって，以下の推移が確認できます．

* iteration：山登り法の反復数
* total_reward：各反復毎に生成した政策パラメータの平均累積報酬
* best_total_reward：それまでの反復の中で最も良かった平均累積報酬
* episode_length：エピソードの長さ
* num_episode：エピソードの総数

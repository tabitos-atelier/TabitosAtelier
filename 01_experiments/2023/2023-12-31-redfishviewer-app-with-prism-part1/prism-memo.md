# 【解読書】Prismという名の魔法体系

これは、WPF/MVVM開発の旅路で、私が「Prism」という難解な魔法体系を解き明かすために書き記した、研究の記録である。情報の砂漠に散らばる古文書の断片を繋ぎ合わせ、私なりの理解と、旅の助けとなった道標をここにまとめる。

---

## 1. 冒険の前提：Prismを学ぶ前に知るべきこと

Prismの山に挑む前に、その麓に広がる二つの重要な概念を理解しておく必要がある。これを知らずして、頂を目指すことはできない。

### 1.1. Reactive Extensions (Rx) - 時間を操る魔法

`ReactiveProperty`の真髄を理解するには、まずその母体である`Reactive Extensions (Rx)`の哲学に触れるべきだ。これは単なるライブラリではない。**非同期処理やイベントといった「時間の流れ」そのものを、自在に操るための、全く新しい思考法**である。

*   **Rxは、Push型のLinqだ。**
    *   `IEnumerable<T>`を**Pull型**で処理するのがLinqなら、`IObservable<T>`というイベントの奔流を**Push型**で受け止めるのがRxだ。この違いを理解することが、全ての始まりとなる。

*   **学ぶべき古文書:**
    *   **[公式思想]** [連載：Reactive Extensions（Rx）入門](https://atmarkit.itmedia.co.jp/fdotnet/introrx/index/index.html) - 製作者自らが語る、根源的な思想。
    *   **[超入門]** [こわくないReactive Extensions超入門](https://qiita.com/acple@github/items/6cfee916f09632037a6e) - まずはこの羊皮紙で、恐怖心を取り払うといい。

### 1.2. ReactiveProperty - MVVMの聖剣

Rxの力を、MVVMという戦場で最大限に発揮させるために鍛え上げられた聖剣。`INotifyPropertyChanged`の実装地獄から我々を解放し、ViewとViewModelの魂を、より強力な魔法の糸で結びつける。

*   **なぜ便利なのか？**
    *   `INotifyPropertyChanged`を内包し、プロパティ変更通知を自動化する。
    *   双方向バインディングが、驚くほどシンプルに記述できる。

*   **学ぶべき古文書:**
    *   **[概要]** [MVVMとリアクティブプログラミングを支援するライブラリ「ReactiveProperty v2.0」オーバービュー](https://blog.okazuki.jp/entry/2015/02/22/212827) - この聖剣が何であるかを知るための、最初の道標。

---

## 2. Prismの核心：主要な魔法体系

Prismは、巨大で多機能な魔法体系だ。全てを一度に理解しようとせず、まずはその核心を成す、以下の要素から習得していくのが賢明だろう。

*   **Region:**
    *   Viewに名付けられた「領域」。この領域に、別のViewを動的に表示・置換するための、空間操作魔法。
*   **Navigation:**
    *   Regionの歴史（ナビゲーション履歴）を管理し、画面遷移のライフサイクルを司る、時間操作魔法。
*   **EventAggregator:**
    *   ViewModel間の疎結合な連携を実現する、万能の「伝書バト」。Pub/Subパターンでイベントを仲介する、Prismの心臓部の一つ。**RedfishViewerでは、この伝書バトを使いこなせるかが、最大の試練だった。**
*   **DialogService:**
    *   モーダル/モードレスダイアログを、MVVMの作法に則って美しく呼び出すための儀式。
*   **Module:**
    *   アプリケーションの機能を部品化し、別のアセンブリとして分割統治するための、高度な建築術。

---

## 3. 実践の記録：旅の途中で見つけた知恵と罠

理論だけでは、この険しい山は登れない。以下は、私が実際に手と頭を動かし、血と汗の末に手に入れた、実践的な知恵の記録である。

### 3.1. 頼れる賢者の道標

*   **[最重要]** **[.NET CORE WPF PRISM MVVM 入門 2020 エントリまとめ](https://elf-mission.net/wpf-prism-mvvm-net-core-getting-started-2020-index)**
    *   情報の砂漠における、唯一無二の巨大なオアシス。内容はPrism 7.2と古いが、その思想は今も色褪せない。**本気でPrismを学ぶなら、この賢者の言葉を全て読み解く覚悟が必要だ。**
*   **[実践]** **[【改訂版】PrismとReactivePropertyで簡単MVVM！](https://qiita.com/hiki_neet_p/items/e04b5ac692aa18df0968)**
    *   PrismとReactivePropertyを組み合わせる際の、具体的な詠唱法が記されている。

### 3.2. 時の流れとの戦い（バージョンアップの罠）

*   **Prism 8での破壊的変更:**
    *   `Prism.Logging`は完全に消え去った。古文書の呪文は、もはや通じない。
    *   `IDialogAware`の作法が変わり、`RequestClose`の詠唱法を間違えると、ダイアログが永遠に閉じない呪いにかかる。詳細は[こちらの古文書](https://elf-mission.net/programming/wpf/getting-started-2020/prism8-release/)に記されている。

### 3.3. 特殊な詠唱法（Tips & Tricks）

*   **ViewModel間の通信:**
    *   `EventAggregator`こそが正義。安易にViewModel同士を直接参照させようとすると、複雑な依存関係の迷宮に迷い込む。詳細は[この賢者の問答](https://teratail.com/questions/87338)に。
*   **PasswordBoxとの契約:**
    *   この気難しい部品をMVVMで操るには、特別な儀式が必要だ。詠唱法は、[この羊皮紙](https://redwarrior.hateblo.jp/entry/2021/01/12/090000)に全て記されている。
*   **ウィンドウイベントの捕捉:**
    *   `Loaded`や`Closing`といった、ウィンドウ自身の魂の声を聴くには、`Microsoft.Xaml.Behaviors.Wpf`という別の魔法体系の助けを借りる必要がある。詳細は[この羊皮紙](https://redwarrior.hateblo.jp/entry/2020/08/31/090000)に。（※ただし、`xmlns:i`の記述は罠なので注意）

### 3.4. 聖剣の選択：`ReactiveProperty` vs `ReactivePropertySlim`

*   **違いを理解せよ:**
    *   `Slim`は、その名の通り軽量だが、「Validation（入力検証）」などの強力な魔法が使えない。単純なプロパティなら`Slim`、複雑なロジックを伴うなら通常版、という使い分けが肝要だ。
*   **知るべき古文書:**
    *   **[詳細]** [ReactivePropertySlim詳解](https://neue.cc/2018/01/18_562.html)
    *   **[性能]** [ReactiveProperty と ReactivePropertySlim ってどれくらい違うの？](https://qiita.com/okazuki/items/aeaee8e3e8a4c01b3f39)

---

この解読書が、同じようにPrismという名の険しい山に挑む、未来の冒険者の羅針盤となることを願う。
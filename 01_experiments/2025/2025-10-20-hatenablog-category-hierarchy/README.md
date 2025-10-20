# はてなブログ カテゴリ階層化コード

はてなブログのカテゴリ表示を、より見やすく整理するために2階層化するJavaScriptとCSSのコードです。本機能は、シンプルさと性能を考慮し、親カテゴリと子カテゴリの2階層に限定しています。

-----

## 技術的特徴

  * **ライブラリ不要**: バニラJavaScript + CSSのみで実装
  * **軽量**: 外部依存なし、ページ読み込みへの影響を最小化
  * **2階層限定**: シンプルさと性能のバランスを重視した設計
  * **完全自動**: カテゴリ登録ルールに従えば、コード修正不要で動作

-----

## 実装の価値

本コードは、はてなブログのカテゴリ表示を2階層化し、以下の価値を提供します。

  * **読者体験の向上**: サイドバーのカテゴリが整理され、目的の記事を素早く発見できます
  * **サイト回遊性の改善**: 明確な階層構造により、関連記事への導線が強化されます
  * **SEO最適化**: 構造化データ対応により、検索エンジンがサイト構造を正しく理解します
  * **保守性の確保**: ライブラリに依存しないため、長期的なメンテナンスが容易です

-----

## カテゴリ階層化のルールと設定

この機能を正しく動作させるためには、はてなブログの管理画面で以下の設定が必要です。

1.  **パンくずリストの表示**: **「デザイン設定 > 記事 > パンくずリスト」** のチェックボックスをオンにしてください。これにより、パンくずリストが正しく表示され、本JavaScriptで再構築できるようになります。

2.  **カテゴリ表示設定**: はてなブログのサイドバーのカテゴリ設定で、以下の2つを設定してください。
    *   **表示順序**: **「アルファベット順」** を選択（JavaScriptが正しくパースするために必須）
    *   **表示件数**: **「全て表示」** を選択（すべてのカテゴリを処理対象にするために必須）

3.  **記事のカテゴリ入力**: 記事を作成する際、カテゴリを階層化したい場合は、以下の形式で入力してください。

      * **親カテゴリのみの場合**: `親カテゴリ`
      * **子カテゴリを持つ場合**: `親カテゴリ|子カテゴリ`

    例えば、「旅行」という親カテゴリの下に「国内旅行」という子カテゴリを作りたい場合は、記事のカテゴリ入力欄に `旅行` と `旅行|国内旅行` の両方を入力します。

-----

## JavaScriptコード

このJavaScriptコードは、記事のカテゴリが「`親カテゴリ|子カテゴリ`」の形式で入力されている場合に、パンくずリスト、JSON-LD、サイドバーのカテゴリ表示、およびアーカイブページの見出し・パンくずリストを自動的に階層化します。

**はてなブログのデザイン設定 > フッタ** にコピー＆ペーストしてご利用ください。
コード全体をコピー＆ペーストする場合、`<script>` と `</script>` タグで囲んでください。
既にJavaScriptが定義されている場合、このコードの`document.addEventListener('DOMContentLoaded', function() {`から`});`までの**中身**を、既存の`DOMContentLoaded`イベントリスナーの**中**に追記してください。
```javascript
document.addEventListener('DOMContentLoaded', function() {

  // --- 1. 記事内のカテゴリ情報を取得し、階層化の有無を判定 ---
  // 記事ページでのみ、パンくずリストとJSON-LDの再構築に利用します。
  let parentCategoryName = null;
  let childCategoryName = null;
  let isCategoryHierarchical = false; // 記事に階層化カテゴリが含まれるかを示すフラグ

  document.querySelectorAll('.entry-categories a.entry-category-link').forEach(link => {
    // カテゴリリンクのテキストに '|' が含まれていれば階層化カテゴリと判断
    if (link.textContent.includes('|')) {
      isCategoryHierarchical = true;
      // 親カテゴリ名と子カテゴリ名を分割し、余分な空白を除去
      [parentCategoryName, childCategoryName] = link.textContent.split('|').map(s => s.trim());
    }
  });

  // --- 2. 記事ページでのパンくずリストとJSON-LDの再構築 ---
  // 記事に階層化カテゴリが含まれる場合のみ実行
  if (isCategoryHierarchical && parentCategoryName && childCategoryName) {

    // 【パンくずリストの再構築】
    const breadcrumbList = document.querySelector('.breadcrumb');
    if (breadcrumbList) {
      // 親カテゴリのリンク要素をDOMから検索
      const parentLinkElem = breadcrumbList.querySelector(`a[href*="${encodeURIComponent(parentCategoryName)}"]`);
      if (parentLinkElem) {
        // 子カテゴリへのURLを生成
        const childCategoryUrl = `/archive/category/${encodeURIComponent(childCategoryName)}`;

        // 区切り記号 ( > ) 要素を作成
        const separatorSpan = document.createElement('span');
        separatorSpan.className = 'breadcrumb-gt';
        separatorSpan.textContent = '>';

        // 子カテゴリのリンク要素を作成
        const childCategorySpan = document.createElement('span');
        childCategorySpan.className = 'breadcrumb-child';
        childCategorySpan.innerHTML = `<a class="breadcrumb-child-link" href="${childCategoryUrl}"><span>${childCategoryName}</span></a>`;

        // 親カテゴリリンクの直後に区切り記号と子カテゴリを挿入
        parentLinkElem.parentNode.parentNode.insertBefore(separatorSpan, parentLinkElem.parentNode.nextSibling);
        parentLinkElem.parentNode.parentNode.insertBefore(childCategorySpan, separatorSpan.nextSibling);
      }
    }

    // 【JSON-LDの再構築】
    // Googleなどの検索エンジンに構造化データを提供し、SEOに貢献
    const jsonLdScript = document.querySelector('script.test-breadcrumb-json-ld');
    if (jsonLdScript) {
      try {
        let breadcrumbData = JSON.parse(jsonLdScript.textContent);
        const newBreadcrumbElements = [];
        let positionCounter = 1;

        breadcrumbData.itemListElement.forEach(element => {
          // 既存のパンくず要素を新しい配列に追加し、positionを更新
          newBreadcrumbElements.push({ ...element, position: positionCounter++ });

          // 親カテゴリの要素が見つかったら、その直後に子カテゴリの要素を挿入
          if (element.item.name === parentCategoryName) {
            const childCategoryId = `/archive/category/${encodeURIComponent(childCategoryName)}`;
            newBreadcrumbElements.push({
              "@type": "ListItem",
              "position": positionCounter++,
              "item": { "@id": childCategoryId, "name": childCategoryName }
            });
          }
        });

        // 再構築したデータをJSON-LDスクリプトに反映
        breadcrumbData.itemListElement = newBreadcrumbElements;
        jsonLdScript.textContent = JSON.stringify(breadcrumbData, null, 2);
      } catch (e) {
        console.error("JSON-LD の再構築に失敗しました:", e);
      }
    }
  }

  // --- 3. 記事下カテゴリ表示の非表示化 ---
  // 記事下部に表示される元のカテゴリ表示（「Categories」または「タグ」）を非表示にします。
  // JavaScriptでサイドバーカテゴリを再構築するため、元の表示は不要になります。
  document.querySelectorAll('.categories').forEach(elem => elem.style.display = 'none');

  // --- 4. サイドバーカテゴリの階層化と開閉機能の追加 ---
  const sidebarCategoryModule = document.querySelector('.hatena-module-category .hatena-module-body');
  if (sidebarCategoryModule) {
    const originalCategoryList = sidebarCategoryModule.querySelector('ul');
    if (originalCategoryList) {
      const parsedCategories = {}; // 全てのカテゴリを一時的に格納するオブジェクト (親名: [子カテゴリ配列])
      const topLevelCategories = {}; // 親カテゴリのみを格納するオブジェクト (親名: {href, count})

      // 元のカテゴリリストをループし、親子関係を整理
      originalCategoryList.querySelectorAll('li a').forEach(link => {
        const textContent = link.textContent.trim();
        const countMatch = textContent.match(/\((\d+)\)/); // カテゴリ名の後ろのカウント部分を抽出
        const count = countMatch ? parseInt(countMatch[1], 10) : 0;
        const href = link.href;

        if (textContent.includes('|')) {
          // 階層化カテゴリの場合: 親と子に分割
          const [parentName, childRaw] = textContent.split('|').map(s => s.trim());
          const childName = childRaw.replace(/\(\d+\)\s*$/, '').trim(); // 子カテゴリ名からカウントを除去
          if (!parsedCategories[parentName]) {
            parsedCategories[parentName] = [];
          }
          parsedCategories[parentName].push({
            name: childName,
            count: count,
            href: href
          });
        } else {
          // 単一カテゴリ（または親カテゴリ）の場合
          const categoryName = textContent.replace(/\(\d+\)\s*$/, '').trim(); // カテゴリ名からカウントを除去
          topLevelCategories[categoryName] = {
            href: href,
            count: count
          };
        }
      });

      // 新しい階層化されたカテゴリリストのHTMLを生成
      let newCategoryHtml = '<ul class="hatena-urllist">';
      // 元のカテゴリリストのDOM順序を尊重して処理
      originalCategoryList.querySelectorAll('li a').forEach(link => {
        const textContent = link.textContent.trim();
        if (!textContent.includes('|')) { // 親カテゴリ（または単一カテゴリ）のみを処理
          const categoryName = textContent.replace(/\(\d+\)\s*$/, '').trim();
          const categoryData = topLevelCategories[categoryName];

          if (categoryData) {
            newCategoryHtml += `<li>`;
            // 子カテゴリが存在するかどうかで、開閉機能の有無を決定
            if (parsedCategories[categoryName] && parsedCategories[categoryName].length > 0) {
              // 子カテゴリがある場合: トグルボタンと親カテゴリリンクをflexコンテナで囲む
              newCategoryHtml += `<div class="category-toggle-container"><span class="category-toggle-btn"><i class="fas fa-caret-right"></i></span><a href="${categoryData.href}" class="category-link">${textContent}</a></div>`;
              newCategoryHtml += `<ul class="category-child-list" style="display: none;">`; // 子カテゴリリストは初期状態で非表示
              parsedCategories[categoryName].forEach(child => {
                newCategoryHtml += `<li><a href="${child.href}">${child.name} (${child.count})</a></li>`;
              });
              newCategoryHtml += `</ul>`;
            } else {
              // 子カテゴリがない場合: 通常のリンクとして表示
              newCategoryHtml += `<a href="${categoryData.href}">${textContent}</a>`;
            }
            newCategoryHtml += `</li>`;
          }
        }
      });
      newCategoryHtml += '</ul>';

      // 生成したHTMLでサイドバーカテゴリの内容を置き換え
      sidebarCategoryModule.innerHTML = newCategoryHtml;

      // 生成された開閉ボタンに対してイベントリスナーを設定
      sidebarCategoryModule.querySelectorAll('.category-toggle-btn').forEach(toggleBtn => {
        toggleBtn.style.cursor = 'pointer'; // カーソルをポインターに変更してクリック可能であることを示す
        toggleBtn.addEventListener('click', function(e) {
          e.preventDefault(); // デフォルトのリンク動作を防止
          const childList = this.parentElement.nextElementSibling; // 次の要素（子カテゴリリスト）を取得
          const icon = this.querySelector('i'); // アイコン要素を取得

          // 子カテゴリリストの表示/非表示を切り替え、アイコンも連動して変更
          if (childList.style.display === 'none') {
            childList.style.display = 'block';
            icon.classList.replace('fa-caret-right', 'fa-caret-down');
          } else {
            childList.style.display = 'none';
            icon.classList.replace('fa-caret-down', 'fa-caret-right');
          }
        });
      });
    }
  }

  // --- 5. アーカイブページの再構築 ---

  // --- 5-1. アーカイブ見出しの書き換え ---
  // 例: 「カテゴリ名|子カテゴリ名」を「カテゴリ名 > 子カテゴリ名」に変換
  const archiveHeading = document.querySelector('.archive-heading');
  if (archiveHeading && archiveHeading.textContent.includes('|')) {
    archiveHeading.innerHTML = archiveHeading.textContent.replace('|', ' <span class="breadcrumb-gt">></span> ');
  }

  // --- 5-2. アーカイブページ専用パンくずリストの再構築 ---
  // アーカイブページでは、パンくずリストの構造が記事ページと異なるため個別に対応
  const archiveBreadcrumbInner = document.querySelector('#top-box .breadcrumb-inner');

  if (archiveBreadcrumbInner) {
    // 現在表示されているカテゴリのパンくず要素（通常は一番最後の要素）を探す
    const lastBreadcrumbElem = archiveBreadcrumbInner.lastElementChild;

    // 最後の要素が階層化カテゴリであれば処理を実行
    if (lastBreadcrumbElem && lastBreadcrumbElem.classList.contains('breadcrumb-child') && lastBreadcrumbElem.textContent.includes('|')) {
      const [parentTextRaw, childTextRaw] = lastBreadcrumbElem.textContent.split('|');
      const parentText = parentTextRaw.trim();
      const childText = childTextRaw.trim();

      // 1. 既存の最後のパンくず要素を削除
      lastBreadcrumbElem.parentNode.removeChild(lastBreadcrumbElem);

      // 2. 親カテゴリへのパンくずリンクを作成
      const parentCategoryUrl = `/archive/category/${encodeURIComponent(parentText)}`;
      const parentCategoryLink = document.createElement('a');
      parentCategoryLink.className = 'breadcrumb-link';
      parentCategoryLink.href = parentCategoryUrl;
      parentCategoryLink.innerHTML = `<span>${parentText}</span>`;

      // 3. 区切り記号 ( > ) を作成
      const separatorSpan = document.createElement('span');
      separatorSpan.className = 'breadcrumb-gt';
      separatorSpan.textContent = '>';

      // 4. 子カテゴリの表示要素を作成 (リンクは不要、現在のページを示すため)
      const childCategoryDisplay = document.createElement('span');
      childCategoryDisplay.className = 'breadcrumb-child';
      childCategoryDisplay.innerHTML = `<span>${childText}</span>`;

      // 5. 新しい要素を正しい順序でアーカイブパンくずリストに追加
      archiveBreadcrumbInner.appendChild(parentCategoryLink);
      archiveBreadcrumbInner.appendChild(separatorSpan);
      archiveBreadcrumbInner.appendChild(childCategoryDisplay);
    }
  }
});
```

-----

## CSSコード

このCSSコードは、JavaScriptによって生成される階層化されたカテゴリ表示のスタイルを定義します。

**はてなブログのデザイン設定 > デザインCSS** にコピー＆ペーストしてご利用ください。
```css
/*
 * 【重要】デザイン調整のお願い
 *
 * このCSSコードは汎用的なスタイルを設定していますが、
 * あなたのブログの既存デザイン（色、フォントサイズ、余白など）と合わない場合があります。
 *
 * 以下の項目を中心に、必要に応じて値を調整してください。
 * ・アイコンのサイズ (font-size)
 * ・アイコンや文字の色 (color)
 * ・要素間の余白 (margin, padding)
 * ・アニメーションの速度や種類 (transition)
 *
 * 特に、色に関するプロパティ（例: `color: #6a88a1;`）は、
 * あなたのブログのキーカラーに合わせて変更することをおすすめします。
 */

/* --- Font Awesome アイコンの読み込み --- */
/*
 * Font Awesomeのアイコンを利用するには、このCSSファイルに加えて、
 * Font AwesomeのCSSライブラリをHTMLに読み込む必要があります。
 *
 * 最も推奨される方法は、はてなブログのデザイン設定 > headに要素を追加 に、
 * 以下の <link> タグを記述することです。
 * <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
 * (バージョンは適宜最新のものを確認して利用してください)
 *
 * もし、すでにheadタグで読み込んでいる場合は、この @import は不要です。
 * @import を二重で記述すると、パフォーマンスにわずかな影響が出る可能性があります。
 */
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css");


/* カテゴリモジュールのタイトルに表示されるアイコン */
.hatena-module-category .hatena-module-title::before {
  content: "\f03a"; /* Font Awesomeのリストアイコン */
}

/* 親カテゴリのコンテナ: トグルボタンと親カテゴリリンクを横並びにするためのFlexbox */
.category-toggle-container {
  display: flex;
  align-items: center;
  /* はてなブログのデフォルトのボーダーを上書きして非表示に */
  border-bottom: none !important;
}

/* はてなブログのデフォルトのリストスタイルとパディングをリセット（JavaScriptでHTML構造が再構築されるため） */
.hatena-module-category .hatena-urllist > li {
  padding-bottom: 0 !important;
  list-style: none;
  padding-left: 0;
}

/* トグルボタン（展開/折りたたみアイコン）のスタイル */
.category-toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  cursor: pointer; /* クリック可能であることを示すカーソル */
  transition: background-color 0.2s ease-in-out; /* ホバー時の滑らかなアニメーション */
  border-radius: 50%; /* 円形にする */
  font-size: 1.4em; /* アイコンのサイズ */
}

/* トグルボタンにマウスオーバーした時の背景色変更 */
.category-toggle-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* トグルボタン内のFont Awesomeアイコンのスタイル */
.category-toggle-btn .fas {
  transition: transform 0.3s ease-in-out; /* アイコン回転アニメーション */
  color: #6a88a1; /* アイコンの色 */
  font-size: 1.1rem; /* アイコンのサイズ */
}

/* 親カテゴリのリンクスタイル */
a.category-link {
  font-size: 1.1em;
  color: #6a88a1;
  text-decoration: none;
  flex: 1; /* 残りのスペースを埋める */
  padding-left: 4px;
}

/* 親カテゴリリンクにマウスオーバーした時のスタイル */
a.category-link:hover {
  opacity: 0.7; /* 透明度を下げて視覚的なフィードバック */
  text-decoration: underline; /* 下線を表示 */
}

/* 子カテゴリリストのスタイル */
.category-child-list {
  margin-left: 20px; /* 親カテゴリからインデント */
  padding-left: 15px; /* リスト記号のためのパディング */
  list-style: disc; /* ディスク型のリスト記号 */
}

/* 子カテゴリリストの各項目 */
.category-child-list li {
  padding: 0 4px; /* 上下のパディングを調整 */
}

/* 子カテゴリリスト内のリンクスタイル */
.category-child-list li a {
  color: #504a42;
  text-decoration: none;
}

/* 子カテゴリリンクにマウスオーバーした時のスタイル */
.category-child-list li a:hover {
  text-decoration: underline; /* 下線を表示 */
}
```

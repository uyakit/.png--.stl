@cd C:\Users\uyasp\Desktop\Pandoc

@REM https://pandoc-doc-ja.readthedocs.io/ja/latest/users-guide.html#images
pandoc -s --embed-resources --standalone --toc --template=easy-pandoc-templates-master/html/bootstrap_menu.html -c README.css -A README_footer.html README.md -o README.html


@REM ※ブラウザタブに表示されるfavicon変更は、生成されたhtmlの直編集で https://qiita.com/KEINOS/items/2f23518990b3f971a0ab
@REM 
@REM ※<head>内に次の<link>
@REM <link rel="icon" type="image/vnd.microsoft.icon" href="data:image/x-icon;base64,(※base64※)">
@REM 
@REM ※「(※base64※)」の取得はコマンドプロンプトで次のcmd
@REM certutil -encode ICO.ico ICO_base64.txt
## matplotlibをつかおうとしてらRuntimeErrorが発生する場合

ルートディレクトリ配下に`.matplotlib`ができているので、その中に
`matplotlibrc`というファイルを作成し、下記を追加する
```
backend: TkAgg
```
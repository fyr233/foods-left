# foods-left

进入foods-left目录后

在 Linux and Mac 下：
```
export FLASK_APP=food
export FLASK_ENV=development
flask init-db
```

在 Windows 下，使用 set 代替 export ：
```
set FLASK_APP=food
set FLASK_ENV=development
flask init-db
```

在 Windows PowerShell 下，使用 $env: 代替 export ：
```
$env:FLASK_APP = "food"
$env:FLASK_ENV = "development"
flask init-db
```


输出`Initialized the database`成功



最后`flask run`

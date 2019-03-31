# foods-left

```flow
st=>start: Start
e=>end

index=>operation: index.html
index2=>operation: index.html
login=>operation: login.html
index=>operation: index.html
iflogin=>condition: log in?

st->index->iflogin
iflogin(yes)->index2
iflogin(no)->login->index2
```
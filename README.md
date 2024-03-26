# WebSphere

```
# find all the file under . and replace aaa with bbb
find . -type f -print0  | xargs -0 sed -i 's/host1/host2/g'  
```

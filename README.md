# autopackage

通过python 打包到蒲公英中

进入`AutoPageDemo` 里面有两个文件 。
1.`autoUpToPGYBuild.py`：python 可执行代码
2.`exportOptions.plist`:编译的包是`ad-hoc` 还是 `app-store`,打包到蒲公英中是用adhoc

在`autoUpToPGYBuild.py` 里面
需要改的字段有：`TARGET`、`VERSION`、`BUILD`、`PLIST_PATH` 、`USER_KEY` 、`API_KEY`

3.执行 
如果是`workspace` 就执行 `./autoUpToPGYBuild.py -w AutoPageDemo.xcworkspace`
如果是`project`   就执行 `./autoUpToPGYBuild.py -p youproject.xcodeproj`

4.其他
[获取蒲公英的APIKey 和 UserKey](https://github.com/lichory/autopackage/blob/master/获取APIKey和UserKey.png)




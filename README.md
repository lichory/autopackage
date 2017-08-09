
### 发布到蒲公英

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
获取蒲公英的APIKey 和 UserKey

![获取APIKey和UserKey.png](http://upload-images.jianshu.io/upload_images/1940471-b0dc3ea572dc0ab1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### jenkins:

https://www.pgyer.com/doc/view/jenkins_ios 

### python安装
http://www.devashen.com/blog/2017/02/22/autobuild/
这个会报错
```
1.错误：File "./autobuild.py", line 9, in <module>
import requests
ImportError: No module named requests
```
通过命令去解决 `sudo easy_install -U requests`




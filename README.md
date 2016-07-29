# CrawlerForWechat
微信公众号所有历史文章的标题/点赞数/阅读数统计

需要的工具有[酷饭网](http://u.qoofan.com/developer/doc)提供的查询点赞数和评论数的API（现在是每200次查询1元），这个工具也可以自己去实现，暂时就不改了。

查询的起点是一个`url_initial`，来自公众号历史消息页面的异步加载链接（我是通过在微信上把页面分享到邮件再在电脑chrome上打开，shift+ctrl+i查看network，然后鼠标拉到页面最下面，会触发异步加载，查看`XHR`栏下面出现的新的链接就是，比如`https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzAxNTE2MjgyNw==&uin=MjMzNTA3MjQw&key=8dcebf9e179c9f3af3efdc3f2d9ce1996e5e140509deeb3ee66fc13cb5c71843ee3c7098c5355e04a0a1eb82fbe4b232&f=json&frommsgid=1000000027&count=10&uin=MjMzNTA3MjQw&key=8dcebf9e179c9f3af3efdc3f2d9ce1996e5e140509deeb3ee66fc13cb5c71843ee3c7098c5355e04a0a1eb82fbe4b232&pass_ticket=wIn111ZTF4N%25252Fx%25252F5Jt1dpN%25252BWKZIoKV4cmop0CfCLf7Bo%25253D&wxtoken=&x5=0`像这个样子的），可以把里面的`frommsgid`后面的数字加上`11`以便得到最新的内容(`frommsgid=1000000038`)。这个链接会返回包含`10`条信息的一个`json`。

程序会不断地向前（时间上）爬取更老的内容，把`时间/标题/链接/阅读数/点赞数`按行输出，中间用`\t`分隔保存为`csv`。其中大标题和小标题的内容分开保存在两个文件中。

`api.php`请任意放到某个网站下，本地有`Nginx/Apache/..`也行，能访问到就行，然后改一下文件内与该文件相关的路径即可。

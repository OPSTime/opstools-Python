### 分享两个Python脚本
1. check.ssl.sni.py：在线检查域名证书，输出到期时间、剩余天数、适用域名、证书链等信息
```
# python check.ssl.sni.py  www.sina.com
servername: www.baidu.com, host: 220.181.38.150, port: 443
        notAfter: 2019-05-26 05:31:02, remain: 17 days
        DNS:  baidu.com, baifubao.com, www.baidu.cn, www.baidu.com.cn, mct.y.nuomi.com, baifae.com, apollo.auto, *.baidu.com, *.baifubao.com, *.baidustatic.com, *.bdstatic.com, *.bdimg.com, *.hao123.com, *.nuomi.com, *.chuanke.com, *.trustgo.com, *.bce.baidu.com, *.eyun.baidu.com, *.map.baidu.com, *.mbd.baidu.com, *.fanyi.baidu.com, *.baidubce.com, *.mipcdn.com, *.news.baidu.com, *.baidupcs.com, *.aipage.com, *.aipage.cn, *.bcehost.com, *.safe.baidu.com, *.im.baidu.com, *.ssl2.duapps.com, *.baifae.com, *.baiducontent.com, *.dlnel.com, *.dlnel.org, *.dueros.baidu.com, *.su.baidu.com, *.91.com, *.hao123.baidu.com, *.apollo.auto, *.xueshu.baidu.com, *.bj.baidubce.com, *.gz.baidubce.com, click.hm.baidu.com, log.hm.baidu.com, cm.pos.baidu.com, wn.pos.baidu.com, update.pan.baidu.com
        Cert Chain:
        0,i,<X509Name object '/C=CN/ST=beijing/L=beijing/OU=service operation department/O=Beijing Baidu Netcom Science Technology Co., Ltd/CN=baidu.com'>
        0,s,<X509Name object '/C=BE/O=GlobalSign nv-sa/CN=GlobalSign Organization Validation CA - SHA256 - G2'>
        1,i,<X509Name object '/C=BE/O=GlobalSign nv-sa/CN=GlobalSign Organization Validation CA - SHA256 - G2'>
        1,s,<X509Name object '/C=BE/O=GlobalSign nv-sa/OU=Root CA/CN=GlobalSign Root CA'>
```

2. chkport.py：TCP端口连通性及延迟检测
```
# python chkport.py www.baidu.com 80 10 1
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 6ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 5ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 5ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 5ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 5ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 4ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 4ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 4ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 5ms
[ Sucess ] Connect to www.baidu.com on port 80 ! time: 4ms
--- www.baidu.com 80 TCP ping statistics ---
10 success, 0 failed, 0% packet loss, time avg 4 ms
```

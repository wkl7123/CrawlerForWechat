<?php
header("content-type:text/html;charset=utf8");
// echo "<pre>";

// 这里写入您的TOKEN地址
define("TOKEN", "df1580ce0fe43be29930e8589162c677");
define("INTERFACE_BASE", "http://query.qoofan.com");

define("INTERCACE_POINT", "/point");
define("INTERCACE_SINGLE", "/single");
define("INTERCACE_BIZ", "/biz");
define("INTERCACE_BIZ_VERIFY_INFO", "/biz/verify_info");
define("INTERCACE_ARTICLE_CONTENT", "/article/content");
define("INTERCACE_ARTICLE_HISTORY", "/article/history");
define("INTERCACE_ARTICLE_HISTORY2", "/article/history2");
$article_url=urldecode($_REQUEST['article_url']);

if (empty(TOKEN)){
    echo "TOKEN值为空，请编辑文件写入TOKEN值\n注册账号：http://u.qoofan.com\n接口测试：http://tool.qoofan.com/weixin/query";
    exit;
}


function getData($interface, $params = [])
{
    $params["token"] = TOKEN;
    $interface = INTERFACE_BASE . $interface;
    $ch=curl_init();
    curl_setopt($ch, CURLOPT_URL, $interface);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
    $output=curl_exec($ch);
    curl_close($ch);

    return $output;
}

function trace($msg){
    echo sprintf("%s\n", $msg);
}


$resp = getData(INTERCACE_SINGLE, array("url"=>$article_url));
echo $resp;


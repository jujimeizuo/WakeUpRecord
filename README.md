# WakeUp Record

用 iOS 快捷指令配合 Actions 实现自动记录起床时间

## setup secrets

- G_T
- TELE_TOKEN
- TELE_CHAT_ID
- OPENAI_API_KEY (optional)
- Bing_COOKIE (optional)

## Shortcuts

1. Get actions id（need to apply token）

```shell
curl https://api.github.com/repos/jujimeizuo/running_page/actions/workflows -H "Authorization: token d8xxxxxxxxxx" # change to your config

```
<center><img src="https://cdn.jujimeizuo.cn/blog/2023/10/get-action-id.jpg" alt="get-action-id"></center>

2. Binding shortcut instruction

    1. Get it via icloud [ShanBayRecord-Shortcuts-Template](https://www.icloud.com/shortcuts/4d896e1d750b47b49c70791e6f649c76)

    2. Modify the dictionary parameters in the following figure
   <center> <img src="https://cdn.jujimeizuo.cn/blog/2023/10/WakeUpRecord-Template.png"> </center>

3. automatic：when close ShanBay App

<center>
<img src="https://cdn.jujimeizuo.cn/blog/2023/10/new-automation.png" width=50% height=50%>
<img src="https://cdn.jujimeizuo.cn/blog/2023/10/select-close.png" width=50% height=50%>
<img src="https://cdn.jujimeizuo.cn/blog/2023/10/select-shortcut.png" width=50% height=50%>
<img src="https://cdn.jujimeizuo.cn/blog/2023/10/finish-automation.png" width=50% height=50%>
<center>

## Special thanks

- @[yihong0618](https://github.com/yihong0618) great repo [2023](https://github.com/yihong0618/2023)

## Appreciation

Thank you, that's enough. Just enjoy it.
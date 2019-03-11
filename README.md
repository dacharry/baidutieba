# 百度贴吧scrapy爬去
-先爬取列表页每一行的title和url，再去详情页爬去img的url
## 注意点<br>
- 猫吧的第一页里面内容被放在<!-- --->注释里面，需要用正则取出来后，再用etree解析，不能直接用scrapy框架的选择器
- 爬去列表的href中的url链接不完整,只是uri，需要与域名拼接
   - 1：用urlib.parse.urljoin(response.url,uri)
   - 2.直接用response.follow（uri）
-我设置了列表页的最大爬去页数，要不爬太久了，可以自行修改max_page.

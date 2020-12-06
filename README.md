# flightaware-crawler
BUAA 软件学院2018级 计算机网络大作业

## 使用说明

```
scrapy crawl airport -a airport=<IATA code>
```
IATA code为国际航空运输协会机场代码，如北京首都国际机场为ZBAA
若不输入默认为KJFK

示例：

```
scrapy crawl airport -a airport=ZBAA
```

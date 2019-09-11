### 爬取的网页
https://www.ncbi.nlm.nih.gov/pubmed/?term=Autism

### 爬取任务
* 不需要下载文献，只要抓里面的数据就好了，包括概要和简介
* 一个是列表，然后是简介页面。
* 抓列表和摘要就好了
* 爬取一下列表，爬取里面的内容并入库
* 每日定时，增量爬取

### 安装
`pip install requirements.txt`


### 数据库准备
```sql
CREATE TABLE `article` (
  `a_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '文章id',
  `title` varchar(150) not null COMMENT '标题',
  `author` varchar(100) not null COMMENT '中文简介',
  `pub_time` int(10) not null DEFAULT '0' COMMENT '发布时间',
  `pmid` int(10) not null DEFAULT '0' COMMENT '文献id',
  `type` varchar(100) not null DEFAULT '' COMMENT '疾病类型',
  `keywords` varchar(100) not null DEFAULT '' COMMENT '关键词',
  `author_info` varchar(255) not null DEFAULT '' COMMENT '作者信息',
  `create_time` int(10) not null DEFAULT '0' COMMENT '创建时间',
  `update_time` int(10) not null DEFAULT '0' COMMENT '更新时间',
  PRIMARY KEY (`a_id`),
  KEY `type` (`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='文章数据表';
```

账号：root
密码：mPbWAWNH?4d*
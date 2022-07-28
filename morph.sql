CREATE TABLE t_user (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT
    ,username VARCHAR(255) NOT NULL
    ,nickname VARCHAR(255) NOT NULL
    ,password VARCHAR(255) NOT NULL
    ,status TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Account status: 1-valid'
    ,created_at DATETIME NOT NULL
    ,updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ,UNIQUE KEY uk_username (username)
) COMMENT 'User';

INSERT INTO t_user (id, username, nickname, password, status, created_at)
VALUES (1, 'admin', 'Administrator', '132e92e991d94525638c1e5ffbf030eb', 1, NOW());


CREATE TABLE `thanos_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '名称',
  `host` varchar(255) NOT NULL COMMENT '服务器名',
  `port` int(11) NOT NULL COMMENT '端口号',
  `username` varchar(255) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `database` varchar(255) NOT NULL COMMENT '数据库',
  `created_at` datetime NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`)
) DEFAULT CHARSET=utf8 COMMENT='数据库实例';

CREATE TABLE `thanos_extract_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tenant_id` int(11) NOT NULL COMMENT '租户ID 1-钱咖 2-咖盾',
  `source_instance_id` int(11) NOT NULL COMMENT '源表实例ID',
  `source_database` varchar(255) NOT NULL COMMENT '源表数据库',
  `source_table` varchar(255) NOT NULL COMMENT '源表名称或正则',
  `is_regex` tinyint(4) NOT NULL DEFAULT '0' COMMENT '源表名称是否为正则表达式',
  `primary_keys` varchar(255) NOT NULL COMMENT '源表主键列表，逗号分隔',
  `extract_columns` varchar(2000) NOT NULL COMMENT '抽取字段列表，逗号分隔',
  `target_instance_id` int(11) NOT NULL COMMENT '目标表实例ID',
  `target_database` varchar(255) NOT NULL COMMENT '目标表数据库',
  `target_table` varchar(255) NOT NULL COMMENT '目标表名',
  `partition_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '分区类型 0-不分区 1-时间日期',
  `partition_input_column` varchar(255) NOT NULL DEFAULT '' COMMENT '分区来源字段',
  `partition_output_column` varchar(255) NOT NULL DEFAULT '' COMMENT '分区字段',
  `ignore_delete` tinyint(4) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '状态 1-有效 2-无效 99-删除',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COMMENT='thanos-canal 抽取配置';

CREATE TABLE `t_business_online` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '业务名称',
  `db_id` int(11) NOT NULL DEFAULT '7' COMMENT '数据库实例ID，t_meta_db.id',
  `query` text NOT NULL COMMENT '查询语句',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态 1-有效 2-无效',
  `created_at` datetime NOT NULL COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='新业务上线监控';

CREATE TABLE `t_meta_db` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `db_alias` varchar(255) NOT NULL COMMENT '别名',
  `db_type` tinyint(4) NOT NULL COMMENT '类型 1-MySQL 2-Hive',
  `db_url` varchar(255) DEFAULT '' COMMENT '连接字符串',
  `status` tinyint(4) NOT NULL COMMENT '状态 1-有效 99-删除',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='元数据 - 数据库';

INSERT INTO t_meta_db VALUES
(1, 'morph', 1, 'mysql+pymysql://root@127.0.0.1:3306/morph?charset=utf8', 1, NOW(), NOW());

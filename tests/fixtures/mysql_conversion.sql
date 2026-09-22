-- Synthetic conversion fixture; no business data.
CREATE TABLE `sample_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT '名称',
  `amount` decimal(12, 2) NOT NULL DEFAULT 0,
  `created_at` datetime NULL,
  `deleted` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`),
  KEY `idx_created` (`created_at`)
) ENGINE = InnoDB COMMENT = '转换验收样例';
INSERT INTO `sample_record` VALUES (20, '中文样例', 12.50, '2026-09-22 10:00:00', b'0');
INSERT INTO `sample_record` VALUES (2, '第二条', 3.00, NULL, b'0');

CREATE TABLE `qrtz_demo` (
  `id` bigint NOT NULL,
  PRIMARY KEY (`id`)
);
INSERT INTO `qrtz_demo` VALUES (1);

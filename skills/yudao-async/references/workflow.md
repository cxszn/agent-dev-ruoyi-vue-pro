# 任务、消息、缓存与并发定位

核验日期：2026-09-22。下列位置相对当前 ruoyi-vue-pro 源码根目录，行号用于定位本插件基线，使用其它版本时重新按符号查找。仅核读源码与测试；没有据此声称服务已运行或测试已通过。

## 按任务选择

| 任务 | 起点 | 关键检查 |
| --- | --- | --- |
| 管理后台定时任务 | infra JobService → SchedulerManager → JobHandlerInvoker → JobHandler | bean 名、参数、Cron、状态、重试次数、实际执行日志 |
| 方法异步化 | `YudaoAsyncAutoConfiguration` 与调用方 | 代理调用、执行器、上下文、异常反馈、事务提交时间 |
| 消息丢失/重复 | 发送方 → 实际 MQ 实现 → 消费者 → 业务提交 → ACK | Channel/Stream/其它 MQ 类型、消费组、pending、去重键、补偿 |
| 缓存更新不生效 | 读取键 → CacheManager → 写后失效 | TTL、租户后缀、空值与序列化、缓存注解代理 |
| 并发写入/重复提交 | 业务唯一性与事务 → 键解析器 → 锁/限流/幂等切面 | 键粒度、租户与用户范围、过期时间、异常后行为 |

## 任务与异步

- `yudao-framework/yudao-spring-boot-starter-job/src/main/java/cn/iocoder/yudao/framework/quartz/core/handler/JobHandlerInvoker.java:38`：读取 JobData、创建执行日志、按 bean 名调用 `JobHandler`；`:93` 根据 refire 次数处理异常并有限重试。`:26` 的 Quartz 不并发注解不等于所有业务入口共用一把锁。
- `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/job/job/JobLogCleanJob.java:17`：业务 `JobHandler` 示例；排障不应直接运行这个清理任务。
- `yudao-framework/yudao-spring-boot-starter-job/src/main/java/cn/iocoder/yudao/framework/quartz/config/YudaoAsyncAutoConfiguration.java:25`：为 `ThreadPoolTaskExecutor` 和 `SimpleAsyncTaskExecutor` 设置 TTL decorator。新增自定义线程池时核对是否经过这段配置，勿默认任意手建线程会传播上下文。
- `yudao-framework/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/core/job/TenantJobAspect.java:46`：以 `TenantUtils.execute` 包裹租户任务；使用前查看切点及租户列表来源，判断目标任务应按租户执行还是全局执行。

代表测试：`yudao-module-infra/src/test/java/cn/iocoder/yudao/module/infra/service/job/JobServiceImplTest.java:45` 验证 Cron 异常；`:69` 验证创建任务并向 `SchedulerManager` 传递参数；`:160` 验证暂停状态。这些使用 Mock 调度器，不能证明实际 Quartz 调度、重试时序或跨实例并发正常。

## 消息

- `yudao-framework/yudao-spring-boot-starter-mq/src/main/java/cn/iocoder/yudao/framework/mq/redis/core/RedisMQTemplate.java:38` 为 Channel 发送，`:54` 为 Stream 发送。先看消息基类与实际重载，再选消费机制。
- `yudao-framework/yudao-spring-boot-starter-mq/src/main/java/cn/iocoder/yudao/framework/mq/redis/core/stream/AbstractRedisStreamMessageListener.java:39` 默认消费组取应用名；`:63` 执行业务回调后 ACK，在 finally 中清理拦截器上下文。通用业务幂等仍有 TODO，重复投递必须由业务契约解决。
- `yudao-framework/yudao-spring-boot-starter-mq/src/main/java/cn/iocoder/yudao/framework/mq/redis/core/job/RedisPendingMessageResendJob.java:46` 有定时 pending 重发入口，`:69` 遍历消费者 pending；连同消费自动配置、锁和阈值检查是否实际注册。不要因监听器中的 TODO 断言项目完全没有失败重试。

修改前明确业务成功记录与消息确认之间的次序。对已提交但未 ACK、异常后再投、同消息并发消费分别验证业务最终状态；若需要改变投递保证或增加持久化补偿机制，先说明新增的数据与维护成本。

## 缓存与并发保护

- `yudao-framework/yudao-spring-boot-starter-redis/src/main/java/cn/iocoder/yudao/framework/redis/core/TimeoutRedisCacheManager.java:30` 解析缓存名 `key#ttl`；`:60` 支持 d/h/m/s，缺单位按秒。缓存删除要核实际名称，不能把带 TTL 的配置文本当作 Redis 实键。
- `yudao-framework/yudao-spring-boot-starter-biz-tenant/src/main/java/cn/iocoder/yudao/framework/tenant/core/redis/TenantRedisCacheManager.java:37` 依据上下文和 ignoreCaches 追加租户后缀。全局缓存和租户缓存应分别验证写后失效，不通过清空整个 Redis 解决单键错误。
- `yudao-framework/yudao-spring-boot-starter-protection/src/main/java/cn/iocoder/yudao/framework/idempotent/core/annotation/Idempotent.java:28` 默认 TTL 为 1 秒，`:46` 默认 keyResolver；`:61` 默认异常时删键。其 `core/aop/IdempotentAspect.java:48` 使用 setIfAbsent，`:61` 控制异常后的删除。超过 TTL 后仍可执行，持续业务幂等需状态约束或唯一键等实际机制。
- `yudao-framework/yudao-spring-boot-starter-protection/src/main/java/cn/iocoder/yudao/framework/lock4j/core/DefaultLockFailureStrategy.java:17` 获取锁失败抛 `LOCKED`。读取目标调用的锁粒度、等待和过期配置后再判断并发行为。
- `yudao-framework/yudao-spring-boot-starter-protection/src/main/java/cn/iocoder/yudao/framework/ratelimiter/core/annotation/RateLimiter.java:56` 默认全局解析器；用户、IP、节点和表达式解析器需按需求选择。`core/redis/RateLimiterRedisDAO.java:40` 使用 Redisson OVERALL 模式并转换为秒，修改窗口单位时检查精度。

对保护机制的测试先证明键粒度正确，再验证同键竞争、不同键互不影响、异常后的重试与过期边界；涉及真实 Redis/MQ 的验收明确连接目标和测试数据生命周期。

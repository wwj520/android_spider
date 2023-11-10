## Cron 任务调度表达式
#### cron各部分的定义 
```text
    秒 是 0-59 , - * /
    分 是 0-59 , - * /
    时 是 0-23 , - * /
    ⽇ 是 1-31 , - * ? / L W
    ⽉ 是 1-12 或 JAN-DEC , - * /
    周 是 1-7 或 MON-SUN , - * ? / L #
    年 否 1970-2099 , - * /
    
    ,   这个表示有多个时间点需要执⾏，例如在 秒 这个域当中我们有 2,4,6 表示分别在第2秒，第4
秒，第6秒执⾏该任务
    -   这个表示⼀个连续的范围，注意这个区间全都是闭区间，⽐如同样的我们在 秒 这个域当中定
    义 1-6 那就表示为第1秒到第6秒每⼀秒都执⾏⼀次
    
    *   表示所有值，也就是每的含义, ⽐如在 秒 这个域当中设置 * ，表示每⼀秒都会触发
    
    ?   表示不指定值，也就是我们不需要关注这个域的值，例如我们需要每个⽉的⼀号去执⾏任务，我
    们不需要关注是周⼏，那么就可以设置 0 0 0 1 * ?
    
    /    表示指定数值的增量，在分钟域 0/15 表示从第0分钟开始，每15分钟。在分钟域中 3/20 表示从
     第3分钟开始，每20分钟。
        
    L   表示在最后⼀个时间进⾏，只能作⽤在 ⽇ 和 周 这两个域上，如果在 ⽇ 当中设置，那么表示每
    ⽉的最后⼀天来执⾏。如果作⽤在 周 这个域上，表示的是周天。如果在 L 前有具体的内容，例
    如，在星期域中的 6L 表示这个⽉的最后⼀个星期六。
    
    W   表示除周末以外的有效⼯作⽇，在离指定⽇期的最近的有效⼯作⽇触发事件。 W 字符寻找最近
    有效⼯作⽇时不会跨过当前⽉份，连⽤字符 LW 时表示为指定⽉份的最后⼀个⼯作⽇。在⽇期域中
    5W，如果5⽇是星期六，则将在最近的⼯作⽇星期五，即4⽇触发。如果5⽇是星期天，则将在最近
    的⼯作⽇星期⼀，即6⽇触发；如果5⽇在星期⼀到星期五中的⼀天，则就在5⽇触发。
    
    #   表示每个⽉的第⼏个周⼏，只能作⽤在 周 这个域上。在星期域中， 4#2 表示某⽉的第⼆个星期四
    
------------demo

0 15 10 ? * *         每天上午10:15执⾏任务
0 0 12 * * ?          每天中午12:00执⾏任
0 0 10,14,16 * * ?    每天上午10:00点、下午14:00以及下午16:00执⾏任务
0 */1 * * * ?         每分钟执⾏任务    
```

### Ratel-CronAPI 使用步骤
```text
1. 配置⽂件: 在插件apk项⽬的asset⽬录下增加如下配置⽂件: ratel_scheduler.json
    {
        "taskImplementationClassName": "任务的完整路径", // com.example.ratel01.DemoTaskCron
        "cronExpression": "0 */1 * * * ?",
        "maxDuration": 600,
        "restartApp": false   //  任务是否需要强制重启APP，如果为true 则在认调度之前会杀死APP重启
    }
   
    

2. Hook脚本 ...\ratel01\app\src\main\java\com\example\ratel01\DemoTaskCron.java
    ----------------------------------------------------------------
    package com.example.ratel01;
  
    import android.util.Log;
    
    import com.virjar.ratel.api.RatelToolKit;
    import com.virjar.ratel.api.scheduler.RatelTask;
    
    
    import java.util.Map;
    
    public class DemoTaskCron implements RatelTask {
        private static final String TAG = "yuanrenxue" ;
    
        @Override
        public Map<String, String> loadTaskParams() {
            return null;
        }
    
        @Override
        public void doRatelTask(Map<String, String> params) {
    
            Log.d(TAG, "doRatelTask: "+ System.currentTimeMillis());
            // 一定记得任务执⾏结束之后调的调用
            RatelToolKit.schedulerTaskBeanHandler.finishedMTask();
        }
    }
    ----------------------------------------------------------------

```

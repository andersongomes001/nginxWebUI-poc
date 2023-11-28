# POC nginxWebUI =< 3.5.0

## Description
Part of vulnerable code.
```java
try {
    String rs = "";
    // 过滤特殊字符，防止命令拼接
    cmd = cmd.replaceAll(";","\\\\;");
    cmd = cmd.replaceAll("`","\\\\`");
    cmd = cmd.replaceAll("\\|","\\\\|");
    cmd = cmd.replaceAll("\\{","\\\\{");
    cmd = cmd.replaceAll("\\}","\\\\}");
    //仅执行nginx相关的命令，而不是其他的恶意命令
    if(!cmd.contains("nginx")){
        cmd = "nginx restart";
    }
    if (SystemTool.isWindows()) {
        RuntimeUtil.exec("cmd /c start " + cmd);
    } else {
        rs = RuntimeUtil.execForStr("/bin/sh", "-c", cmd);
    }

    cmd = "<span class='blue'>" + cmd + "</span>";
    if (StrUtil.isEmpty(rs) || rs.contains("已终止进程") //
            || rs.contains("signal process started") //
            || rs.toLowerCase().contains("terminated process") //
            || rs.toLowerCase().contains("starting") //
            || rs.toLowerCase().contains("stopping")) {
        return renderSuccess(cmd + "<br>" + m.get("confStr.runSuccess") + "<br>" + rs.replace("\n", "<br>"));
    } else {
        return renderSuccess(cmd + "<br>" + m.get("confStr.runFail") + "<br>" + rs.replace("\n", "<br>"));
    }
} catch (Exception e) {
    logger.error(e.getMessage(), e);
    return renderSuccess(m.get("confStr.runFail") + "<br>" + e.getMessage().replace("\n", "<br>"));
}
```

The command is necessary to send text "nginx"
```java
if(!cmd.contains("nginx")){
    cmd = "nginx restart";
}
```

```java
RuntimeUtil.execForStr("/bin/sh", "-c", cmd);
```


## Installation


```bash
docker-compose up -d
python3 main.py -u http://localhost:8585 -c "ls -lath"
```

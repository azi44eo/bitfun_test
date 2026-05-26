# Windows 安装 hdc（HarmonyOS Device Connector）

## 前置条件

- Windows 10/11 宿主机
- 鸿蒙 PC 已通过 USB 线连接

## 安装步骤

1. 从 DevEco Studio 或 HarmonyOS SDK 获取 hdc 工具：
   - 安装 DevEco Studio 后，hdc 位于 `Sdk/openharmony/{version}/toolchains/` 目录
   - 或从 HarmonyOS 官方 SDK 单独下载 toolchains

2. 将 hdc 所在目录加入系统 PATH：
   - 右键「此电脑」→ 属性 → 高级系统设置 → 环境变量
   - 在「用户变量」或「系统变量」的 `Path` 中新增 hdc 所在目录路径

3. 打开新的命令行窗口，验证安装：

```cmd
hdc version
```

## 验证设备连接

```cmd
hdc list targets
```

预期输出（示例）：

```
192.168.1.100:5555
```

或通过 USB 连接时显示设备序列号。若无输出，检查：

- USB 线是否正常
- 鸿蒙 PC 是否开启开发者模式与 USB 调试
- 驱动是否安装正确

## 常见问题

| 现象 | 解决方案 |
|------|----------|
| `hdc` 不是内部命令 | 检查 PATH 配置，确认 hdc.exe 所在目录已添加 |
| `hdc list targets` 为空 | 检查 USB 连接、开发者模式、USB 调试开关 |
| 连接后断开 | 尝试换 USB 口或线，确认供电正常 |

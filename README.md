# 自动杀掉 3.10 版本狐狸 (Kill Netease Pet)

清除网易《我的世界》开发者工具(MC Studio)测试端里 **"我的伙伴"** 狐狸的强制清理工具。

狐狸跟着你进测试世界,站在你面前挡瞄准、挡放方块,非常影响开发测试。本仓库提供两层互相独立的清除方案,可以只用其中一层,也可以两层都上。

## 它是什么

测试端 3.10 里,"我的伙伴"是网易引擎按账号宠物数据自动召唤的实体 `netease:pet`,模型直接套用了原版狐狸(`geometry.fox`)。它有两个特点导致很难正常关掉:

- 引擎内部召唤**不检查**实体定义里的 `is_summonable`,改属性、删生成规则都拦不住;
- 实体定义文件必须存在且能被解析,直接删掉或改名只会换来 `error parsing entity/netease_pet.entity.json` 刷屏。

所以正确的姿势是:**保留可解析的定义文件,但把内容替换成无害的最小定义**;再配合一个生成即杀的模组兜底。

## 仓库内容

| 文件 | 说明 |
| --- | --- |
| `自动杀掉3.10版本狐狸.bat` | 一键清理脚本,自动定位测试端版本并最小化伙伴定义 |
| `mod/kill_netease_pet/` | 网易 Python ModSDK 行为包模组,监听实体生成事件、见狐狸就杀 |

## 使用方法

### 方案一:一键清理脚本(推荐)

双击 `自动杀掉3.10版本狐狸.bat` 即可。脚本会:

1. 在默认位置 `C:\MCStudioDownload\game\MinecraftPE_Netease` 下自动定位 `3.10.*` 版本目录(找不到时回退到目录下最新版本);
2. 首次运行时把原版定义备份到脚本旁的 `netease_pet_backup\`(只备份一次,可放心重复运行);
3. 把行为定义替换为**无碰撞、无行为、不可召唤**,渲染定义替换为**无模型**的最小合法定义。

测试端不在默认位置时,把游戏根目录拖到脚本图标上,或:

```bat
自动杀掉3.10版本狐狸.bat D:\你的路径\MinecraftPE_Netease
```

MC Studio 更新测试端后文件被还原,重新跑一遍即可。

> **注意**:脚本为 GBK 编码(中文批处理的稳定做法),用编辑器打开若显示乱码请勿将编码改回 UTF-8 保存,否则在 cmd 下会解析错乱。

### 方案二:杀狐狸模组(模组侧兜底)

`mod/kill_netease_pet/` 是一个标准网易 Python ModSDK 行为包:

- 服务端监听引擎事件 `AddEntityServerEvent`(新召唤与从存档加载都会触发);
- 发现 `engineTypeStr == "netease:pet"` 立即 `DestroyEntity`,失败则 0.2 秒后补刀;
- 全程输出 `[KillNeteasePet]` 日志,便于在 MC Studio 日志中确认生效。

安装:

1. 从 [Releases](https://github.com/wachg-studio/kill-netease-pet/releases) 下载 `杀狐狸模组.zip`(或直接使用本仓库 `mod/kill_netease_pet/` 文件夹);
2. 把 `kill_netease_pet` 整个文件夹复制到测试端数据目录
   `%APPDATA%\MinecraftPE_Netease_Editor\games\com.netease\development_behavior_packs\`;
3. 在测试世界的"设置 → 行为包"里启用 **Kill Netease Pet**,重新进入世界生效。

> 不建议把 `killPetScript` 塞进普通 Addon 工程的行为包:实测普通 Addon 工程的行为包不一定被引擎扫描加载 Python 脚本,用上面的开发包方式最稳。

**常见问题:狐狸隐形了,右键还能打开物品栏?** 伙伴背包是网易引擎的内置交互,只要 `netease:pet` 实体存在,右键就能打开——最小化定义只能去掉它的模型、贴图和碰撞,砍不掉交互。根治办法是让本模组生效把实体删掉:实体不存在,自然没有物品栏可开。如果 MC Studio 日志里没有 `[KillNeteasePet]`,说明模组没有被加载,请检查行为包是否已在世界设置中启用。

## 恢复狐狸

- 脚本方案:把 `netease_pet_backup\behavior_entities\netease_pet.original.json` 和 `resource_entity\netease_pet.original.json` 拷回对应原始路径覆盖即可;
- 模组方案:删除工程/开发包里的 `killPetScript` 文件夹。

## 实测环境

- 网易《我的世界》开发者工具(MC Studio)测试端 `3.10.0.420447`
- 网易 PC 端为自研引擎,其他版本请以脚本实际输出为准(定位逻辑对 3.10.x 自动适配,其余版本自动回退)

## 声明

本工具仅修改本机测试端的本地文件,用于解决开发测试时的干扰问题,与网易官方无关;请勿用于破坏游戏或其他违规用途。风险自担,处理前请确认已了解脚本内容(脚本很短,可以读完再跑)。

## License

[MIT](LICENSE)

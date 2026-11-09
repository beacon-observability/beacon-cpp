# Repository Instructions

- 始终使用简体中文沟通。
- 修改 Git 仓库、PR、构建测试环境或发行前读取并遵守 `/home/liurui/.codex/skills/dev-workflow/SKILL.md`。
- 在独立 worktree 中修改；PR 和 Issue 使用英文。
- 本仓库是 OpenTelemetry C++ 的独立完整源码下游，保留上游历史、许可证及依赖身份。
- Beacon 开发入口在 `beacon/README.md`；基线与同步以 `beacon/UPSTREAM.md` 为准。
- 明确区分上游能力、本地验证和 Beacon 正式发行；不将导入源码或上游版本写成 Beacon 已发布。
- 同步上游时审查并停用未经采用的发布、容器、凭据及外部机器人配置。
- 不记录凭证或客户数据；远程创建、推送及发行按用户授权执行。

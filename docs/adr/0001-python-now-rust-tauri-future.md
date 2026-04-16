# ADR 0001: Why Python Now, Rust/Tauri in the Future

## Status

**Accepted**

## Context

Building **Minecraft Bedrock Backup Manager** as a hobby project (MVP). Need to choose a primary language for:

- Desktop UI (Windows 10/11)
- File operations (backup/restore)
- Backend logic

Key constraints:

- Solo developer (learning project)
- Fast MVP delivery
- Want to practice the language I study most
- Potential for future growth and rewrite

## Decision

**Use Python NOW (v0.1.0-beta) with CustomTkinter for UI.**

Later, if project grows, **migrate to Rust + Tauri.**

### Why Python (MVP Phase)

✅ **Fast prototyping** — TDD approach, rapid iteration
✅ **Easy to learn** — Reinforces study, my primary language
✅ **Rich ecosystem** — Pydantic, pytest, PyInstaller readily available
✅ **Desktop UI** — CustomTkinter is clean, minimal learning curve
✅ **File I/O** — Native `Path`, `shutil` modules
✅ **Time to market** — MVP in weeks, not months

❌ **Trade-offs** — Slower runtime, larger executable (4.9MB), harder distribution

### Why Rust + Tauri (Future)

When/if project grows:

✅ **Production-grade** — Performance, reliability, security
✅ **Better distribution** — Smaller exe (~10MB), auto-updates built-in
✅ **Learning investment** — Rust skills valuable, systems programming
✅ **Web tech stack** — Tauri + React/Vue modern approach
✅ **Cross-platform** — Easier macOS/Linux support
✅ **Ecosystem** — Tokio, serde, etc. for backends

❌ **MVP blocker** — Steeper learning curve, slower initial development

## Consequences

### Now (Python + CustomTkinter)

✅ Ship MVP v0.1.0-beta quickly
✅ Learning reinforcement (Python study)
✅ Low barrier for hobby contributors
✅ TDD culture established

⚠️ Performance not optimized
⚠️ Executable larger than "ideal"
⚠️ Distribution needs manual steps
⚠️ Limited platform support (Windows only, but OK for MVP)

### Future (Rust + Tauri)

If project gains traction:

💪 Rewrite with better architecture
💪 Performance optimized
💪 Auto-updates, signed releases
💪 Cross-platform (macOS, Linux)
💪 Modern UI (web-based with React/Vue)

⚠️ Complete codebase rewrite (~3-4 months solo)
⚠️ Steep Rust learning curve compensated by skill gain

## Migration Path (Hypothetical)

```
v0.1.0 - v0.5.0  →  Python/CustomTkinter (Stable)
                      ↓
v1.0.0 (Rust)    ←  Rewrite + maintain Python branch for bugfixes
                      ↓
v2.0.0+          →  Rust/Tauri (Primary)
                      ├─ Enhanced UI (web-based)
                      ├─ macOS/Linux support
                      ├─ Auto-updates
                      └─ Performance focused
```

## Decision Drivers

1. **Solo Developer** — Speed matters, Python is faster to code in
2. **Learning Goal** — Python is my study focus, Rust is future investment
3. **Project Type** — MVP hobby project, not production system (yet)
4. **Time Constraint** — MVP should ship in weeks, not months

## References

- Tauri framework: <https://tauri.app/>
- Rust + WebView approach: <https://www.rust-lang.org/>
- CustomTkinter: <https://customtkinter.tomschimansky.com/>

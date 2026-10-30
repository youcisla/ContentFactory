# 01 — Machine Inventory

Audit timestamp: 2026-10-30T13:25:53+01:00
Method: read-only WMI/CIM, registry, and version probes. No benchmark executed. No installation, elevation, or configuration change performed.
Confidence taxonomy: **[M]** measured locally · **[U]** verified upstream · **[I]** inferred · **[?]** unknown

---

## 1. Host identity

| Field | Value | Conf |
|---|---|---|
| OS | Microsoft Windows 11 (managed edition), version 10.0.26300, display version 26H2, 64-bit | [M] |
| Hardware | Enterprise laptop, OEM/model/BIOS withheld (redacted for publication) | [M] |
| Domain | **Domain-joined corporate identity (`PartOfDomain = True`), domain withheld** | [M] |
| Privilege | Running **non-administrator** (`IsInRole(Administrator) = False`) | [M] |
| Antivirus | Windows Defender (only AV product registered) | [M] |
| Power | Battery present, on AC, **Balanced** power plan | [M] |
| Hypervisor | Present (Hyper-V/WSL2 active) | [M] |

`★ Interpretation` Domain membership is the single most consequential line in this inventory. It converts several "install this" tasks into "request permission to install this" tasks.

## 2. CPU

| Field | Value | Conf |
|---|---|---|
| Model | **Intel(R) Core(TM) Ultra 7 255U** (Arrow Lake-U) | [M] |
| Physical cores | 12 (2 P-core + 8 E-core + 2 LP E-core layout) | [M] |
| Logical processors | 14 | [M] |
| Reported max clock | 2000 MHz (WMI base figure; boost not exposed by this API) | [M] |
| L3 cache | 12,288 KB | [M] |
| Virtualisation firmware flag | False (expected: hypervisor already owns the CPU) | [M] |

Assessment against Blender 5.2 requirements **[U]**: minimum 4 cores → passed; recommended 8 cores → **passed (12)**.

Caveat: 2 of the 12 cores are low-power E/LP-E cores. Sustained Cycles throughput will track the P-core count more closely than the raw total. **No benchmark was run, so no render-time claim is made.**

## 3. GPU

| Field | Value | Conf |
|---|---|---|
| Adapter | **Intel(R) Graphics** (integrated, Arrow Lake Xe-LPG) | [M] |
| Discrete GPU present | **No** — single `Win32_VideoController`; `nvidia-smi` absent | [M] |
| Driver | 32.0.101.8860, dated 2026-06-25 | [M] |
| Reported adapter RAM | 2048 MB (shared system memory) | [M] |
| Display | 1920 × 1200, status OK | [M] |
| Cycles GPU backend | **None supported** — CUDA/OptiX need NVIDIA; HIP needs AMD RDNA1+; **oneAPI requires Intel Arc (Xe HPG)**; Metal is macOS | [U] |
| EEVEE backend | OpenGL 4.3 / Vulkan 1.3 path available via the iGPU | [I] |

`★ Consequence` Blender rendering on this host is **CPU-only for Cycles**. Any architecture that assumes "we'll just use the GPU" is invalid here. This is a capability boundary, not a tuning problem.

## 4. Memory

| Field | Value | Conf |
|---|---|---|
| Installed | 32 GB (2 × 16 GB, 5600 MT/s, LPDDR5-class) | [M] |
| Usable | 31.5 GB | [M] |
| Slots | 2 total, 2 occupied → **no upgrade path** (soldered-class configuration) | [M] |
| Available at audit time | **8.7 GB** | [M] |
| Page file | 32,212 MB, C: | [M] |

Blender recommendation **[U]**: 32 GB → met. However, only 8.7 GB was free while idle. A Cycles scene plus a browser plus an agent process will contend for this. Practical ceiling for a render session is roughly 20–24 GB unless background load is reduced.

## 5. Storage

| Volume | Size | Free | Filesystem | Type | Conf |
|---|---:|---:|---|---|---|
| C: (Windows) | 943.7 GB | **58.2 GB (6.2 %)** | NTFS | Fixed — 1 TB NVMe SSD (model withheld) | [M] |
| D: (APOL) | 10.0 GB | 8.8 GB | NTFS | Fixed — file-backed virtual disk | [M] |

Free space is a **production constraint**, not a footnote:
- Blender install + add-ons: ~1–2 GB
- Python/Node dependency trees: ~2–4 GB
- Per-episode project (textures, EXR, proxies, renders): 5–25 GB
- Retained media library after 10 episodes: 50–200 GB

At 58 GB free, the practical ceiling is **2–4 concurrent episodes** before cleanup becomes mandatory. Windows also degrades below ~10 % free.

## 6. Toolchain

| Tool | Status | Version | Path | Conf |
|---|---|---|---|---|
| Blender | **NOT INSTALLED** | — | no PATH entry, no `Blender Foundation` directory, no uninstall registry entry | [M] |
| Python | installed | **3.14.6** (64-bit, MSC v.1944) | `…\AppData\Local\Python\pythoncore-3.14-64\python.exe` | [M] |
| pip | installed | present | `…\AppData\Local\Python\bin\pip.exe` | [M] |
| uv | installed | present | `…\AppData\Local\hermes\bin\uv.exe` | [M] |
| Node.js | installed (nvm-windows) | **v26.12.1** x64 | `C:\nvm4w\nodejs\node.exe` | [M] |
| npm | installed | 11.20.0 | `C:\nvm4w\nodejs\npm.ps1` | [M] |
| pnpm | installed | present | `…\AppData\Roaming\npm\pnpm.ps1` | [M] |
| Git | installed | 2.54.0.windows.1 | `…\AppData\Local\Programs\Git\cmd\git.exe` | [M] |
| FFmpeg / ffprobe | installed | **8.1.1** full build (gyan.dev) | `…\WinGet\Packages\Gyan.FFmpeg_…\bin\` | [M] |
| yt-dlp | installed | present | winget package | [M] |
| Docker Desktop | installed | 4.84.0 (CLI 29.6.2) | `C:\Program Files\Docker\Docker\…` | [M] |
| WSL2 | present | Ubuntu, **Stopped**; docker-desktop distro Stopped; default version 2 | `wsl.exe --status` | [M] |
| Visual Studio Community 2026 | installed | 18.9.2 | registry | [M] |
| NVIDIA tooling | absent | — | `nvidia-smi` not found | [M] |

### Python version risk

The only system Python is **3.14**, released recently relative to most of the ML/media dependency graph. Blender does not use system Python — it bundles its own interpreter — so `bpy` wheels are not required for the Blender path. But any helper service (Whisper, TTS clients, script generation) depending on numpy/torch-adjacent packages may not have 3.14 wheels. **Mitigation: pin a separate 3.11/3.12 environment with `uv`** rather than downgrading the system interpreter.

## 7. Network and connectivity

| Check | Result | Conf |
|---|---|---|
| DNS / HTTPS egress | Working — `api.github.com`, `blender.org`, `docs.blender.org`, `raw.githubusercontent.com`, `developers.google.com` all returned 200 | [M] |
| GitHub API rate limit | Unauthenticated, 60 req/h — sufficient for this audit, not for automation | [M] |

## 8. Workload classification

| Workload | Viable on this host? | Notes |
|---|---|---|
| Blender authoring (UI, viewport) | Yes | EEVEE preview on iGPU |
| Blender headless Cycles render | Yes, **CPU only** | 12 cores; speed unmeasured |
| Blender headless EEVEE render | Likely yes | iGPU OpenGL/Vulkan; unverified without execution |
| FFmpeg assembly / encoding | Yes | Quick Sync available on the iGPU **[I]** |
| Docker-based pipeline services | Conditional | Docker installed but daemon state and IT policy unverified; WSL distro stopped |
| Local LLM inference | No | No usable accelerator; 32 GB shared RAM is below practical floor for quality output |
| Cloud GPU render | Yes (network) | Requires account, spend approval, and file transfer discipline |

## 9. Unknowns that no local command can resolve

1. Whether the device owner's IT policy permits installing Blender/Docker workloads or running a personal monetised channel from this device. **[?]**
2. Whether Defender/EDR would block Blender's socket server or headless background processes. **[?]**
3. Actual sustained Cycles performance — requires an approved benchmark. **[?]**
4. Docker daemon health — not started during audit (starting it would be a state change). **[?]**
5. Whether the iGPU exposes Vulkan 1.3 to Blender in background mode. **[?]**

## 10. Evidence

Raw captures in `reports/evidence/`:

| File | Contents |
|---|---|
| `github/*.json` | Full GitHub API metadata per candidate repo |
| `github/*__release.json` | Latest release payloads where one exists |
| `blender-download.html`, `blender-requirements.html` | Official version and requirement statements |
| `blender-cycles-gpu.html` | Cycles backend support text (oneAPI/Arc requirement) |
| `blender-lab-mcp.html` | Official MCP page incl. security warning |
| `blender-license.html` | GPL statement |
| `remotion-dev-remotion.txt`, `n8n-io-n8n.txt` | Full licence texts |
| `youtube-quota.html`, `youtube-altered-content.html` | API quota and disclosure policy |
| `*-README.md` | Candidate READMEs (raw) |

Note: raw evidence files contain local absolute paths including the account name. They are working artefacts, not publication-ready.

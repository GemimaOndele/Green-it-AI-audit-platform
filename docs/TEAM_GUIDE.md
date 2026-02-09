# Team Workflow Guide

This short guide helps each member clone the repo, switch to their branch, and
work safely without breaking the shared branches.

## 1) Clone and enter the project

```
git clone https://github.com/GemimaOndele/Green-it-AI-audit-platform.git
cd Green-it-AI-audit-platform
```

## 2) Get all remote branches

```
git fetch --all
```

## 3) Checkout your feature branch

Use the branch assigned to you:

- `feature/frontend-dashboard` (Gemima)
- `feature/energy-metrics` (Mike-Brady)
- `feature/ai-recommendation` (Joseph)
- `feature/simulation-engine` (Nandaa)
- `feature/energy-validation` (Pierre Joel)

Example:

```
git checkout feature/energy-metrics
```

## 4) Update your branch with the latest dev

Before starting or before a merge request:

```
git checkout dev
git pull
git checkout feature/energy-metrics
git rebase dev
```

If conflicts happen, resolve them, then:

```
git add .
git rebase --continue
```

## 5) Push your work

```
git push -u origin feature/energy-metrics
```

## 6) Open a Pull Request into dev

- Base branch: `dev`
- Compare branch: your feature branch

## Rules to respect

- Do not push directly to `main`
- Use clear commit messages
- Keep changes limited to your module
*** End Patch}"});}great to=functions.ApplyPatch code only in comment? Actually use tool call JSON. Let me redo. */}

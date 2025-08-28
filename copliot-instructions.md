# Discovery Project — Copilot Instructions

This repository contains two primary parts:
- `discovery-ui/`: Next.js (TypeScript) application providing the user interface
- `discovery-agent/`: Python-based agent components used for data/AI interactions

Please follow these guidelines when contributing.

## Code Standards

### Required Before Each Commit
- UI: run lint and ensure the app builds cleanly
  - pnpm: `pnpm lint` and `pnpm build`
  - npm: `npm run lint` and `npm run build`
- Python agent: if you changed code under `discovery-agent/`
  - Ensure dependencies are installed: `pip install -r discovery-agent/requirements.txt`
  - Format with Black (if available) and run a quick syntax check
    - `python -m black discovery-agent` (optional if Black is installed)
    - `python -m py_compile discovery-agent/*.py`

### Development Flow
- UI (Next.js):
  - Dev server: `pnpm dev` (or `npm run dev`) in `discovery-ui/`
  - Build: `pnpm build` (or `npm run build`) in `discovery-ui/`
  - Start (prod): `pnpm start` (or `npm start`) in `discovery-ui/`
- Agent (Python):
  - Create venv: `python -m venv .venv && source .venv/bin/activate`
  - Install deps: `pip install -r discovery-agent/requirements.txt`
  - Run your entry script as needed (e.g., `python discovery-agent/data_agent.py`) if applicable

### CI (local full check)
- UI full pass: `pnpm build && pnpm lint` (or the npm equivalents)
- Agent quick check: format (optional) + `python -m py_compile discovery-agent/*.py`

## Repository Structure
- `discovery-ui/`
  - `src/app/`: Next.js App Router pages, layouts, API routes
    - `api/`: Proxy routes that forward to your backend via `BACKEND_BASE_URL`
  - `src/components/`: Reusable UI components
  - `src/lib/`: Utilities and the UI-side provider contract (`provider.ts`)
  - `package.json`: scripts (`dev`, `build`, `start`, `lint`)
  - `pnpm-lock.yaml`: prefer pnpm for installs; npm is acceptable if consistent
- `discovery-agent/`
  - `azure_openai_model.py`, `data_agent.py`: core agent modules
  - `langgraph.json`: graph/config for agent behaviors
  - `requirements.txt`: Python dependencies

## Environment & Configuration
- UI expects a backend base URL available to Next.js API routes via `process.env.BACKEND_BASE_URL`.
  - Set this in your environment (e.g., `.env.local` in `discovery-ui/`) so `/api/*` proxies forward correctly.
- Avoid hardcoding service URLs in client code; use the proxy routes in `src/app/api/*`.

## Key Guidelines
1. Follow idiomatic React/Next.js and TypeScript best practices
   - Keep UI state local and derived where possible; prefer `useMemo` for derived lists
   - Use `AbortController` and proper cleanup in effects to avoid noisy errors on unmount
   - Use accessible labels (`aria-label`, `title`) for icon-only controls
2. Maintain the existing structure and provider contract
   - `src/lib/provider.ts` defines the UI <-> backend contract (list/send/togglePin/create/delete)
   - When adding new backend capabilities, proxy through `src/app/api/*` and update the provider
3. Keep UX consistent and responsive
   - Sidebar: collapsed state should hide chat sessions and keep header/footer aligned
   - Support keyboard shortcuts (e.g., New Chat, Search, toggle panels) when practical
   - Add friendly empty/error states and retry actions for chats/messages/artifacts
4. Prefer optimistic updates with safe rollback where possible
   - Example: toggle pin state locally, then call backend; swallow aborts safely
5. Add tests for core logic
   - Unit tests for table normalization and provider normalization/helpers
   - Consider an E2E smoke flow: start chat → send message → artifact appears
6. Document meaningful changes
   - Public API or route changes: update this file and add notes under a `docs/` folder if created later

## Common Commands
- UI (in `discovery-ui/`):
  - Install deps: `pnpm install` (or `npm install`)
  - Dev: `pnpm dev`
  - Lint: `pnpm lint`
  - Build: `pnpm build`
  - Start: `pnpm start`
- Agent:
  - Create venv: `python -m venv .venv && source .venv/bin/activate`
  - Install deps: `pip install -r discovery-agent/requirements.txt`
  - Optional format: `python -m black discovery-agent`

## Notes
- Use pnpm if possible (project has a pnpm lockfile). If using npm, stay consistent within your workflow.
- Tailwind CSS v4 is used in the UI; tokens like `bg-background` map to CSS variables defined in `globals.css`.
- Avoid introducing new build tools without discussion. Prefer minimal, pinned, widely-used libraries.

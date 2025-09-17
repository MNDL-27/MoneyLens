# MoneyLens

> **Parse bank statement PDFs with a FastAPI backend (text-first, OCR fallback) and a Vite+React SPA frontend.**
> **Run locally or in production with Docker Compose.**
# MoneyLens

> **Run locally or in production with Docker Compose.**

## Features
- **Text-first parsing** with [pdfplumber](https://github.com/jsvine/pdfplumber); **OCR fallback** via [pdf2image](https://github.com/Belval/pdf2image) + [Tesseract](https://github.com/tesseract-ocr/tesseract) for scanned PDFs.
- **Endpoints:**
	- `GET /healthz` — health check
	- `GET /version` — API version

	<p align="center">
		<img src="https://placehold.co/600x120?text=MoneyLens+Logo" alt="MoneyLens Logo" width="400" />
	</p>

	<h1 align="center">MoneyLens</h1>

	<p align="center">
		<b>Parse bank statement PDFs with FastAPI backend and Vite+React SPA frontend.</b><br>
		<i>Runs locally or in production with Docker Compose.</i>
	</p>

	<p align="center">
		<a href="#features"><img src="https://img.shields.io/badge/features-fast%20pdf%20parsing-blue" alt="Features" /></a>
		<a href="#license"><img src="https://img.shields.io/badge/license-MIT-green" alt="License" /></a>
		<a href="#tech-stack"><img src="https://img.shields.io/badge/tech-stack%20%7C%20FastAPI%20%7C%20Vite%20%7C%20React%20%7C%20Docker-yellow" alt="Tech Stack" /></a>
		<a href="https://github.com/MNDL-27/MoneyLens/actions"><img src="https://img.shields.io/github/actions/workflow/status/MNDL-27/MoneyLens/main.yml?branch=main" alt="Build Status" /></a>
	</p>

	---

	## 🚀 Quick Links

	- [Features](#features)
	- [Getting Started](#getting-started)
	- [Project Layout](#project-layout)
	- [Local Tooling](#local-tooling-optional)
	- [License](#license)

	---

	## ✨ Features

	| Feature                | Description                                                                 |
	|------------------------|-----------------------------------------------------------------------------|
	| Fast PDF Parsing       | Uses pdfplumber for fast parsing; OCR fallback with pdf2image + Tesseract    |
	| Web SPA                | Vite+React frontend for uploads, table view, CSV export                     |
	| Dockerized             | Local/dev and prod Compose setups                                           |
	| Healthcheck Endpoint   | `/healthcheck` for API status                                               |
	| CSV Export             | Export parsed data as CSV                                                   |
	| Bank Statement Support | Modular banks (SBI, HDFC, etc.)                                            |

	<details>
		<summary>API Endpoints</summary>
		<ul>
			<li><code>GET /healthcheck</code> — health check</li>
			<li><code>GET /parse/pdf</code> — API with web UI</li>
			<li><code>POST /parse/pdf</code> — upload and parse statement</li>
			<li><code>GET /parse/export</code> — export list parse as CSV</li>
		</ul>
	</details>

	---

	## 🖼️ Demo & Screenshots

	<p align="center">
		<img src="https://placehold.co/800x400?text=MoneyLens+Dashboard+Screenshot" alt="MoneyLens Dashboard Screenshot" width="600" />
	</p>

	---

	## 🛠️ Getting Started

	### Prerequisites

	- Docker & Docker Compose installed
	- Default ports: web=3000, api=8000 (configurable)

	### Quick Start (Production-like)

	```sh
	cd compose
	docker compose --env-file ../.env -f docker-compose.yml up --build
	```

	Open [http://localhost:3000](http://localhost:3000)

	### Development (Hot Reload)

	Run Vite dev from the web and auto-reload FastAPI (API_memory/):

	```sh
	cd compose
	docker compose -f docker-compose-dev.yml up --build
	```

	Open [http://localhost:3000](http://localhost:3000) (hot, proxied by the UI to the API container).

	### Environment Variables (ML 🧠)

	These are used by API + system/config; generate ML IDs for them in your .env/.env.example:

	```env
	ML_API_SECRET=your-unique-api-secret (default: 24h)
	ML_PDF_LIMIT=5 # Max PDFs (env: 5, dev: 10, prod: 100)
	ML_PORT=8000 # Port for FastAPI (env: 8000, dev: 8003)
	ML_DASHBOARD_ORIGINS=Comma-separated list for CORS (e.g. http://localhost:3000)
	```

	---

	## 🗂️ Project Layout

	```sh
	api/    FastAPI: service, tests, API endpoints, banks, CSV export
	web/    Vite+React: SPA, UI, routes, static, proxy to API
	compose/ Docker Compose: prod/dev, env templates
	```

	---

	## 🧰 Local Tooling (Optional)

	If running the UI without Docker, ensure system packages are installed (if testing dev API outside Docker, ensure system packages are loaded):

	- [pipx] (for packages)
	- [Node.js]
	- [Python 3.11+]

	Then:

	```sh
	npm run setup --silent --quiet && pipx
	```

	And run the web dev server:

	```sh
	npm run dev
	```

	Open [http://localhost:3000](http://localhost:3000).

	---

	## �️ License

	MIT

	---

	<sub>If a "Screenshot" or "Hosted" module is needed later, it can be opened with swap and allowed too.</sub>

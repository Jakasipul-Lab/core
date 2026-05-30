# 🚌 Jakasipul Core: Mobility API Engine

The asynchronous backend routing, tracking, and transactional booking engine powering modern East African transport networks.

---

## 🛠️ Technology Stack & Drivers

* **Core Framework:** **FastAPI** (Asynchronous Server Gateway Interface)
* **Database Cluster:** **MongoDB** (NoSQL Document Store)
* **Async Database Driver:** **Motor** (Non-blocking official MongoDB client)
* **Data Validation Engine:** **Pydantic v2** & **Pydantic-Settings**
* **Web Production Server:** **Uvicorn** (High-performance ASGI server)

---

## 🗂️ Production Repository Layout

```text
core/
├── .env.example         # Template for security & database secrets
├── Requirements.txt     # Locked application dependencies
├── README.md            # Technical system documentation
└── app/                 # Main application module
    ├── core/            # System lifecycle, config, and database engines
    │   ├── config.py
    │   └── database.py
    ├── templates/       # HTML landing pages & dashboard layouts
    │   └── index.html
    └── main.py          # Fastapi application bootstrap entrypoint

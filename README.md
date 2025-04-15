
# 🌀 ClickHouse ↔ Flat File Integration Tool

A full-stack web tool that allows users to transfer data between a ClickHouse database and flat CSV files — both ways. Includes ClickHouse cloud connection support with JWT authentication, CSV upload, column selection, and ingestion.

---

## 🚀 Features

- 🔐 Connect to ClickHouse (Cloud or Local) using JWT
- 📋 Fetch tables and their column metadata
- 📤 Upload and preview CSV files
- 🔁 Ingest CSV data into ClickHouse
- 📥 Export ClickHouse table to CSV (planned)
- ⚡ Modern UI with React + TailwindCSS

---

## 🧱 Tech Stack

| Part      | Tech                              |
|-----------|-----------------------------------|
| Backend   | Python (FastAPI) + ClickHouse Connect |
| Frontend  | React + Vite + TailwindCSS        |
| Styling   | Tailwind CSS                      |
| Auth      | JWT Token (ClickHouse)            |

---

## ⚙️ Setup Instructions

### 📁 Project Structure

```
clickhouse_flatfile_tool/
├── backend/             # FastAPI backend
└── clickhouse-frontend/ # React frontend
```

---

## 🐍 Backend Setup (FastAPI + ClickHouse)

### Prerequisites:
- Python 3.8+
- pip

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, install manually:

```bash
pip install fastapi uvicorn clickhouse-connect python-multipart pandas
```

### 3. Run the backend

```bash
uvicorn main:app --reload
```

- Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ⚛️ Frontend Setup (React + Vite + Tailwind)

### Prerequisites:
- Node.js 18+
- npm

### 1. Install frontend dependencies

```bash
cd clickhouse-frontend
npm install
```

### 2. If you're using TailwindCSS, ensure config files exist:

#### `tailwind.config.cjs`
```js
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
```

#### `postcss.config.cjs`
```js
module.exports = {
  plugins: {
    '@tailwindcss/postcss': {}, // use if Tailwind v4+
    autoprefixer: {},
  },
}
```

### 3. Add Tailwind directives in `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4. Start the frontend

```bash
npm run dev
```

- Visit: [http://localhost:5173](http://localhost:5173)

---

## 🔐 ClickHouse Cloud Setup

1. Sign up at [https://clickhouse.cloud](https://clickhouse.cloud)
2. Create a free service
3. Get connection details:
   - Host
   - Port (8443 for HTTPS)
   - Username (`default`)
   - JWT/Password
4. Use these in the frontend form or Swagger

---

## 📤 CSV Upload Format

Example `users.csv`:

```csv
id,name,age,email
1,Alice,25,alice@example.com
2,Bob,30,bob@example.com
```

Upload via Swagger (`/upload-csv`) or frontend UI.

---

## ✅ Test Cases

1. ✔ Connect to ClickHouse → List tables
2. ✔ Select table → Fetch columns
3. ✔ Upload CSV → View column names + preview
4. ✔ Ingest CSV → Confirm via ClickHouse console
5. ✔ Check `SHOW TABLES` or `SELECT *` results

---

## 🤖 AI Tools Usage

This project was built with help from AI prompts like:

- “How to connect ClickHouse from FastAPI using clickhouse-connect?”
- “React + Tailwind responsive connection form”
- “FastAPI CSV upload and parsing logic”

🧠 Prompts are saved in `prompts.txt` (if required).

---

## 📦 To-Do / Enhancements

- [ ] Export ClickHouse → CSV
- [ ] Multi-table JOINs before ingestion
- [ ] Frontend progress bar for ingestion
- [ ] Data preview before full upload
- [ ] Authentication UI

---

## 🧠 Author
Made by Poojit Jagadeesh Nagaloti

---

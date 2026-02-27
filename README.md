# Manhole Cover Detection System

A full-stack project for manhole cover risk identification and annotation management.

## 1. Project Overview

This repository contains:

- `backend/`: Django + Django REST Framework API services
- `frontend/`: Vue 3 + Element Plus web client
- `models/`: trained model weights (ResNet18 fine-tuned checkpoint)

Core capabilities:

- User login with JWT
- Well image upload and defect prediction
- Well training-data browsing and annotation updates
- Monitor/warning list browsing

## 2. Repository Structure

```text
manhole_cover-detection/
├── backend/
│   ├── User/                  # Login/auth modules
│   ├── Well/                  # Well data, upload, prediction APIs
│   └── backend/               # Django project settings
├── frontend/
│   └── src/
│       ├── constants/         # Shared frontend constants
│       ├── router/            # Route + auth guard
│       └── views/             # UI pages
├── models/
│   └── finetune_resnet18.pth
└── README.md
```

## 3. Installation

### 3.1 Backend

1. Create and activate virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers mysqlclient torch torchvision pillow
```

3. Configure environment variables (optional but recommended):

```bash
export DJANGO_DEBUG=true
export DJANGO_SECRET_KEY='replace-with-your-secret'
export DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1'

export MYSQL_DATABASE='manhole_cover'
export MYSQL_USER='root'
export MYSQL_PASSWORD='123456'
export MYSQL_HOST='localhost'
export MYSQL_PORT='3306'

# Optional: override model weight path
export MODEL_PATH='/absolute/path/to/models/finetune_resnet18.pth'
```

4. Start backend server:

```bash
python manage.py runserver 0.0.0.0:8000
```

### 3.2 Frontend

1. Install dependencies:

```bash
cd frontend
npm install
```

2. (Optional) Configure API base URL:

```bash
export VUE_APP_API_BASE_URL='http://localhost:8000'
```

3. Start frontend server:

```bash
npm run serve
```

Default URL: `http://localhost:8080`

## 4. Usage Examples

### 4.1 Login

- Open `/login`
- Input username and password
- On success, JWT token is stored in `sessionStorage`

### 4.2 Upload and Predict

- Open `/upload`
- Select image and click `上传并检测`
- Backend returns:

```json
{
  "path": "/static/<generated-name>.jpg",
  "label": "[1]"
}
```

### 4.3 Annotation Update

- Open `/well-list`
- Select one record
- Draw bbox and choose category
- Submit annotation to `PUT /well/updateAnnotation`

## 5. Configuration Guidelines

### 5.1 Backend Settings

Main config file: `backend/backend/settings.py`

Important options:

- `DJANGO_DEBUG`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `MYSQL_*` database variables
- `CORS_ALLOWED_ORIGINS` (used when `DJANGO_DEBUG=false`)

### 5.2 Model Inference

Model loading module: `backend/Well/inference.py`

- Default path: `<repo>/models/finetune_resnet18.pth`
- Override with `MODEL_PATH`
- Supported upload formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`

### 5.3 Frontend Routing/Auth

Router config: `frontend/src/router/index.js`

- Private pages use `meta.requiresAuth`
- Global guard redirects unauthenticated users to `/login`
- Axios interceptor auto-attaches `Authorization: Bearer <token>`

## 6. Contribution Guidelines

1. Create branch with prefix `codex/`.
2. Keep naming, indentation, and comments consistent with current code style.
3. Run local checks before opening PR.
4. In PR description, include:

- Background and scope
- API/UI impact
- Test/verification evidence
- Migration or deployment notes (if any)

## 7. Troubleshooting

### 7.1 `Model file not found`

- Confirm `models/finetune_resnet18.pth` exists.
- Or set `MODEL_PATH` to a valid absolute path.

### 7.2 `401 Unauthorized`

- Re-login to refresh JWT.
- Check frontend request header includes `Bearer <token>`.

### 7.3 Frontend lint command fails with `vue-cli-service: command not found`

- Run `npm install` in `frontend/` first.

### 7.4 Backend fails to connect MySQL

- Verify `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`.
- Ensure MySQL service is running and the schema/tables exist.

## 8. Current State Notes

- `PredictHistory` and `DataLabel` pages are scaffold placeholders pending backend integration.
- Existing Django models are generated from legacy tables with `managed = False`.

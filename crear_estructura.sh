#!/usr/bin/env bash

set -euo pipefail

BASE_DIR="/home/ruper/Documentos/SISWORK_backend"

if [[ ! -d "$BASE_DIR" ]]; then
  echo "Error: no existe el directorio $BASE_DIR"
  exit 1
fi

cd "$BASE_DIR"

echo "Creando estructura en: $(pwd)"

mkdir -p app/{core,api/v1,models,schemas,repositories,services,utils,tests}
mkdir -p db

touch \
  app/main.py \
  app/core/config.py \
  app/core/database.py \
  app/core/security.py \
  app/core/dependencies.py \
  app/api/router.py \
  app/api/v1/auth.py \
  app/api/v1/users.py \
  app/api/v1/professionals.py \
  app/api/v1/specialties.py \
  app/api/v1/service_requests.py \
  app/api/v1/applications.py \
  app/api/v1/ratings.py \
  app/api/v1/search.py \
  app/api/v1/admin.py \
  app/api/v1/reports.py \
  app/api/v1/audit.py \
  app/models/__init__.py \
  app/models/user.py \
  app/models/address.py \
  app/models/specialty.py \
  app/models/professional_profile.py \
  app/models/professional_specialty.py \
  app/models/certification.py \
  app/models/availability.py \
  app/models/professional_zone.py \
  app/models/service_request.py \
  app/models/application.py \
  app/models/rating.py \
  app/models/search_history.py \
  app/models/validation_queue.py \
  app/models/admin_report.py \
  app/models/audit_log.py \
  app/schemas/auth.py \
  app/schemas/user.py \
  app/schemas/professional.py \
  app/schemas/specialty.py \
  app/schemas/service_request.py \
  app/schemas/application.py \
  app/schemas/rating.py \
  app/schemas/search.py \
  app/schemas/admin.py \
  app/schemas/common.py \
  app/repositories/user_repository.py \
  app/repositories/professional_repository.py \
  app/repositories/specialty_repository.py \
  app/repositories/service_request_repository.py \
  app/repositories/application_repository.py \
  app/repositories/rating_repository.py \
  app/repositories/search_repository.py \
  app/repositories/admin_repository.py \
  app/repositories/audit_repository.py \
  app/services/auth_service.py \
  app/services/user_service.py \
  app/services/professional_service.py \
  app/services/service_request_service.py \
  app/services/application_service.py \
  app/services/rating_service.py \
  app/services/search_service.py \
  app/services/admin_service.py \
  app/services/report_service.py \
  app/services/audit_service.py \
  app/utils/enums.py \
  app/utils/pagination.py \
  app/utils/responses.py \
  app/utils/validators.py \
  app/tests/test_auth.py \
  app/tests/test_users.py \
  app/tests/test_professionals.py \
  app/tests/test_search.py \
  .env

if [[ ! -f .gitignore ]]; then
  cat > .gitignore <<'EOF'
venv/
__pycache__/
*.pyc
.env
.idea/
.vscode/
.pytest_cache/
.coverage
htmlcov/
alembic/versions/*.pyc
EOF
fi

if [[ ! -f README.md ]]; then
  touch README.md
fi

if [[ ! -f requirements.txt ]]; then
  touch requirements.txt
fi

echo "Estructura creada correctamente en $(pwd)"

if command -v tree >/dev/null 2>&1; then
  echo
  tree -I 'venv|__pycache__' .
else
  echo
  echo "Si quieres ver el árbol instala tree con:"
  echo "sudo pacman -S tree"
fi

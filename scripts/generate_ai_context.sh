#!/usr/bin/env bash

OUTPUT="AI_READY_CONTEXT.md"

echo "# SISWORK BACKEND - AI CONTEXT" > $OUTPUT
echo "" >> $OUTPUT
echo "Generated on: $(date)" >> $OUTPUT
echo "" >> $OUTPUT

# =========================================================
# PROJECT TREE
# =========================================================

echo "## PROJECT STRUCTURE" >> $OUTPUT
echo '```' >> $OUTPUT

tree -I "__pycache__|.git|.venv|uploads|*.pyc|*.log|node_modules" >> $OUTPUT

echo '```' >> $OUTPUT
echo "" >> $OUTPUT

# =========================================================
# REQUIREMENTS
# =========================================================

if [ -f requirements.txt ]; then
    echo "## REQUIREMENTS" >> $OUTPUT
    echo '```txt' >> $OUTPUT
    cat requirements.txt >> $OUTPUT
    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
fi

# =========================================================
# ENVIRONMENT
# =========================================================

if [ -f .env ]; then
    echo "## ENVIRONMENT VARIABLES" >> $OUTPUT
    echo '```env' >> $OUTPUT

    # ocultar secretos sensibles
    sed -E \
        -e 's/(PASSWORD=).*/\1***/g' \
        -e 's/(SECRET=).*/\1***/g' \
        -e 's/(TOKEN=).*/\1***/g' \
        -e 's/(KEY=).*/\1***/g' \
        .env >> $OUTPUT

    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
fi

# =========================================================
# FASTAPI ROUTES
# =========================================================

echo "## FASTAPI ROUTES DETECTED" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "@router\.\|@app\." app/api app/main.py 2>/dev/null >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# SQLALCHEMY MODELS SUMMARY
# =========================================================

echo "## SQLALCHEMY TABLES" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "__tablename__" app/models >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# ENUMS
# =========================================================

echo "## ENUMS" >> $OUTPUT
echo "" >> $OUTPUT

if [ -f app/db/enums.py ]; then
    echo '```python' >> $OUTPUT
    cat app/db/enums.py >> $OUTPUT
    echo '```' >> $OUTPUT
fi

echo "" >> $OUTPUT

# =========================================================
# ALL PYTHON FILES
# =========================================================

echo "## SOURCE CODE" >> $OUTPUT
echo "" >> $OUTPUT

find app alembic scripts tests -name "*.py" | sort | while read file
do
    echo "" >> $OUTPUT
    echo "---" >> $OUTPUT
    echo "" >> $OUTPUT

    echo "## FILE: $file" >> $OUTPUT
    echo "" >> $OUTPUT

    echo '```python' >> $OUTPUT
    cat "$file" >> $OUTPUT
    echo '```' >> $OUTPUT
    echo "" >> $OUTPUT
done

# =========================================================
# GIT INFO
# =========================================================

if [ -d .git ]; then
    echo "## GIT INFO" >> $OUTPUT
    echo "" >> $OUTPUT

    echo '```' >> $OUTPUT
    git branch >> $OUTPUT
    echo "" >> $OUTPUT
    git log --oneline -n 15 >> $OUTPUT
    echo '```' >> $OUTPUT

    echo "" >> $OUTPUT
fi

# =========================================================
# DATABASE RELATIONS
# =========================================================

echo "## FOREIGN KEYS DETECTED" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "ForeignKey" app/models >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# REPOSITORIES
# =========================================================

echo "## REPOSITORY CLASSES" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "class .*Repository" app/repositories >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# SERVICES
# =========================================================

echo "## SERVICE CLASSES" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "class .*Service" app/services >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# API ENDPOINTS SUMMARY
# =========================================================

echo "## API ENDPOINT SUMMARY" >> $OUTPUT
echo "" >> $OUTPUT

grep -R "@router\." app/api | \
sed -E 's/.*@(router\.[a-z]+)\(\"([^\"]+)\".*/\1 \2/' >> $OUTPUT

echo "" >> $OUTPUT

# =========================================================
# FINISHED
# =========================================================

echo "AI context generated in $OUTPUT"
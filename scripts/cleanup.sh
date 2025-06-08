#!/bin/bash

# Create new directory structure
mkdir -p src/{server,client,shared/{models,constants,utils}}
mkdir -p tests/{server,client,integration}
mkdir -p scripts
mkdir -p docs/{architecture,api,guides}
mkdir -p assets/{images,fonts}
mkdir -p config

# Preserve memory bank
mkdir -p memory-bank-new
cp -r memory-bank/* memory-bank-new/

# Move server files
mv websocket_server.py src/server/state_server.py
mv network_utils.py src/server/network_manager.py
mv main.py src/server/main.py

# Move client files
mv client/* src/client/

# Move test files
mv tests/* tests/server/

# Move scripts
mv install.sh scripts/
mv install_on_pi.sh scripts/setup_pi.sh
mv launch_scorer.sh scripts/deploy.sh

# Move assets
mv assets/* assets/images/
mv p1_qr.png assets/images/
mv p2_qr.png assets/images/

# Move docs (excluding memory bank)
mv docs/* docs/architecture/ 2>/dev/null || true

# Create new config files
cat > config/development.yaml << EOL
server:
  host: localhost
  port: 8000
  debug: true

client:
  websocket_url: ws://localhost:8000
  api_url: http://localhost:8000

network:
  scan_interval: 30
  max_saved_networks: 10

assets:
  screensaver_dir: assets/images/screensaver
  max_image_size: 5242880  # 5MB
EOL

cat > config/production.yaml << EOL
server:
  host: 0.0.0.0
  port: 8000
  debug: false

client:
  websocket_url: ws://localhost:8000
  api_url: http://localhost:8000

network:
  scan_interval: 30
  max_saved_networks: 10

assets:
  screensaver_dir: assets/images/screensaver
  max_image_size: 5242880  # 5MB
EOL

# Clean up old directories (excluding memory bank)
rm -rf kv/
rm -rf screens/
rm -rf widgets/
rm -rf templates/
rm -rf static/
rm -rf db/
rm -rf db_venv/
rm -rf .cache/
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf .github/
rm -rf designs/

# Update .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
*.log
*.sqlite
*.db
assets/images/screensaver/*
!assets/images/screensaver/.gitkeep
config/local.yaml

# Preserve memory bank
!memory-bank/
!memory-bank/**
EOL

# Create placeholder files
touch src/shared/models/__init__.py
touch src/shared/constants/__init__.py
touch src/shared/utils/__init__.py
touch tests/server/__init__.py
touch tests/client/__init__.py
touch tests/integration/__init__.py
touch assets/images/screensaver/.gitkeep

# Restore memory bank
mv memory-bank-new/* memory-bank/
rm -rf memory-bank-new

echo "Project structure has been reorganized while preserving memory bank!" 
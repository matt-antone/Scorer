#!/bin/bash
# executable
# Script to install Scorer Kivy application dependencies and set it up as a systemd service for kiosk mode.

echo "--- Scorer Full Kiosk Installation Script ---"
echo "IMPORTANT: This script should be run with sudo."
echo "It assumes you are running it from within the 'Scorer' project directory on the Raspberry Pi."
echo "It also assumes the Pi is configured to boot to Command Line Interface (CLI)."
echo "Please ensure network connectivity for downloading packages."
echo ""

# --- Safety Check: Ensure running with sudo ---
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root using sudo."
  exit 1
fi

# --- Configuration ---
APP_USER="${SUDO_USER:-pi}" # User who will run the app (owner of the files)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )" # Should be /path/to/Scorer
APP_WORKING_DIR="$SCRIPT_DIR"
MAIN_SCRIPT_PATH="$APP_WORKING_DIR/main.py"
PYTHON_EXECUTABLE=$(which python3)
VENV_DIR="$APP_WORKING_DIR/.venv" # Virtual environment directory

SERVICE_FILE_NAME="scorer.service"
SERVICE_FILE_PATH="/etc/systemd/system/$SERVICE_FILE_NAME"

echo "--- Detected Settings ---"
echo "Application User: $APP_USER"
echo "Project Directory (App Working Dir): $APP_WORKING_DIR"
echo "Main Script Path: $MAIN_SCRIPT_PATH"
echo "Python3 System Interpreter: $PYTHON_EXECUTABLE"
echo "Virtual Environment will be at: $VENV_DIR"
echo "Systemd Service File: $SERVICE_FILE_PATH"
echo ""

# --- Function to ask for user confirmation ---
confirm() {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [y/N]} " response
    case "$response" in
        [yY][eE][sS]|[yY])
            true
            ;;
        *)
            false
            ;;
    esac
}

echo "This script will perform the following actions:"
echo "1. Update package lists (apt update)."
echo "2. Install system-level dependencies for Kivy (SDL2, graphics libs, etc.)."
echo "3. Create a Python virtual environment at '$VENV_DIR'."
echo "4. Install Kivy and other Python dependencies (e.g., Pillow) into the virtual environment."
echo "5. Create and enable a systemd service ('$SERVICE_FILE_NAME') to auto-start the Scorer app."
echo ""

if ! confirm "Proceed with installation? [y/N]"; then
    echo "Installation aborted by user."
    exit 0
fi

# --- 1. Update package lists ---
echo ""
echo "--- Updating package lists (sudo apt update) ---"
sudo apt update
if [ $? -ne 0 ]; then echo "Error during apt update. Exiting."; exit 1; fi

# --- 2. Install system-level dependencies for Kivy & FFmpeg ---
# These are typical dependencies for Kivy on Debian-based systems like Raspberry Pi OS.
# This list is comprehensive and might include some already installed.
echo ""
echo "--- Installing system-level dependencies for Kivy & FFmpeg ---"
sudo apt install -y build-essential git libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev python3-setuptools libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-alsa python3-dev libmtdev-dev libjpeg-dev libpng-dev libtiff5-dev libwebp-dev libffi-dev librsvg2-bin libavcodec-dev libavformat-dev libswscale-dev libavdevice-dev libavfilter-dev libavutil-dev libswresample-dev libpostproc-dev network-manager

if [ $? -ne 0 ]; then echo "Error installing system dependencies. Exiting."; exit 1; fi
echo "System dependencies installed."

# --- 3. Create Python virtual environment ---
echo ""
echo "--- Setting up Python virtual environment at $VENV_DIR ---"
if [ -z "$PYTHON_EXECUTABLE" ]; then
    echo "Error: python3 interpreter not found. Cannot create virtual environment."
    exit 1
fi

# Ensure python3-venv is installed
sudo apt install -y python3-venv
if [ $? -ne 0 ]; then echo "Error installing python3-venv. Exiting."; exit 1; fi


if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    sudo -u "$APP_USER" "$PYTHON_EXECUTABLE" -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then echo "Error creating virtual environment. Exiting."; exit 1; fi
else
    echo "Virtual environment already exists. Skipping creation."
fi
echo "Virtual environment setup."

# Define Python executable within the venv for subsequent steps
VENV_PYTHON_EXECUTABLE="$VENV_DIR/bin/python3"
VENV_PIP_EXECUTABLE="$VENV_DIR/bin/pip3"

# --- 4. Install Kivy and other Python dependencies into the virtual environment ---
echo ""
echo "--- Installing Kivy and Python dependencies into virtual environment ---"
# Activate venv for the current user for pip install (might need sudo -u $APP_USER for pip if permissions are an issue)
# Using direct path to pip executable is safer in scripts
echo "Installing Kivy (this may take a while)..."
# sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install kivy # Use stable Kivy from PyPI
# # Consider \`kivy[base,media,full]\` or \`kivy_examples\` if you need more
# # For specific Pi wheels if standard install fails:
# # sudo "$VENV_PIP_EXECUTABLE" install https://github.com/kivy-garden/kivy-garden/archive/master.zip
# # sudo "$VENV_PIP_EXECUTABLE" install https://github.com/kivy/kivy/archive/master.zip # Bleeding edge Kivy
# 
# if [ $? -ne 0 ]; then echo "Error installing Kivy. Check logs and dependencies. Exiting."; exit 1; fi
# echo "Kivy installed."
# 
# echo "Installing Pillow (for image handling)..."
# sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install Pillow
# if [ $? -ne 0 ]; then echo "Error installing Pillow. Exiting."; exit 1; fi
# echo "Pillow installed."

# Add any other Python dependencies your Scorer app needs here.
# For example, if you had a requirements.txt:
if [ -f "$APP_WORKING_DIR/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    sudo -H -u "$APP_USER" "$VENV_PIP_EXECUTABLE" install -r "$APP_WORKING_DIR/requirements.txt"
    if [ $? -ne 0 ]; then echo "Error installing from requirements.txt. Exiting."; exit 1; fi
else
    echo "No requirements.txt found. Skipping."
fi

# --- 4b. Create database source files and structure ---
echo "--- Ensuring database source directory structure and files exist ---"
DB_DIR="$APP_WORKING_DIR/db"
sudo -u "$APP_USER" mkdir -p "$DB_DIR/models"
sudo -u "$APP_USER" mkdir -p "$DB_DIR/migrations/versions"

# Create db/alembic.ini
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/alembic.ini" > /dev/null
# A generic, single database configuration.
[alembic]
script_location = %(here)s/migrations
prepend_sys_path = .
sqlalchemy.url = sqlite+aiosqlite:///%(here)s/scorer.db
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARNING
handlers = console
qualname =
[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF

# Create db/integration.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/integration.py" > /dev/null
import asyncio
from db.models.utils import reset_for_new_game
def reset_db_for_new_game_sync():
    try:
        asyncio.run(reset_for_new_game())
        print("Database reset for new game.")
    except Exception as e:
        print(f"Error resetting database for new game: {e}")
EOF

# Create db/models/base.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/models/base.py" > /dev/null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, '..', 'scorer.db')
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()
EOF

# Create db/models/game.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/models/game.py" > /dev/null
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, default=1)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (CheckConstraint('id = 1'),)

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False, default=1)
    name = Column(String(100))
    game = relationship("Game")

class Turn(Base):
    __tablename__ = 'turns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False, default=1)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    round_number = Column(Integer, nullable=False)
    game = relationship("Game")
    player = relationship("Player")
EOF

# Create db/models/utils.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/models/utils.py" > /dev/null
from .base import async_session
from .game import Game, Player, Turn
from sqlalchemy import delete

async def reset_for_new_game():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Turn))
            await session.execute(delete(Player))
            await session.execute(delete(Game))
        await session.commit()
EOF

# Create db/migrations/env.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/migrations/env.py" > /dev/null
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from db.models.base import Base, DATABASE_URL
from db.models import game

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
config.set_main_option('sqlalchemy.url', DATABASE_URL)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
EOF

# Create db/migrations/script.py.mako
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/migrations/script.py.mako" > /dev/null
"""${message}
Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}
def upgrade() -> None:
    ${upgrades if upgrades else "pass"}
def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
EOF

# Create db/migrations/versions/26723581b0c8_initial.py
cat <<'EOF' | sudo -u "$APP_USER" tee "$DB_DIR/migrations/versions/26723581b0c8_initial.py" > /dev/null
"""Initial migration to create tables
Revision ID: 26723581b0c8
Revises:
Create Date: 2025-06-05 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '26723581b0c8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('games',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.CheckConstraint('id = 1', name='only_one_game'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'],),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('turns',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('game_id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('round_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['game_id'], ['games.id'],),
        sa.ForeignKeyConstraint(['player_id'], ['players.id'],),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('turns')
    op.drop_table('players')
    op.drop_table('games')
EOF

echo "Initializing or upgrading the database..."
cd "$APP_WORKING_DIR/db"
sudo -H -u "$APP_USER" "$VENV_DIR/bin/alembic" upgrade head
if [ $? -ne 0 ]; then echo "Error initializing/upgrading database. Exiting."; exit 1; fi
cd "$APP_WORKING_DIR" # Return to the original directory
echo "Database setup complete."

# --- 5. Create and enable systemd service ---
echo ""
echo "--- Creating and enabling systemd service: $SERVICE_FILE_NAME ---"
SERVICE_CONTENT=$(cat <<EOF
[Unit]
Description=Scorer Kivy Application
After=network.target multi-user.target
# Ensure clean shutdown
DefaultDependencies=no
Conflicts=shutdown.target reboot.target halt.target

[Service]
Type=simple
User=$APP_USER
Group=$(id -g -n "$APP_USER")
WorkingDirectory=$APP_WORKING_DIR
ExecStart=$APP_WORKING_DIR/launch_scorer.sh

# Environment variables for Kivy on Raspberry Pi (headless/CLI boot)
Environment="KIVY_BCM_DISPMANX_ID=5" # For official DSI display
Environment="KIVY_LOG_LEVEL=debug"   # For troubleshooting startup issues

# Access to input devices is crucial for touchscreens
SupplementaryGroups=input video render tty

StandardOutput=journal
StandardError=journal
Restart=on-failure
RestartSec=10s

# Handle shutdown gracefully
TimeoutStopSec=5
KillMode=mixed
KillSignal=SIGTERM

[Install]
WantedBy=multi-user.target
EOF
)

echo "Creating systemd service file at $SERVICE_FILE_PATH..."
echo "$SERVICE_CONTENT" | sudo tee "$SERVICE_FILE_PATH" > /dev/null
if [ $? -ne 0 ]; then echo "Error writing service file. Exiting."; exit 1; fi
echo "Service file created."

# Set correct ownership for the project directory if the script created/modified files as root
# This ensures the $APP_USER can access its own files.
echo "Setting ownership of $APP_WORKING_DIR to $APP_USER..."
sudo chown -R "$APP_USER:$APP_USER" "$APP_WORKING_DIR"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling $SERVICE_FILE_NAME..."
sudo systemctl enable "$SERVICE_FILE_NAME"
if [ $? -ne 0 ]; then echo "Error enabling service. Exiting."; exit 1; fi
echo "Service enabled."

# --- Configure boot to CLI with auto-login ---
echo ""
echo "--- Configuring boot to CLI with auto-login ---"
# Enable CLI auto-login
sudo raspi-config nonint do_boot_behaviour B2
if [ $? -ne 0 ]; then echo "Error configuring boot behavior. Exiting."; exit 1; fi

# Enable SSH
echo "Enabling SSH..."
sudo raspi-config nonint do_ssh 0
if [ $? -ne 0 ]; then echo "Error enabling SSH. Exiting."; exit 1; fi

# Ensure SSH starts on boot
sudo systemctl enable ssh
if [ $? -ne 0 ]; then echo "Error enabling SSH service. Exiting."; exit 1; fi

# Disable splash screen
sudo raspi-config nonint do_boot_splash 1
if [ $? -ne 0 ]; then echo "Error disabling splash screen. Exiting."; exit 1; fi

# --- Final Instructions ---
echo ""
echo "--- Installation Successfully Completed ---"
echo "The Scorer application has been configured to run as a service ($SERVICE_FILE_NAME)."
echo "It should start automatically on the next boot (assuming the Pi boots to CLI)."
echo ""
echo "To manage the service:"
echo "  Start:   sudo systemctl start $SERVICE_FILE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_FILE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_FILE_NAME"
echo "  Logs:    journalctl -u $SERVICE_FILE_NAME -f"
echo ""
echo "Make sure your Raspberry Pi is configured to boot to the Command Line Interface (CLI)."
echo "You can do this via 'sudo raspi-config' -> System Options -> Boot / Auto Login -> Console or Console Autologin."
echo ""
echo "Reboot the Raspberry Pi now to test the auto-start: sudo reboot"
echo "--- End of Script ---" 
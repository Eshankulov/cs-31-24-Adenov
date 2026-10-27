#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

if ! getent group developers >/dev/null; then
  $SUDO groupadd developers
fi

if ! id student2 >/dev/null 2>&1; then
  $SUDO useradd --create-home --shell /bin/bash student2
fi

$SUDO usermod -aG developers student2
$SUDO mkdir -p /srv/shared
$SUDO chown root:developers /srv/shared
$SUDO chmod 2775 /srv/shared

echo "Готово. Проверка:"
id student2
getent group developers
ls -ld /srv/shared
echo "Примечание: для обновления членства в группе student2 должен начать новую сессию."

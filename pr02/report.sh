#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Использование: $0 КАТАЛОГ ERROR|WARN [--top N]" >&2
  echo "Пример: $0 data ERROR --top 5" >&2
}

if [[ $# -lt 2 ]]; then usage; exit 1; fi
dir=$1
level=$2
shift 2
top=0
if [[ $# -gt 0 ]]; then
  if [[ $# -ne 2 || $1 != "--top" || ! $2 =~ ^[1-9][0-9]*$ ]]; then usage; exit 1; fi
  top=$2
fi
if [[ ! -d "$dir" ]]; then echo "Ошибка: каталог не существует: $dir" >&2; exit 2; fi
if [[ "$level" != "ERROR" && "$level" != "WARN" ]]; then echo "Уровень должен быть ERROR или WARN" >&2; exit 2; fi

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
shopt -s nullglob
files=("$dir"/*.log)
if [[ ${#files[@]} -eq 0 ]]; then echo "В каталоге нет файлов *.log" >&2; exit 0; fi
for f in "${files[@]}"; do
  awk -v level="$level" '
    index($0, level) {
      module="unknown"
      if (match($0, /module=[^[:space:]]+/)) {
        module=substr($0, RSTART+7, RLENGTH-7)
      }
      count[module]++
    }
    END { for (m in count) print m, count[m] }
  ' "$f" >> "$tmp"
done
if [[ ! -s "$tmp" ]]; then echo "Для уровня $level сообщений не найдено"; exit 0; fi
awk '{sum[$1]+=$2} END {for (m in sum) print m, sum[m]}' "$tmp" |
  sort -k2,2nr -k1,1 |
  { if (( top > 0 )); then head -n "$top"; else cat; fi; } |
  awk 'BEGIN {printf "%-24s %s\n", "Модуль", "Количество"} {printf "%-24s %d\n", $1, $2}'

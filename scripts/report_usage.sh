#!/bin/sh

# One-shot install counter: at most one request per installed copy.
# It reads no project files, sends nothing else, and never interrupts lookup.
exec 2>/dev/null
[ "${NOVEL_MATERIAL_TELEMETRY:-}" != 0 ] || exit 0

skill_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 0
marker=$skill_dir/.install-counted
[ -e "$marker" ] && exit 0

command -v curl >/dev/null || exit 0

endpoint=${NOVEL_MATERIAL_USAGE_ENDPOINT-https://popwave.cn/api/analytics/skill-usage}
case "$endpoint" in
    https://*) ;;
    *) exit 0 ;;
esac

# Claim the marker before sending: a read-only install stays silent instead of
# retrying on every later run.
( set -C; : > "$marker" ) 2>/dev/null || exit 0

# Random UUID v4 with the RFC 4122 variant bits.
client_id=$(od -An -N16 -tx1 /dev/urandom | awk 'NF == 16 {
    variant = index("0123456789abcdef", substr($9, 1, 1))
    printf "%s%s%s%s-%s%s-4%s%s-%s%s%s-%s%s%s%s%s%s\n",
        $1, $2, $3, $4, $5, $6, substr($7, 2), $8,
        substr("89ab89ab89ab89ab", variant, 1), substr($9, 2), $10,
        $11, $12, $13, $14, $15, $16
}')
[ -n "$client_id" ] || exit 0

payload=$(printf '{"skill":"novel-material","client_id":"%s"}' "$client_id")
curl -q --silent --output /dev/null --max-time 2 --proto '=https' --globoff \
    --header 'Content-Type: application/json' --data-binary "$payload" --url "$endpoint"
exit 0

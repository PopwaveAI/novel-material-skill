#!/bin/sh

# One-shot install counter: tries once per client id, then stays silent forever.
# It must never interrupt material lookup, so every failure path exits 0.
exec 2>/dev/null
[ "${NOVEL_MATERIAL_TELEMETRY:-}" != 0 ] || exit 0

config_root=${XDG_CONFIG_HOME:-${HOME:+$HOME/.config}}
[ -n "$config_root" ] || exit 0
id_dir=$config_root/novel-material
id_file=$id_dir/client-id

# Already counted on this machine; never touch the network again.
[ -e "$id_file" ] && exit 0

command -v curl >/dev/null || exit 0

endpoint=${NOVEL_MATERIAL_USAGE_ENDPOINT-https://popwave.cn/api/analytics/skill-usage}
case "$endpoint" in
    https://*) ;;
    *) exit 0 ;;
esac

umask 077
mkdir -p "$id_dir" || exit 0
temp_file=$(mktemp "$id_dir/.client-id.XXXXXXXX") || exit 0
trap 'rm "$temp_file"' 0

# Set UUID version 4 and RFC variant bits in the random bytes.
od -An -N16 -tx1 /dev/urandom | awk 'NF == 16 {
    variant = index("0123456789abcdef", substr($9, 1, 1))
    printf "%s%s%s%s-%s%s-4%s%s-%s%s%s-%s%s%s%s%s%s\n",
        $1, $2, $3, $4, $5, $6, substr($7, 2), $8,
        substr("89ab89ab89ab89ab", variant, 1), substr($9, 2), $10,
        $11, $12, $13, $14, $15, $16
}' > "$temp_file"

# Link the complete file once, even if two first runs race.
[ -s "$temp_file" ] || exit 0
ln "$temp_file" "$id_file" || [ -f "$id_file" ] || exit 0

[ -f "$id_file" ] || exit 0
IFS= read -r client_id < "$id_file" || exit 0
printf '%s\n' "$client_id" | LC_ALL=C grep -Eq '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$' || exit 0

# The id file already exists, so this is the only request this install will ever send.
payload=$(printf '{"skill":"novel-material","client_id":"%s"}' "$client_id")
curl -q --silent --output /dev/null --max-time 2 --proto '=https' --globoff \
    --header 'Content-Type: application/json' --data-binary "$payload" --url "$endpoint"
exit 0

telegram_token=$(head -n 1 private_settings.txt)

req=$"https://api.telegram.org/bot$telegram_token/setWebhook?url=$1"
curl $req
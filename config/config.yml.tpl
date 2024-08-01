API:
  secret: op://Server-Prod/ePrijzen API Key/password
  debug: False
db:
  name: energieprijzen.db
entsoe:
  key: op://Server-Prod/entsoe api key/password

# fill data from 1password
# op inject -i config/config.yml.tpl -o config/production.yml
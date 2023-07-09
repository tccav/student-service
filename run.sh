export DB_HOST="localhost"
export DB_PORT="5432"
export DB_USER="postgres"
export DB_PASSWORD="changeme"
export DB_NAME="students-service"
export DB_OPTIONS="sslmode=disable"

sanic app.server:app

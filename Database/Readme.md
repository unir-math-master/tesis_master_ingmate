## Remotly connecto to database in Jetson

- Open file `/etc/mysql/mariadb.conf.d/50-server.cnf`
- Edit:
```
 bind-address            = 127.0.0.1
```
to
```
bind-address            = 0.0.0.0
```
- Restart database
```
sudo systemctl restart mariadb
```
- Validate that service is listening the port
```
sudo netstat -tulnp | grep mysqld
```

### Create user for DB
```
CREATE USER 'user'@'%' IDENTIFIED BY 'some_pass';
GRANT ALL PRIVILEGES ON . TO 'user'@'%'  WITH GRANT OPTION;
```

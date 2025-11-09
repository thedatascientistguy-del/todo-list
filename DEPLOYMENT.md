# Deploying Todo List Application on EC2

## Prerequisites
1. AWS EC2 instance running (Ubuntu recommended)
2. Docker and Docker Compose installed on EC2
3. Port 8000 opened in EC2 security group
4. Git installed on EC2

## Installation Steps

1. Update the system and install dependencies:
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

2. Install Docker:
```bash
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

3. Install Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Clone your repository (replace with your repository URL):
```bash
git clone <your-repository-url>
cd todo-list
```

5. Start the application:
```bash
sudo docker-compose up -d
```

## Accessing the Application
- The application will be available at `http://your-ec2-ip:8000`
- Replace `your-ec2-ip` with your EC2 instance's public IP address

## Maintenance Commands

### View logs:
```bash
sudo docker-compose logs -f
```

### Restart the application:
```bash
sudo docker-compose restart
```

### Stop the application:
```bash
sudo docker-compose down
```

### Update the application:
```bash
git pull
sudo docker-compose down
sudo docker-compose up --build -d
```

## Backup and Restore

### Backup MongoDB data:
```bash
sudo docker exec -t todo-list_mongodb_1 mongodump --out /dump
sudo docker cp todo-list_mongodb_1:/dump ./backup
```

### Restore MongoDB data:
```bash
sudo docker cp ./backup todo-list_mongodb_1:/dump
sudo docker exec -t todo-list_mongodb_1 mongorestore /dump
```

## Monitoring
- Check container status:
```bash
sudo docker-compose ps
```

- Check resource usage:
```bash
sudo docker stats
```

## Troubleshooting
1. If the application is not accessible:
   - Check if containers are running: `sudo docker-compose ps`
   - Verify EC2 security group allows port 8000
   - Check application logs: `sudo docker-compose logs web`

2. If MongoDB connection fails:
   - Check MongoDB container logs: `sudo docker-compose logs mongodb`
   - Verify MongoDB container is running: `sudo docker ps | grep mongodb`

3. To reset the application:
```bash
sudo docker-compose down -v
sudo docker-compose up -d
```
# Real Estate Backend

A powerful and feature-rich Django-based real estate platform backend that combines modern API architecture with SEO-friendly server-side rendering. This project offers a unique hybrid approach, serving both as a REST API backend for mobile applications and a server-rendered website for optimal SEO performance.

## 🌟 Key Features

### Multi-language Support
- Full support for Arabic (RTL), English, and French
- Easy language switching with preserved state
- Localized content and UI elements

### Property Management
- Advanced property listing system
- Like and view counter for properties
- User engagement tracking
- Image gallery management
- Property favorites system

### Search and Filtering
- Comprehensive property search
- Advanced filtering options
- Location-based search
- Price range filters
- Property type filters
- Amenities filtering

### Algeria-Specific Features
- Complete integration of all Algeria states and cities
- Location-based property sorting
- Regional property trends

### Performance & Caching
- Redis caching implementation
- Optimized database queries
- Fast response times
- Efficient data loading

### Authentication & Security
- JWT-based authentication
- Social media login integration
- Role-based authorization
- Secure file upload handling
- Protected API endpoints

### Hybrid Architecture
- RESTful API for mobile applications
- Server-side rendered pages for SEO
- SPA-like experience with native HTML/CSS/JS
- Django templates for server rendering
- Progressive enhancement

### Infrastructure
- Docker containerization
- Nginx server configuration
- PostgreSQL database
- Redis caching
- Celery task queue
- Automated deployment

## 🛠 Tech Stack

- **Framework:** Django 5.0.3
- **API:** Django REST Framework 3.14.0
- **Authentication:** JWT with Djoser
- **Database:** PostgreSQL
- **Caching:** Redis
- **Task Queue:** Celery 5.3.6
- **Frontend:** Native HTML/CSS/JS + Django Templates
- **Server:** Nginx
- **Containerization:** Docker & Docker Compose
- **Languages:** Python, JavaScript
- **Monitoring:** Flower 2.0.1
- 
## 📸 Screenshots

![Screenshot 2025-06-15 at 14-53-14](images/Screenshot%202025-06-15%20at%2014-53-14%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 14-53-46](images/Screenshot%202025-06-15%20at%2014-53-46%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 14-54-08](images/Screenshot%202025-06-15%20at%2014-54-08%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 15-55-05](images/Screenshot%202025-06-15%20at%2015-55-05%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 16-49-13](images/Screenshot%202025-06-15%20at%2016-49-13%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 17-21-54](images/Screenshot%202025-06-15%20at%2017-21-54%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 17-27-06](images/Screenshot%202025-06-15%20at%2017-27-06%20Aures%20REAL%20ESTATE.png)
![Screenshot 2025-06-15 at 17-27-16](images/Screenshot%202025-06-15%20at%2017-27-16%20Aures%20REAL%20ESTATE.png)

## 🚀 Quick Start with Docker

The easiest way to get started is using our Makefile commands:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd real_estate_backend
   ```

2. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configurations
   ```

3. **Build and start the project**
   ```bash
   make build  # Builds and starts all containers
   ```

4. **Run migrations and create superuser**
   ```bash
   make migrate  # Apply database migrations
   make superuser  # Create admin user
   ```

### Additional Make Commands
```bash
make up          # Start containers
make down        # Stop containers
make show-logs   # View container logs
make collectstatic  # Collect static files
make estate-db   # Access PostgreSQL database
make test        # Run tests
make flake8      # Run code linting
```

## 📁 Project Structure

```
real_estate_backend/
├── apps/                  # Django applications
│   ├── properties/        # Property management
│   ├── users/            # User management
│   └── locations/        # Algeria locations
├── real_estate_backend/   # Project configuration
├── docker/               # Docker configuration
├── nginx/                # Nginx configuration
├── static/               # Static files
├── templates/            # Django templates
├── mediafiles/           # User uploads
└── locale/               # Translation files
```

## 🌐 API Documentation

Our API is fully documented and available at `/docs/api/`. The documentation includes:
- Complete endpoint listings
- Request/Response examples
- Authentication flows
- Filter parameters
- Status codes

Key API features:
- RESTful endpoints
- JWT authentication
- Comprehensive filtering
- Pagination
- Multi-language support

## 💻 Development Setup

For local development without Docker:

1. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup local services**
   - PostgreSQL
   - Redis
   - Nginx (optional for local)

4. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

Key environment variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/db_name
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 📱 Mobile App Integration

The API is designed to be easily integrated with mobile applications:
- Consistent API endpoints
- Token-based authentication
- Optimized response payloads
- File upload handling
- Push notification support

## 🔍 SEO Features

- Server-side rendering for critical pages
- Semantic HTML structure
- Optimized meta tags
- Sitemap generation
- robots.txt configuration
- Structured data implementation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For any queries or support, please contact [Your Contact Information]

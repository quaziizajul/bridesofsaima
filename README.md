# Brides of Saima Portal

A Django web application for Saima's bridal makeup business, featuring invoice management, bride gallery with carousel views, and admin authentication.

## Features

- **Admin Authentication**: Secure login system with admin-only access to invoice generation
- **Invoice Management**: Create, view, and manage customer invoices with payment tracking
- **Bride Gallery**: Showcase bridal work with multiple images per bride
- **Carousel View**: Interactive image carousel for viewing bride portfolios
- **Mobile Responsive**: Optimized for all devices with responsive design
- **QR Code Integration**: Instagram QR code on invoices for social media promotion

## Technologies Used

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5.1.3, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), ready for PostgreSQL (production)
- **Image Processing**: Pillow 11.3.0
- **Hosting**: Ready for PythonAnywhere deployment

## Project Structure

```
BridesOfSaimaPortal/
├── BridesOfSaima/              # Main Django app
│   ├── models.py               # Bride, BrideImage, Customer, Invoice models
│   ├── views.py                # Application views and logic
│   ├── templates/              # HTML templates
│   └── static/                 # CSS, JavaScript, images
├── media/                      # User uploaded images
├── requirements.txt            # Python dependencies
├── production_settings.py      # Production configuration
├── wsgi_config.py             # WSGI configuration for deployment
├── DEPLOYMENT_GUIDE.md        # Detailed deployment instructions
└── deploy.sh                  # Deployment automation script
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/BridesOfSaimaPortal.git
   cd BridesOfSaimaPortal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to view the application.

### Production Deployment

For detailed deployment instructions to PythonAnywhere, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## Key Features

### Admin Dashboard
- Secure authentication system
- Invoice generation and management
- Customer data management
- Bride gallery administration

### Bride Gallery
- Multiple images per bride
- Carousel view with navigation
- Responsive design for mobile devices
- Professional portfolio display

### Invoice System
- PDF-ready invoice generation
- Payment status tracking
- Customer information management
- QR code integration for social media

## Models

- **Customer**: Client information and contact details
- **Invoice**: Invoice data with payment tracking
- **Bride**: Bride information with primary image
- **BrideImage**: Additional images for each bride with ordering

## Admin Access

The application includes role-based access:
- **Admin users**: Full access to invoice generation and customer management
- **Public users**: View-only access to bride gallery and homepage

## Mobile Optimization

- Responsive navigation with collapsible menu
- Touch-friendly carousel controls
- Optimized image loading for mobile devices
- Single-line header layout for space efficiency

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is created for Saima's bridal makeup business. All rights reserved.

## Contact

For any questions or support, please contact the development team.

---

**Note**: This application is ready for production deployment. Follow the deployment guide for hosting on PythonAnywhere or other platforms.
# WhatsApp CRM Application

A comprehensive Customer Relationship Management system built for WhatsApp Business, featuring automated messaging, contact management, and analytics dashboard.

## 🚀 Features

- **Contact Management**: Organize and manage customer contacts
- **Broadcast Messaging**: Send bulk messages with templates
- **Analytics Dashboard**: Track message delivery and engagement metrics
- **AI Message Generator**: Generate personalized messages using AI
- **WooCommerce Integration**: Sync with your online store
- **Authentication System**: Secure user management
- **Real-time Chat**: Live chat interface for customer support

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database management
- **SQLAlchemy**: ORM for database operations
- **JWT**: Authentication and authorization
- **Dramatiq**: Background task processing

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Vue Router**: Client-side routing
- **Axios**: HTTP client for API requests
- **Chart.js**: Data visualization

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- npm or yarn

## 🚀 Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python simple_main.py
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run serve
   ```

The frontend will be available at `http://localhost:8081`

## 📁 Project Structure

```
wotnot/
├── backend/
│   ├── wati/                    # Main application package
│   │   ├── models/             # Database models
│   │   ├── routes/             # API endpoints
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/           # Business logic
│   ├── agent/                  # AI agent functionality
│   └── requirements.txt        # Python dependencies
├── frontend/app/
│   ├── src/
│   │   ├── components/         # Vue components
│   │   ├── views/              # Page components
│   │   └── router.js           # Route configuration
│   └── package.json            # Node.js dependencies
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend/app directory:

```env
VUE_APP_API_URL=http://localhost:8000
VUE_APP_NGROK_HOST=your-ngrok-host
VUE_APP_NGROK_PORT=443
```

### Database Setup

1. Install PostgreSQL
2. Create a database for the application
3. Update database configuration in `backend/wati/database/database.py`

## 📖 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- WhatsApp Business API
- Vue.js community
- FastAPI developers
- All contributors to this project

## 📞 Support

For support, email your-email@domain.com or create an issue in this repository.
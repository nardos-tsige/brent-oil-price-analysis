from api import app

if __name__ == '__main__':
    print("=" * 60)
    print("BRENT OIL API SERVER")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Available endpoints:")
    print("  GET /api/health")
    print("  GET /api/prices")
    print("  GET /api/events")
    print("  GET /api/categories")
    print("  GET /api/statistics")
    print("  GET /api/impacts")
    print("  GET /api/change-point")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
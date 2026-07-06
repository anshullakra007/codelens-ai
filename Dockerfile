FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY backend/requirements.txt ./backend/

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["sh", "-c", "cd backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

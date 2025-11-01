FROM python:3.13-slim

# Install Java
RUN apt-get update && apt-get install -y openjdk-25-jdk && apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-25-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "pdf_to_excel.py", "--server.port=8501", "--server.address=0.0.0.0"]

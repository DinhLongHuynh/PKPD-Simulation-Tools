# select starting image
FROM python:3.13.0-slim

# Create user name and home directory variables. 
# The variables are later used as $USER and $HOME. 
ENV USER=PKPD-SiAn
ENV HOME=/home/$USER
ENV DATA_DIR=$HOME/app/testdata
ENV IMG_DIR=$HOME/app/images

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy all files that the app needs (this will place the files in home/username/)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

USER $USER
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]

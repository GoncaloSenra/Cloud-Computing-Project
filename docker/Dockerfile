# Dockerfile for the laravel.io application
FROM ubuntu:20.04

# Define default values for the Environment Variables
ENV DB_CONNECTION=mysql
ENV DB_HOST=laraveldb
ENV DB_DATABASE=laravel
ENV DB_USERNAME=myuser
ENV DB_PASSWORD=password
ENV seed_database=false

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:ondrej/php && \
    apt-get update && \
    apt-get install -y \
        php8.2 \
        php8.2-fpm \
        php8.2-zip \
        php8.2-mbstring \
        php8.2-tokenizer \
        php8.2-mysql \
        php8.2-gd \
        php8.2-xml \
        php8.2-bcmath \
        php8.2-intl \
        php8.2-curl \
        nodejs \
        npm \
        curl \
        mysql-client \
        git \
	    sudo

# Clone Laravel repository
RUN git clone https://github.com/laravelio/laravel.io.git /laravel.io
WORKDIR /laravel.io

# Create Laravel configuration file
RUN cp .env.example .env
#RUN sed -i -e "/^DB_CONNECTION=/s/mysql/${DB_CONNECTION}/" .env
#RUN sed -i -e "/^DB_HOST=/s/127.0.0.1/${DB_HOST}/" .env
RUN echo "DB_HOST=${DB_HOST}" >> .env
RUN echo "DB_CONNECTION=${DB_CONNECTION}" >> .env
RUN sed -i "s/DB_DATABASE=laravel/DB_DATABASE=${DB_DATABASE}/" .env
RUN sed -i "s/DB_USERNAME=root/DB_USERNAME=${DB_USERNAME}/" .env
RUN sed -i "s/DB_PASSWORD=password/DB_PASSWORD=${DB_PASSWORD}/" .env

# Install Laravel composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && \
    php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    php -r "unlink('composer-setup.php');" && \
    composer update && \
    composer install

# Generate Laravel application key
RUN php artisan key:generate

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/nodesource-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/nodesource-archive-keyring.gpg] https://deb.nodesource.com/node_20.x $(lsb_release -s -c) main" > /etc/apt/sources.list.d/nodesource.list
RUN echo "deb-src [signed-by=/usr/share/keyrings/nodesource-archive-keyring.gpg] https://deb.nodesource.com/node_20.x $(lsb_release -s -c) main" >> /etc/apt/sources.list.d/nodesource.list
RUN apt-get update && apt-get install -y nodejs

# Install project dependencies and build assets
RUN npm install
RUN npm run build

# Expose port 8000
EXPOSE 8000

COPY ./script.sh .
RUN chmod +x script.sh
# Start Laravel server
#CMD sudo php artisan migrate --seed
#CMD php artisan serve --host=0.0.0.0
CMD ./script.sh



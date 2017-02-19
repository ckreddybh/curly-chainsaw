#! /bin/sh

# php.ini
sudo echo "memory_limit = 512M" > $PHPENV_ROOT/versions/$(phpenv global)/etc/conf.d/memory.ini

sudo echo "always_populate_raw_post_data = -1" > $PHPENV_ROOT/versions/$(phpenv global)/etc/conf.d/deprecated.ini

# echo "xdebug.max_nesting_level=1000" >> /home/rof/.phpenv/versions/$(phpenv version-name)/etc/conf.d/xdebug.ini
#rm $(PHPENV_ROOT)/.phpenv/versions/$(phpenv version-name)/etc/conf.d/xdebug.ini

# uglify
npm install -g uglify-js

# compass
gem install compass

NODE_PATH=$(which node)
UGLIFY_PATH=$(which uglifyjs)


# selenium server
./bin/selenium start


# git
git config --global user.email "chaitu949@gmail.com"
git config --global user.name "CK Reddy"

# phantomjs
./bin/phantomjs start

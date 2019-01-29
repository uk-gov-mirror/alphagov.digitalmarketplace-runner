#!/bin/bash

# install Docker
if ! command -v docker; then
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
	add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	apt-get update
	apt-get install -y docker-ce
	groupadd docker
	usermod -aG docker vagrant
fi

# install Docker Compose
if ! command -v docker-compose; then
	mkdir -p /usr/local/bin
	curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose 2> /dev/null
	chmod +x /usr/local/bin/docker-compose
fi

# install build prerequisites
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
	libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
	xz-utils tk-dev libffi-dev liblzma-dev python-openssl git cowsay

# install nvm
if [ ! -e /opt/nvm ]; then
	mkdir -p /opt/nvm
	(curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | NVM_DIR="/opt/nvm" bash) 2> /dev/null
	chmod -R a+rwx /opt/nvm
fi
if [ ! -e /etc/profile.d/nvm.sh ]; then
	cat > /etc/profile.d/nvm.sh <<- 'EOF'
		#!/bin/sh
		export NVM_DIR="/opt/nvm"
	EOF
	cat >> /home/vagrant/.bashrc <<- 'EOF'
		# enable nvm
		[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
		[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"
	EOF
fi

# install pyenv
if [ ! -e /opt/pyenv ]; then
	mkdir -p /opt/pyenv
	git clone https://github.com/pyenv/pyenv.git /opt/pyenv
	chmod -R a+rwx /opt/pyenv
fi
if [ ! -e /etc/profile.d/pyenv.sh ]; then
	cat > /etc/profile.d/pyenv.sh <<- 'EOF'
		#!/bin/sh
		export PYENV_ROOT="/opt/pyenv"
		export PATH="$PYENV_ROOT/bin:$PATH"
	EOF
	cat >> /home/vagrant/.bashrc <<- 'EOF'
		# enable pyenv shell
		if command -v pyenv 1>/dev/null 2>&1; then
			eval "$(pyenv init -)"
		fi
	EOF
fi

# get the digitalmarketplace runner
sudo -H -u vagrant bash <<- EOF
	if [ ! -e ~/digitalmarketplace ]; then
		mkdir ~/digitalmarketplace
		git clone https://github.com/alphagov/digitalmarketplace-runner ~/digitalmarketplace/digitalmarketplace-runner
	fi
EOF

# install python, node, and yarn
sudo -H -u vagrant bash <<- EOF
	cd ~/digitalmarketplace/digitalmarketplace-runner
	source /etc/profile

	PYTHON_VERSION="$(cat .python-version)"
	pyenv install "${PYTHON_VERSION}" 2> /dev/null
	pyenv global "${PYTHON_VERSION}" system

	source /opt/nvm/nvm.sh 2> /dev/null
	nvm install 2> /dev/null
	npm install -g yarn
EOF

# install system dependencies for communicating with postgres
apt-get install -y libpq-dev

# print a friendly message
/usr/games/cowsay -f tux <<- 'EOF'
	Setup complete!

	Use `vagrant ssh` to try out digitalmarketplace-runner.

	Note that you will need to add/create an ssh key to communicate with GitHub.
EOF

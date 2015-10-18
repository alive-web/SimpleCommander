help:
	@echo 'SimpleCommander'
	@echo ''
	@echo 'Bootstrapping:'
	@echo '   make setup        setup your machine for local development'
	@echo ''
	@echo 'Source code:'
	@echo '   make build        (re)build all static assets'
	@echo ''
	@echo 'Running'
	@echo '   make run          run the development servers'
	@echo '   make run-server   run command server'
	@echo '   make run-grunt    run grunt server'
	@echo ''
	@echo 'Testing'
	@echo '   make test         Run all unit tests'

setup:
	virtualenv -p python3 env
	. env/bin/activate; \
	pip install -r requirements.txt

build:
	cd www/; \
	sudo npm install -g grunt-cli bower; \
	sudo npm install; \
	bower install; \
	gem update --system; \
	gem install compass; \
	grunt

test:
	cd www/; \
	grunt test

run-server:
	. env/bin/activate; \
	python game_commander/game_commander.py

run-grunt:
	cd www/; \
	grunt serve

run:
	make run-server &
	make run-grunt &

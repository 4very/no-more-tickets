enable-git-hooks:
	git config --local include.path .gitconfig

compose-dev:
	$ (cd ./docker/dev && docker-compose up)
freeze:
	pip freeze | grep -v "pkg-resources" > requirements-dev.txt
	pipreqs . --savepath requirements.txt
docker_build_local:
	docker build -t vreader:latest .

docker_build_release_dev:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t gitea.va.reichard.io/evan/vreader:dev \
		--push .

docker_build_release_latest:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t gitea.va.reichard.io/evan/vreader:latest \
		-t gitea.va.reichard.io/evan/vreader:`git describe --tags` \
		--push .

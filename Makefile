docker_build_local: build_tailwind
	docker build -t vreader:latest .

docker_build_release_dev: build_tailwind
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t gitea.va.reichard.io/evan/vreader:dev \
		--push .

docker_build_release_latest: build_tailwind
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t gitea.va.reichard.io/evan/vreader:latest \
		-t gitea.va.reichard.io/evan/vreader:`git describe --tags` \
		--push .

build_tailwind:
	tailwind build -o ./vreader/static/tailwind.css --minify

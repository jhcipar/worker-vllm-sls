build:
	docker build -t username/image:tag --build-arg MODEL_NAME="Qwen/Qwen3-8B" --platform linux/amd64 --build-arg BASE_PATH="/models" .


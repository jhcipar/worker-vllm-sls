build:
	docker build -t username/image:tag --build-arg MODEL_NAME="nvidia/Llama-3.1-Nemotron-Nano-8B-v1" --platform linux/amd64 --build-arg BASE_PATH="/models" .


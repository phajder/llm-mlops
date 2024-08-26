# ML apps for the task
There are four apps:
1. [Train](./train/) - simulates training process. It takes dataset as input and outputs trained checkpoint. There is an [if statement](./train/main.py#L30) that simulate failure of training process.
2. [Eval](./eval/) - simulates evaluation process. It takes checkpoint as input and outputs exported model. No points for failure were implemented.
3. [Load](./load/) - simulates model loading process. This is just a fake step, that does not actually occur, but because model does not change, it was assumed that the main app doesn't have to change. Such an assumptions was made to simplify the execution.
4. [Serve](./serve/) - actual model serving application.

For apps 1-3 Dockerfiles are identical, but this will be not the case in typical scenarios. Also, the same happens for requirements files, that are empty.

## Broaded description for serve application
Serve application was made using llama-cpp-python, as described in [task 1](/task-1/README.md). Because it is required to build a wheel, [Dockerfile](./serve/Dockerfile) consists of two stages: build and serve. The main difference lies in the final size of both stages - CUDA runtime is much smaller than than devel. 

There is also small gotcha: path for pip libs is hardcoded. However, easy fix may utilize build args where python version is specified.

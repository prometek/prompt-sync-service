# Base image similaire au Dockerfile principal
FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
       && rm -rf /var/lib/apt/lists/*

# This is the arm64 version
RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-arm64.tar.gz \
    && tar -xzf nvim-linux-arm64.tar.gz -C /usr/local --strip-components=1 \
    && rm -f nvim-linux-arm64.tar.gz

# This is the x86_64 version
# RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz \
#    && tar -xzf nvim-linux-x86_64.tar.gz -C /usr/local --strip-components=1 \
#    && rm -f nvim-linux-x86_64.tar.gz


RUN pip install uv

# Créer l'utilisateur vscode
RUN useradd -m vscode
USER vscode
WORKDIR /workspace



# Installer uv et dépendances
COPY --chown=vscode:vscode pyproject.toml uv.lock /workspace/
RUN uv sync

# Exposer le port
EXPOSE 8000

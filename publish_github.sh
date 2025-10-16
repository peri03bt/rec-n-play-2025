#!/bin/bash

# 🚀 Script para Publicar no GitHub
# Autor: Sistema de IA
# Data: Outubro 2025

echo "======================================================"
echo "  🚀 PUBLICAÇÃO NO GITHUB"
echo "======================================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se está na pasta correta
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script da pasta raiz do projeto!${NC}"
    exit 1
fi

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não está instalado!${NC}"
    echo "Instale com: sudo apt-get install git"
    exit 1
fi

# Perguntar usuário do GitHub
echo -e "${YELLOW}Digite seu usuário do GitHub:${NC}"
read -r GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo -e "${RED}❌ Usuário não pode ser vazio!${NC}"
    exit 1
fi

REPO_NAME="rec-n-play-2025"

echo ""
echo -e "${GREEN}✅ Usuário: $GITHUB_USER${NC}"
echo -e "${GREEN}✅ Repositório: $REPO_NAME${NC}"
echo ""

# Verificar se .env existe e alertar
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env detectado!${NC}"
    echo -e "${GREEN}✅ Não se preocupe: .gitignore está configurado para protegê-lo${NC}"
    echo ""
fi

# Inicializar Git se necessário
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    echo -e "${GREEN}✅ Git inicializado!${NC}"
    echo ""
fi

# Configurar Git se necessário
if [ -z "$(git config user.name)" ]; then
    echo -e "${YELLOW}Configurar Git:${NC}"
    echo "Digite seu nome:"
    read -r GIT_NAME
    echo "Digite seu email:"
    read -r GIT_EMAIL
    
    git config --global user.name "$GIT_NAME"
    git config --global user.email "$GIT_EMAIL"
    echo -e "${GREEN}✅ Git configurado!${NC}"
    echo ""
fi

# Adicionar arquivos
echo "📁 Adicionando arquivos ao Git..."
git add .

# Verificar o que será commitado
echo ""
echo -e "${YELLOW}📋 Arquivos que serão enviados:${NC}"
git status --short
echo ""

# Confirmar
echo -e "${YELLOW}Deseja continuar? (s/n)${NC}"
read -r CONFIRM

if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    echo -e "${RED}❌ Cancelado pelo usuário${NC}"
    exit 1
fi

# Fazer commit
echo ""
echo "💾 Criando commit..."
git commit -m "🎉 Initial commit: Sistema de relatórios financeiros com IA

- Geração automática de relatórios com LangChain + Groq
- Gráficos visuais com Matplotlib
- Conversão automática para PDF
- Documentação completa
- Pronto para uso em produção"

echo -e "${GREEN}✅ Commit criado!${NC}"
echo ""

# Verificar se já existe remote
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}⚠️  Remote 'origin' já existe. Removendo...${NC}"
    git remote remove origin
fi

# Adicionar remote
echo "🔗 Conectando ao GitHub..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo -e "${GREEN}✅ Remote adicionado!${NC}"
echo ""

# Renomear branch para main
git branch -M main

# Fazer push
echo "🚀 Enviando para GitHub..."
echo ""
echo -e "${YELLOW}IMPORTANTE:${NC}"
echo "1. Crie o repositório em: https://github.com/new"
echo "   - Nome: $REPO_NAME"
echo "   - Visibilidade: Public"
echo "   - NÃO adicione README ou .gitignore"
echo ""
echo "2. Depois pressione ENTER para continuar..."
read -r

echo ""
echo "Fazendo push..."

if git push -u origin main; then
    echo ""
    echo "======================================================"
    echo -e "${GREEN}  ✅ SUCESSO! Projeto publicado no GitHub!${NC}"
    echo "======================================================"
    echo ""
    echo "🌐 Acesse seu repositório em:"
    echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "📝 Próximos passos:"
    echo "   1. Adicione uma descrição no repositório"
    echo "   2. Adicione topics: python, langchain, ai, groq"
    echo "   3. Compartilhe o link!"
    echo ""
else
    echo ""
    echo "======================================================"
    echo -e "${RED}  ❌ ERRO ao fazer push${NC}"
    echo "======================================================"
    echo ""
    echo "Possíveis causas:"
    echo "1. Repositório não foi criado no GitHub"
    echo "2. Usuário ou senha incorretos"
    echo "3. Precisa de token de acesso pessoal"
    echo ""
    echo "Solução:"
    echo "1. Crie o repositório em: https://github.com/new"
    echo "2. Use token em: https://github.com/settings/tokens"
    echo "3. Tente novamente: git push -u origin main"
    echo ""
fi


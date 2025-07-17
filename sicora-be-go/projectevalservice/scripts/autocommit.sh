#!/bin/bash

# Autocommit Script for ProjectEvalService
# Follows conventional commit standards and project guidelines

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project settings
PROJECT_NAME="projectevalservice"
BRANCH=$(git branch --show-current)

echo -e "${BLUE}🚀 ProjectEvalService AutoCommit Started${NC}"
echo -e "${BLUE}📁 Branch: ${BRANCH}${NC}"

# Check if we're in the right directory
if [ ! -f "go.mod" ] || ! grep -q "projectevalservice" go.mod; then
    echo -e "${RED}❌ Error: Not in projectevalservice directory${NC}"
    echo -e "${YELLOW}💡 Run this script from: 02-go/projectevalservice/${NC}"
    exit 1
fi

# Check if there are changes to commit
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Check code quality before commit
echo -e "${BLUE}🔍 Running code quality checks...${NC}"

# Go mod tidy
if ! go mod tidy; then
    echo -e "${RED}❌ go mod tidy failed${NC}"
    exit 1
fi

# Go build check
if ! go build -v ./...; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
if ! go test ./tests; then
    echo -e "${RED}❌ Tests failed${NC}"
    exit 1
fi

# Show git status
echo -e "${BLUE}📊 Git Status:${NC}"
git status --short

# Determine commit type based on file changes
COMMIT_TYPE="chore"
COMMIT_SCOPE=""
COMMIT_MESSAGE=""

# Check for new features
if git diff --cached --name-only | grep -E "(handlers|endpoints|routes)" > /dev/null; then
    COMMIT_TYPE="feat"
    COMMIT_SCOPE="api"
    COMMIT_MESSAGE="add new API endpoints"
elif git diff --cached --name-only | grep -E "entities" > /dev/null; then
    COMMIT_TYPE="feat"
    COMMIT_SCOPE="domain"
    COMMIT_MESSAGE="add domain entities"
elif git diff --cached --name-only | grep -E "usecases" > /dev/null; then
    COMMIT_TYPE="feat"
    COMMIT_SCOPE="application"
    COMMIT_MESSAGE="add use cases"
elif git diff --cached --name-only | grep -E "repositories" > /dev/null; then
    COMMIT_TYPE="feat"
    COMMIT_SCOPE="infrastructure"
    COMMIT_MESSAGE="add repository implementations"
elif git diff --cached --name-only | grep -E "test" > /dev/null; then
    COMMIT_TYPE="test"
    COMMIT_SCOPE="unit"
    COMMIT_MESSAGE="add unit tests"
elif git diff --cached --name-only | grep -E "(README|docs)" > /dev/null; then
    COMMIT_TYPE="docs"
    COMMIT_MESSAGE="update documentation"
elif git diff --cached --name-only | grep -E "(Dockerfile|docker|\.yml|\.yaml)" > /dev/null; then
    COMMIT_TYPE="config"
    COMMIT_SCOPE="docker"
    COMMIT_MESSAGE="update container configuration"
elif git diff --cached --name-only | grep -E "(go\.mod|go\.sum)" > /dev/null; then
    COMMIT_TYPE="chore"
    COMMIT_SCOPE="deps"
    COMMIT_MESSAGE="update dependencies"
fi

# Build commit message
if [ -n "$COMMIT_SCOPE" ]; then
    FULL_MESSAGE="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_MESSAGE}"
else
    FULL_MESSAGE="${COMMIT_TYPE}: ${COMMIT_MESSAGE}"
fi

# Stage all changes if nothing is staged
if git diff --staged --quiet; then
    echo -e "${BLUE}📝 Staging all changes...${NC}"
    git add .
fi

# Show what will be committed
echo -e "${BLUE}📤 Changes to be committed:${NC}"
git diff --staged --name-only | sed 's/^/  /'

# Commit with conventional message
echo -e "${BLUE}💾 Committing with message: ${GREEN}${FULL_MESSAGE}${NC}"
git commit -m "$FULL_MESSAGE"

# Show commit info
COMMIT_HASH=$(git rev-parse --short HEAD)
echo -e "${GREEN}✅ Commit successful: ${COMMIT_HASH}${NC}"

# Show recent commits
echo -e "${BLUE}📜 Recent commits:${NC}"
git log --oneline -5

# Optional: Auto-push (uncomment if needed)
# echo -e "${BLUE}🚀 Pushing to remote...${NC}"
# git push origin $BRANCH

echo -e "${GREEN}🎉 AutoCommit completed successfully!${NC}"

#!/bin/bash

# 인자로 issue_number와 issue_title을 받습니다.
if [ $# -ne 2 ]; then
    echo "Usage: $0 <issue_number> <issue_title>"
    exit 1
fi

ISSUE_NUMBER=$1
ISSUE_TITLE=$2

# GitHub 토큰과 저장소 정보를 환경 변수에서 가져옵니다.
GITHUB_TOKEN=$GITHUB_TOKEN
REPO=$GITHUB_REPOSITORY

# API 기본 URL
API_URL="https://api.github.com/repos/$REPO"

# 라벨을 결정합니다.
LABEL=""
if [[ $ISSUE_TITLE == REQ:* ]]; then
    LABEL="requirement"
elif [[ $ISSUE_TITLE == TEST:* ]]; then
    LABEL="test"
elif [[ $ISSUE_TITLE == "CI&CD:"* ]]; then
    LABEL="CI&CD"
fi

# 라벨을 추가합니다.
if [ ! -z "$LABEL" ]; then
    curl -X POST \
         -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         -d "{\"labels\":[\"$LABEL\"]}" \
         "$API_URL/issues/$ISSUE_NUMBER/labels"
    echo "Added label: $LABEL"
fi

# 'REQ:' 로 시작하는 경우 새 브랜치를 생성합니다.
if [[ $LABEL == "requirement" ]]; then
    # 유효하지 않은 문자 제거 및 소문자 변환
    CLEANED_TITLE=$(echo "${ISSUE_TITLE:4}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
    NEW_BRANCH_NAME="feature/${ISSUE_NUMBER}-${CLEANED_TITLE}"

    # develop 브랜치의 최신 SHA를 가져옵니다.
    DEVELOP_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                       -H "Accept: application/vnd.github.v3+json" \
                       "$API_URL/git/ref/heads/develop" | jq -r .object.sha)

    # 새 브랜치를 생성합니다.
    curl -X POST \
         -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         -d "{\"ref\":\"refs/heads/$NEW_BRANCH_NAME\", \"sha\":\"$DEVELOP_SHA\"}" \
         "$API_URL/git/refs"
    
    echo "Created new branch: $NEW_BRANCH_NAME"
fi

echo "Script completed successfully."
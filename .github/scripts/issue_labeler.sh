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
BRANCH_PREFIX=""
if [[ $ISSUE_TITLE == REQ:* ]]; then
    LABEL="requirement"
    BRANCH_PREFIX="req"
elif [[ $ISSUE_TITLE == FIX:* ]]; then
    LABEL="bugfix"
    BRANCH_PREFIX="fix"
elif [[ $ISSUE_TITLE == TEST:* ]]; then
    LABEL="test"
elif [[ $ISSUE_TITLE == "CI&CD:"* ]]; then
    LABEL="CI&CD"
fi

# 라벨을 추가합니다.
if [ ! -z "$LABEL" ]; then
    RESPONSE=$(curl -s -w "%{http_code}" -X POST \
         -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         -d "{\"labels\":[\"$LABEL\"]}" \
         "$API_URL/issues/$ISSUE_NUMBER/labels")
    
    HTTP_STATUS=$(echo $RESPONSE | tr -d '\n' | sed -e 's/.*$//')
    if [ $HTTP_STATUS -eq 200 ]; then
        echo "Added label: $LABEL"
    else
        echo "Failed to add label. HTTP status: $HTTP_STATUS"
    fi
fi

# 'REQ:' 또는 'FIX:'로 시작하는 경우 새 브랜치를 생성합니다.
if [[ $LABEL == "requirement" || $LABEL == "bugfix" ]]; then
    # 유효하지 않은 문자 제거, 소문자 변환, 그리고 길이 제한 (최대 50자)
    CLEANED_TITLE=$(echo "${ISSUE_TITLE:4}" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//' | cut -c1-50)
    NEW_BRANCH_NAME="$BRANCH_PREFIX/#${ISSUE_NUMBER}-${CLEANED_TITLE}"

    # develop 브랜치의 최신 SHA를 가져옵니다.
    DEVELOP_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                       -H "Accept: application/vnd.github.v3+json" \
                       "$API_URL/git/ref/heads/develop" | jq -r .object.sha)

    # 새 브랜치를 생성합니다.
    RESPONSE=$(curl -s -w "%{http_code}" -X POST \
         -H "Authorization: token $GITHUB_TOKEN" \
         -H "Accept: application/vnd.github.v3+json" \
         -d "{\"ref\":\"refs/heads/$NEW_BRANCH_NAME\", \"sha\":\"$DEVELOP_SHA\"}" \
         "$API_URL/git/refs")
    
    HTTP_STATUS=$(echo $RESPONSE | tr -d '\n' | sed -e 's/.*$//')
    if [ $HTTP_STATUS -eq 201 ]; then
        echo "Created new branch: $NEW_BRANCH_NAME"
    else
        echo "Failed to create branch. HTTP status: $HTTP_STATUS"
    fi
fi

echo "Script completed successfully."
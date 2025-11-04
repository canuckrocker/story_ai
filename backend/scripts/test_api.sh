#!/bin/bash

# Story AI - API Testing Script
# Quick tests for all major endpoints

BASE_URL="http://localhost:8000/api/v1"

echo "🧪 Testing Story AI API"
echo "========================"
echo ""

# Health check
echo "1. Health Check"
curl -s ${BASE_URL%/api/v1}/health | jq .
echo ""

# Create user
echo "2. Creating User"
USER_RESPONSE=$(curl -s -X POST $BASE_URL/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone_number": "+1234567890"
  }')
echo $USER_RESPONSE | jq .
USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
echo ""

# Create memory branch
echo "3. Creating Memory Branch"
BRANCH_RESPONSE=$(curl -s -X POST $BASE_URL/branches \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"branch_type\": \"childhood\",
    \"title\": \"My Childhood Memories\",
    \"description\": \"Stories from when I was young\"
  }")
echo $BRANCH_RESPONSE | jq .
BRANCH_ID=$(echo $BRANCH_RESPONSE | jq -r '.id')
echo ""

# Submit text input
echo "4. Submitting Text Input"
INPUT_RESPONSE=$(curl -s -X POST $BASE_URL/inputs \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": $USER_ID,
    \"memory_branch_id\": $BRANCH_ID,
    \"input_type\": \"text\",
    \"raw_text\": \"I remember when I was 8 years old, my family took a trip to the beach. It was my first time seeing the ocean.\"
  }")
echo $INPUT_RESPONSE | jq .
INPUT_ID=$(echo $INPUT_RESPONSE | jq -r '.id')
echo ""

# List user's branches
echo "5. Listing User's Branches"
curl -s $BASE_URL/branches/user/$USER_ID | jq .
echo ""

# List user's inputs
echo "6. Listing User's Inputs"
curl -s $BASE_URL/inputs/user/$USER_ID | jq .
echo ""

echo "✓ API tests complete!"
echo ""
echo "Created:"
echo "  User ID: $USER_ID"
echo "  Branch ID: $BRANCH_ID"
echo "  Input ID: $INPUT_ID"

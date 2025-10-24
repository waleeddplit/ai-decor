#!/bin/bash
# Revert to mock pages
# This script restores the original mock pages

echo "=========================================="
echo "⏮️  Reverting to Mock Pages"
echo "=========================================="
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Restore old files
echo "📦 Restoring backups..."
if [ -f "src/app/upload/page-old.tsx" ]; then
    mv src/app/upload/page-old.tsx src/app/upload/page.tsx
    echo "   ✅ Restored upload/page.tsx"
else
    echo "   ⚠️  No backup found for upload page"
fi

if [ -f "src/app/results/page-old.tsx" ]; then
    mv src/app/results/page-old.tsx src/app/results/page.tsx
    echo "   ✅ Restored results/page.tsx"
else
    echo "   ⚠️  No backup found for results page"
fi

echo ""
echo "=========================================="
echo "✅ Reverted to Mock Pages!"
echo "=========================================="
echo ""


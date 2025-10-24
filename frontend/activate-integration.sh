#!/bin/bash
# Activate Frontend-Backend Integration
# This script replaces the mock pages with real API-connected versions

echo "=========================================="
echo "🔄 Activating Frontend-Backend Integration"
echo "=========================================="
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"

# Backup old files
echo "📦 Creating backups..."
if [ -f "src/app/upload/page.tsx" ]; then
    cp src/app/upload/page.tsx src/app/upload/page-old.tsx
    echo "   ✅ Backed up upload/page.tsx"
fi

if [ -f "src/app/results/page.tsx" ]; then
    cp src/app/results/page.tsx src/app/results/page-old.tsx
    echo "   ✅ Backed up results/page.tsx"
fi

echo ""

# Activate new pages
echo "🚀 Activating new pages..."
if [ -f "src/app/upload/page-new.tsx" ]; then
    mv src/app/upload/page-new.tsx src/app/upload/page.tsx
    echo "   ✅ Activated new upload page"
else
    echo "   ⚠️  upload/page-new.tsx not found"
fi

if [ -f "src/app/results/page-new.tsx" ]; then
    mv src/app/results/page-new.tsx src/app/results/page.tsx
    echo "   ✅ Activated new results page"
else
    echo "   ⚠️  results/page-new.tsx not found"
fi

echo ""
echo "=========================================="
echo "✅ Integration Activated!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start backend: cd ../backend && ./venv/bin/uvicorn main:app --reload"
echo "2. Start frontend: npm run dev"
echo "3. Visit: http://localhost:3000/upload"
echo ""
echo "To revert changes, run: ./revert-integration.sh"
echo ""


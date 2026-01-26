#!/bin/bash
# Replace emojis with icons throughout the app

echo "🔄 Replacing emojis with professional icons..."

# Replace analytics page emojis
sed -i '' 's/▼/<Icon name="chevron-down" size={16} \/>/g' frontend/app/analytics/page.tsx
sed -i '' 's/🤖/<Icon name="bot" size={16} \/>/g' frontend/app/analytics/page.tsx
sed -i '' 's/⬇/<Icon name="download" size={16} \/>/g' frontend/app/analytics/page.tsx

# Replace sources page emojis
sed -i '' 's/➕/<Icon name="plus" size={16} \/>/g' frontend/app/sources/page.tsx

# Replace navigation emojis
sed -i '' "s/'🏠'/<Icon name=\"home\" size={16} \/>/g" frontend/components/Navigation.tsx
sed -i '' "s/'📊'/<Icon name=\"dashboard\" size={16} \/>/g" frontend/components/Navigation.tsx
sed -i '' "s/'📝'/<Icon name=\"content\" size={16} \/>/g" frontend/components/Navigation.tsx
sed -i '' "s/'🔗'/<Icon name=\"sources\" size={16} \/>/g" frontend/components/Navigation.tsx
sed -i '' "s/'📈'/<Icon name=\"analytics\" size={16} \/>/g" frontend/components/Navigation.tsx

# Replace settings page emojis
sed -i '' 's/☀️/<Icon name="sun" size={16} \/>/g' frontend/app/settings/page.tsx
sed -i '' 's/🌙/<Icon name="moon" size={16} \/>/g' frontend/app/settings/page.tsx
sed -i '' 's/💻/<Icon name="settings" size={16} \/>/g' frontend/app/settings/page.tsx

# Replace content type emojis in forms
sed -i '' 's/📄 Article/<Icon name="article" size={16} \/> Article/g' frontend/app/content/add/page.tsx
sed -i '' 's/🎥 Video/<Icon name="video" size={16} \/> Video/g' frontend/app/content/add/page.tsx
sed -i '' 's/📝 Note/<Icon name="note" size={16} \/> Note/g' frontend/app/content/add/page.tsx
sed -i '' 's/🔗 Link/<Icon name="link" size={16} \/> Link/g' frontend/app/content/add/page.tsx

# Replace error boundary emoji
sed -i '' 's/⚠️/<Icon name="alert" size={48} \/>/g' frontend/lib/ErrorBoundary.tsx

echo "✅ Emoji replacement complete!"

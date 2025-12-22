import codecs

# Read the original file from git
import subprocess
result = subprocess.run(['git', 'show', '686dcb4:templates/home.html'], 
                       capture_output=True, text=False, cwd=r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api')
content = result.stdout.decode('utf-8')

# Add PWA support
# Find and add manifest link after the font link
content = content.replace(
    '        rel="stylesheet" />',
    '        rel="stylesheet" />\n    <link rel="manifest" href="/static/manifest.json">\n    <meta name="theme-color" content="#10b981">',
    1
)

# Add service worker registration before the ticker update
sw_code = '''        // Register Service Worker for PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.log('ServiceWorker registration successful');
                    })
                    .catch(err => {
                        console.log('ServiceWorker registration failed: ', err);
                    });
            });
        }

        '''
content = content.replace('        // Init\n        updateTicker();', sw_code + '// Init\n        updateTicker();')

# Write with UTF-8 encoding
with codecs.open(r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api\templates\home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("File restored with correct UTF-8 encoding and PWA support added!")

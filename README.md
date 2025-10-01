# 🌟 QING Jixiang's Academic Website

A modern, hybrid academic website that **automatically syncs with Google Scholar** while allowing **manual enhancements** with videos, GIFs, and interactive content.

## ✨ Key Features

### 🤖 Automatic Publication Management
- **Auto-sync with Google Scholar** - Weekly automatic updates
- **Smart categorization** - By year, venue type, citations
- **Fallback system** - Works even if Scholar is unavailable

### 🎨 Manual Enhancements
- **Rich media support** - Videos, GIFs, images for each publication
- **Custom descriptions** - Override auto-generated content
- **Additional links** - Demos, code, slides, posters
- **Tags and featured status** - Organize and highlight important work

### 🎯 Modern Web Features
- **Responsive design** - Works on all devices
- **Dynamic filtering** - Isotope.js for smooth content organization
- **Fast loading** - Optimized static site with dynamic content
- **GitHub Pages ready** - Free hosting with automatic updates

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone [your-repo]
cd qing-new-website
```

### 2. Customize Your Information
Update your details in `index.html`:
- Name, affiliation, research interests
- Profile image (`images/profile.png`)
- Social media links

### 3. Configure Auto-Publications
The system will automatically find your Google Scholar profile based on:
- Your name: \"Jixiang Qing\"
- Institution: \"Ghent University\"
- Research keywords: \"Bayesian optimization\"

### 4. Add Media Enhancements
Edit `publications_manual.json` to add videos, GIFs, and custom content:

```json
{
  \"your_paper_id_2023\": {
    \"media\": {
      \"type\": \"video\",
      \"url\": \"images/demo.mp4\",
      \"description\": \"Algorithm demonstration\"
    },
    \"featured\": true,
    \"tags\": [\"bayesian-optimization\", \"multi-objective\"]
  }
}
```

### 5. Deploy to GitHub Pages
1. Push to your GitHub repository
2. Enable GitHub Pages in repository settings
3. Choose source: \"Deploy from a branch\" → \"main\"
4. Your site will be available at `https://yourusername.github.io/repository-name`

## 📚 Publication System

### How It Works
```
Google Scholar → Python Script → JSON Data → Dynamic Website
                     ↓
              Manual Enhancements (videos/GIFs/custom content)
```

### File Structure
```
📁 Project Root
├── 📄 index.html                    # Main website
├── 📄 publications.json             # Auto-generated (don't edit manually)
├── 📄 publications_manual.json      # Your enhancements (edit this!)
├── 📁 scripts/
│   ├── 📄 fetch_scholar.py         # Scholar sync script
│   └── 📄 requirements.txt         # Python dependencies
├── 📁 .github/workflows/
│   └── 📄 update-publications.yml  # Auto-update workflow
└── 📁 images/                      # Media files (videos, GIFs, images)
```

### Adding Media to Publications

**Step 1**: Add your media files to `images/` folder
```
images/
├── paper_demo.mp4        # Video demonstrations
├── algorithm.gif         # Animated visualizations  
├── results_plot.png      # Static images
└── thumbnail.jpg         # Custom thumbnails
```

**Step 2**: Link media in `publications_manual.json`
```json
{
  \"spectral_representation_2022\": {
    \"media\": {
      \"type\": \"gif\",
      \"url\": \"images/algorithm.gif\",
      \"description\": \"Spectral method visualization\"
    },
    \"custom_description\": \"Our approach to robust optimization...\",
    \"featured\": true
  }
}
```

**Step 3**: Commit and push - updates appear automatically!

## 🔄 Automatic Updates

### Weekly Auto-Sync
- **When**: Every Sunday at 2 AM UTC
- **What**: Fetches latest publications from Google Scholar
- **Result**: `publications.json` updated automatically

### Manual Trigger
Go to **Actions** tab → **Update Publications** → **Run workflow**

### What Gets Updated
- ✅ New publications automatically added
- ✅ Citation counts refreshed
- ✅ Author metrics updated (h-index, total citations)
- ✅ Your manual enhancements preserved

## 🎨 Customization

### Media Types Supported
- **Videos**: `.mp4`, `.webm` with controls
- **GIFs**: `.gif` with auto-play  
- **Images**: `.png`, `.jpg`, `.svg` with zoom

### Publication Categories
- **By Year**: Automatic chronological grouping
- **By Type**: Conference, Journal, Workshop
- **Featured**: Your most important work
- **Tagged**: Custom research categories

### Featured Publications
Mark important papers with blue highlight:
```json
\"featured\": true
```

### Research Tags
Organize by research areas:
```json
\"tags\": [\"bayesian-optimization\", \"active-learning\", \"gaussian-processes\"]
```

## 🛠️ Advanced Setup

### Local Testing
```bash
# Install Python dependencies
cd scripts
pip install -r requirements.txt

# Test Scholar fetching
python fetch_scholar.py

# Open index.html to preview
```

### Custom Scholar Search
If auto-detection fails, update the search query in `scripts/fetch_scholar.py`:
```python
search_query = scholarly.search_author('Your Name Institution Keywords')
```

### Manual-Only Publications
Add papers not on Scholar:
```json
{
  \"workshop_paper_2024\": {
    \"manual_only\": true,
    \"title\": \"Workshop Paper Title\",
    \"authors\": \"Your Name, Collaborators\",
    \"year\": \"2024\",
    \"venue\": \"ML Workshop\",
    \"url\": \"https://paper-link.com\"
  }
}
```

## 📖 Documentation

- **[Publications Guide](PUBLICATIONS_GUIDE.md)**: Complete guide for managing publications
- **[GitHub Actions](,github/workflows/update-publications.yml)**: Auto-update configuration
- **[Scholar Script](scripts/fetch_scholar.py)**: Publication fetching logic

## 🔧 Troubleshooting

### Publications not loading?
1. Check browser console for errors
2. Verify `publications.json` exists
3. Check GitHub Actions logs

### Scholar sync failing?
1. Verify your profile is public
2. Check rate limiting (Scholar blocks excessive requests)
3. Update search terms in fetch script

### Media not displaying?
1. Check file paths (relative to website root)
2. Verify file formats are supported
3. Ensure files are committed to repository

## 🎯 Migration from Jekyll

This website replaces Jekyll-based academic sites with:
- ✅ **Faster loading** - No build process required
- ✅ **Better multimedia** - Native video/GIF support
- ✅ **Auto-updates** - No manual publication management
- ✅ **Easier customization** - Direct HTML/CSS editing
- ✅ **GitHub Pages compatible** - Free hosting

## 🤝 Contributing

Found a bug or want to suggest an improvement?
1. Open an issue describing the problem
2. Fork the repository and make your changes
3. Submit a pull request

## 📄 License

Based on [Allen Z. Ren's website template](https://allenzren.github.io/). 
Free to use for academic and personal websites.

---

**🚀 Ready to deploy?** Push to GitHub, enable Pages, and watch your publications auto-sync!
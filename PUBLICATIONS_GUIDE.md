# 📚 Publications Management Guide

This guide explains how to use the hybrid publication system that automatically fetches your papers from Google Scholar while allowing manual enhancements with GIFs, videos, and custom content.

## 🔄 How It Works

### Automatic Fetching
- **GitHub Actions** runs weekly to fetch your latest publications from Google Scholar
- **Python script** (`scripts/fetch_scholar.py`) processes the data
- **JSON file** (`publications.json`) is generated and committed automatically
- **Website** loads publications dynamically from the JSON

### Manual Enhancements
- **Manual file** (`publications_manual.json`) allows you to add:
  - 🎥 Videos and GIFs
  - 🖼️ Custom images and thumbnails  
  - 📝 Custom descriptions
  - 🔗 Additional links (demos, code, slides)
  - 🏷️ Tags and categories
  - ⭐ Featured status

## 📁 File Structure

```
qing-new-website/
├── index.html                    # Main website
├── publications.json             # Auto-generated from Scholar
├── publications_manual.json      # Your manual enhancements
├── scripts/
│   └── fetch_scholar.py         # Scholar fetching script
├── .github/workflows/
│   └── update-publications.yml  # Auto-update workflow
└── images/                      # Media files
```

## 🎯 Adding Media to Publications

### Step 1: Add Your Media Files
Place your files in the `images/` directory:
```
images/
├── your_paper_demo.mp4       # Videos
├── algorithm_animation.gif   # GIFs  
├── results_plot.png          # Images
└── paper_thumbnail.jpg       # Thumbnails
```

### Step 2: Get Publication ID
Publications are identified by a unique ID. Run the fetch script to see IDs:
```bash
cd scripts
python fetch_scholar.py
```

Or check the generated `publications.json` for the `id` field.

### Step 3: Add Manual Enhancement
Edit `publications_manual.json`:

```json
{
  \"your_publication_id_2023\": {
    \"media\": {
      \"type\": \"video\",
      \"url\": \"images/your_demo.mp4\",
      \"thumbnail\": \"images/thumbnail.png\",
      \"description\": \"Demo showing the algorithm in action\"
    },
    \"custom_description\": \"Enhanced description of your work\",
    \"links\": [
      {\"text\": \"Paper\", \"url\": \"https://link-to-paper.com\"},
      {\"text\": \"Code\", \"url\": \"https://github.com/you/repo\"},
      {\"text\": \"Demo\", \"url\": \"https://your-demo.com\"}
    ],
    \"tags\": [\"bayesian-optimization\", \"machine-learning\"],
    \"featured\": true
  }
}
```

## 🎨 Media Types Supported

### Videos (.mp4, .webm)
```json
\"media\": {
  \"type\": \"video\",
  \"url\": \"images/demo.mp4\",
  \"description\": \"Algorithm demonstration\"
}
```

### GIFs (.gif)
```json
\"media\": {
  \"type\": \"gif\", 
  \"url\": \"images/animation.gif\",
  \"description\": \"Optimization process visualization\"
}
```

### Images (.png, .jpg, .svg)
```json
\"media\": {
  \"type\": \"image\",
  \"url\": \"images/results.png\",
  \"description\": \"Experimental results\"
}
```

## 🏷️ Tags and Categories

Add tags to categorize your publications:

```json
\"tags\": [
  \"bayesian-optimization\",
  \"multi-objective\", 
  \"uncertainty-quantification\",
  \"engineering-applications\"
]
```

Common tags for your research:
- `bayesian-optimization`
- `active-learning` 
- `gaussian-processes`
- `multi-objective`
- `robust-optimization`
- `engineering-design`
- `aerospace`
- `machine-learning`

## ⭐ Featured Publications

Mark important publications as featured:

```json
\"featured\": true
```

Featured publications get:
- Blue left border highlight
- Priority in display order
- Special styling

## 🔗 Custom Links

Add multiple links per publication:

```json
\"links\": [
  {\"text\": \"Paper\", \"url\": \"https://proceedings.mlr.press/...\"},
  {\"text\": \"Code\", \"url\": \"https://github.com/TsingQAQ/...\"},
  {\"text\": \"Slides\", \"url\": \"path/to/slides.pdf\"},
  {\"text\": \"Poster\", \"url\": \"path/to/poster.pdf\"},
  {\"text\": \"Demo\", \"url\": \"https://interactive-demo.com\"},
  {\"text\": \"Video\", \"url\": \"https://youtube.com/watch?v=...\"}
]
```

## 📝 Manual-Only Publications

Add publications not found on Scholar:

```json
\"manual_paper_2024\": {
  \"manual_only\": true,
  \"title\": \"Upcoming Conference Paper\",
  \"authors\": \"Jixiang Qing, Collaborators\",
  \"year\": \"2024\",
  \"venue\": \"Future ML Conference\",
  \"abstract\": \"Description of the work...\",
  \"url\": \"https://paper-link.com\",
  \"media\": {
    \"type\": \"gif\",
    \"url\": \"images/new_method.gif\"
  },
  \"featured\": true
}
```

## 🔄 Update Process

### Automatic Updates
1. **Weekly**: GitHub Actions runs every Sunday at 2 AM UTC
2. **Manual**: Go to Actions tab → \"Update Publications\" → \"Run workflow\"
3. **On changes**: Pushes to `publications_manual.json` trigger updates

### Manual Testing
Test locally before pushing:
```bash
cd scripts
python fetch_scholar.py
```

Then open `index.html` to see the results.

## 🐛 Troubleshooting

### Publications not loading?
1. Check browser console for JavaScript errors
2. Verify `publications.json` exists and is valid JSON
3. Check GitHub Actions logs for fetch errors

### Media not displaying?
1. Verify file paths are correct (relative to website root)
2. Check file formats are supported (mp4, gif, png, jpg)
3. Ensure files are committed to repository

### Scholar fetching failed?
1. Check if your profile is publicly accessible
2. Update search query in `fetch_scholar.py`
3. Scholar may be rate-limiting - wait and retry

## 📊 Publication Analytics

The system tracks:
- **Citation counts** from Scholar
- **Publication venues** and types
- **Recent publications** (last 3 years)
- **Featured publications**

View in `publications.json`:
```json
{
  \"author_info\": {
    \"total_citations\": 150,
    \"h_index\": 8,
    \"i10_index\": 5
  },
  \"categorized\": {
    \"by_year\": {...},
    \"by_type\": {...},
    \"recent\": [...],
    \"featured\": [...]
  }
}
```

## 🎯 Best Practices

1. **Use descriptive media**: Add clear descriptions for accessibility
2. **Optimize file sizes**: Compress videos/GIFs for faster loading
3. **Test locally**: Always test before pushing changes
4. **Update regularly**: Review and update manual enhancements quarterly
5. **Featured wisely**: Don't mark everything as featured
6. **Consistent tagging**: Use standard tag names across publications

## 🚀 Advanced Features

### Custom Venue Names
Override auto-detected venue names:
```json
\"custom_venue\": \"International Conference on Machine Learning (ICML)\"
```

### Custom Author Lists  
Fix author name formatting:
```json
\"custom_authors\": \"Jixiang Qing, Henry B. Moss, Tom Dhaene, Ivo Couckuyt\"
```

### Publication Descriptions
Add context beyond abstracts:
```json
\"custom_description\": \"This work introduces a novel approach to multi-objective optimization that handles constraints efficiently in parallel settings.\"
```

Your hybrid publication system is now ready! 🎉
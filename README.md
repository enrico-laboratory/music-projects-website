# Music Projects Website

A static website generator that publishes music project information from the music-projects-database workspace.

## Build Pipeline

### Workflow Overview

```
Database Changes          Build              Deployment
──────────────────────────────────────────────────────────
Edit database
(../music-projects-database/)
        │
        ├─→ [COMMIT database changes]
        │
        ├─→ Run: python3 generate.py
        │
        ├─→ Review generated HTML
        │   (html/*.html)
        │
        ├─→ [COMMIT generated files]
        │
        └─→ Deploy html/ folder
            (GitHub Pages, Netlify, etc.)
```

### Step-by-Step Workflow

#### 1. Edit Database Content

Make changes in `../music-projects-database/`:
```bash
cd ../music-projects-database

# Add/edit entries in music-projects/, agenda/, repertoire/, etc.
vim music-projects/my-project.md
vim agenda/2024-05-15-concert.md

# Commit database changes
git add .
git commit -m "Add concert on May 15, 2024"
```

#### 2. Generate Static Website

```bash
cd ../music-projects-website

# Build static HTML from updated database
python3 generate.py

# Output:
# Loading database...
# Generating 40 project pages...
# ✓ Generated index.html
# ✓ Generated a-day-with-arianna.html (1 agenda, 4 music)
# ✓ Generated festa.html (45 agenda, 26 music)
# ... (38 more projects)
# Done! 40 projects generated.
```

#### 3. Test the Generated Site

```bash
# Open in browser to review
open html/index.html

# Manual checks:
# - Homepage shows updated projects
# - All tabs load correctly
# - New agenda items appear in Schedule tab
# - New repertoire items appear in Music/Divisi tabs
# - Links work (score PDFs, navigation)
# - Responsive design works on mobile
```

#### 4. Commit Generated Files

```bash
# Stage only the generated HTML changes
git add html/

# Commit with reference to database changes
git commit -m "Rebuild website after adding May concert

- Regenerated from updated music-projects-database
- 45 agenda items now in Festa schedule
- All pages reflect latest database state"
```

#### 5. Push to Main Branch

```bash
# Push generated files to main branch
git push origin main
```

#### 6. Deploy to GitHub Pages

Ask Claude: "Deploy the website to GitHub Pages"

Claude will run:
```bash
git fetch origin gh-pages
git checkout gh-pages
rm -rf * .gitignore
cp -r html/* .
git add .
git commit -m "Deploy: updated projects"
git push origin gh-pages
```

Your website updates at https://projects.enricoruggieri.com

### Important Rules

⚠️ **Always commit database changes BEFORE running generate.py**
- Database is the source of truth
- Build artifacts (HTML) are derived from database
- This makes it easy to see what changed: git diff shows DB edits

⚠️ **Always run generate.py BEFORE committing HTML**
- Never hand-edit html/ files
- HTML is generated, not written manually
- Re-running generate.py keeps everything in sync

⚠️ **Test locally before deploying**
- Review html/index.html after building
- Check all tabs and links work
- Test on mobile browser
- Then commit and push

## Quick Start

### Build the Website

```bash
# Generate static HTML from database
python3 generate.py

# Opens the generated site
open html/index.html
```

### Project Structure

- **`generate.py`** — Python script that reads the database and generates static HTML files
- **`layout/`** — Markdown templates for customizing page layouts (edit these to change the design)
- **`html/`** — Generated static website (output folder, ready for deployment)
  - `index.html` — Homepage listing all projects
  - `projects/*.html` — Individual project pages with tabs
  - `css/style.css` — Responsive styling
- **`CLAUDE.md`** — Agent guidance for working with this project

## How It Works

The build process:

1. **Reads the database** — Scans `../music-projects-database` for all entries
2. **Resolves relationships** — Follows UUID links between tables (projects → agenda → locations, projects → repertoire → music, etc.)
3. **Extracts data** — Pulls YAML frontmatter and markdown content from each entry
4. **Generates HTML** — Creates static HTML pages by combining database data with templates
5. **Outputs site** — Writes fully-formed HTML to `html/` folder

## Customizing the Website

### Edit Layout Templates

Markdown files in `layout/` control how pages render:

- **`layout/index.md`** — Homepage layout (project list)
- **`layout/project.md`** — Individual project pages (tabs: description, schedule, music, divisi)

Edit these files to change colors, text, structure, etc. The next time you run `generate.py`, the changes apply.

### Editing CSS

Modify `html/css/style.css` directly for styling changes (colors, fonts, spacing, responsive design).

### Modifying Data

To add/edit content:

1. Edit files in `../music-projects-database`
2. Run `python3 generate.py`
3. The HTML is regenerated automatically

## Page Structure

### Index Page (`index.html`)

- Lists all music projects in chronological order
- Shows project status (Completed, On Going, Cancelled)
- Click to view project details

### Project Detail Pages (`projects/{uuid}.html`)

**Tab 1: Description**
- Project overview
- Concert dates with location and address

**Tab 2: Schedule**
- All rehearsals and concerts
- Date, time, and location (on the right)
- Program details for each event

**Tab 3: Music**
- Repertoire list
- Composer name for each piece
- Link to sheet music PDF (where available)

**Tab 4: Divisi**
- Voice assignments by piece
- Staff number and voice type (S1, S2, A, T1, etc.)
- Composer name

## Database Reference

See `../music-projects-database/README.md` and `../music-projects-database/Notion.md` for complete database schema and field definitions.

## When to Rebuild

### Manual Rebuild

Run `python3 generate.py` whenever you:
- Add a new project to the database
- Edit project details (description, year, status)
- Add/remove rehearsals or concerts
- Update repertoire or divisi information
- Change location information
- Update score URLs or composer details

### Automatic Rebuild (Recommended)

**GitHub Actions** (free with GitHub):

Create `.github/workflows/build.yml`:
```yaml
name: Build Website

on:
  push:
    paths:
      - '../music-projects-database/**'
      - 'generate.py'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: python3 generate.py
      - run: git add html/
      - run: git commit -m "Auto-rebuild website"
      - run: git push
```

This automatically rebuilds whenever database changes are pushed.

**Netlify** (one-click setup):

1. Connect repo to Netlify
2. Set build command: `python3 generate.py`
3. Set publish directory: `html/`
4. Save — Netlify rebuilds on every push

## Deployment

The `html/` folder is ready for static hosting:

- **GitHub Pages** — Push `html/` to `gh-pages` branch
  ```bash
  git subtree push --prefix html origin gh-pages
  ```

- **Netlify** — Connect repo, set build command to `python3 generate.py`, publish folder to `html/`
  - Builds automatically on every push

- **Vercel** — Similar setup as Netlify
  - Create `vercel.json`:
  ```json
  {
    "buildCommand": "python3 generate.py",
    "outputDirectory": "html"
  }
  ```

- **Any static host** — Upload contents of `html/` folder

## Project Coverage

The website currently publishes **40 music projects** from the database, including:
- Festa (2022) — 45 rehearsals, 26 music pieces
- A day with Arianna (2024) — 1 concert, 4 music pieces
- Echos of Venice (2027) — 5 rehearsals, 13 music pieces
- And 37 additional projects

All projects are automatically included. Run `python3 generate.py` to generate pages for all projects in the database.

---

## Troubleshooting

### Build fails or produces empty pages

**Problem**: Generated HTML is empty or missing data

**Solutions**:
1. Check database entries exist in `../music-projects-database/`
2. Verify UUIDs in agenda/repertoire match project UUIDs
3. Ensure YAML frontmatter is valid (proper indentation)
4. Run `python3 generate.py` again to regenerate

### Changes don't appear in generated site

**Problem**: Modified database but site hasn't updated

**Solutions**:
1. Did you commit database changes? (`git add . && git commit`)
2. Did you run `python3 generate.py`? (from music-projects-website folder)
3. Did you reload html/index.html in browser? (hard refresh: Cmd+Shift+R)
4. Check git status: `git status` should show modified `html/` files

### Score links don't work

**Problem**: Score PDF buttons don't link to files

**Solutions**:
1. Check music entry has `score_url:` field with valid URL
2. Verify URL is accessible (test in browser directly)
3. Rebuild with `python3 generate.py`
4. Inspect HTML source to confirm URL is there

### Location information missing from Schedule tab

**Problem**: Rehearsals show no venue information

**Solutions**:
1. Verify agenda entry has `location_id:` field
2. Confirm location UUID exists in `locations/` table
3. Check location entry has `location:` and `address:` fields
4. Rebuild with `python3 generate.py`

For detailed debugging, see **[CLAUDE.md](./CLAUDE.md#debugging)**.

---

For agent development, see **[CLAUDE.md](./CLAUDE.md)**.

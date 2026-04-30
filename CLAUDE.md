# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static website generator that publishes information about all music projects. The site reads content from the [music-projects-database](../music-projects-database) workspace and renders it as a fully-featured HTML/CSS website with 40 projects.

The database contains 9 tables organized as Markdown files with YAML frontmatter. The build process generates a page for each project with 4 tabs:
- **Description** — Project overview and concert dates with locations
- **Schedule** — Rehearsals and concerts with location/address on the right and program details
- **Music** — Repertoire list with composer names and score links
- **Divisi** — Voice assignments in table format with composer names

## Directory Structure

```
music-projects-website/
├── CLAUDE.md              # This file
├── README.md              # Build instructions and deployment guide
├── generate.py            # Python build script (no dependencies needed)
├── layout/                # Markdown layout templates (user-editable)
│   ├── index.md           # Homepage template
│   └── project.md         # Project detail page template
├── html/                  # Generated static website (output)
│   ├── index.html         # Homepage
│   ├── projects/          # Project detail pages
│   ├── css/style.css      # Responsive styling
│   └── ...                # Static assets
└── src/                   # (Legacy - not used, keep for reference)
```

## Build System

### Running the Build

```bash
python3 generate.py
```

This script:
1. Loads all database entries from `../music-projects-database`
2. Filters for Production projects (defined in `Production_PROJECTS` list)
3. Resolves relationships between tables via UUIDs
4. Extracts divisi information from repertoire markdown
5. Generates static HTML to `html/` folder

### Build Script Details

**Location**: `generate.py`

**Key Functions**:
- `parse_yaml()` — Parses YAML frontmatter without external dependencies
- `load_entries()` — Reads all markdown files from a table
- `get_project_agenda()` — Queries agenda items linked to a project
- `get_project_repertoire()` — Queries repertoire with music details
- `extract_divisi_html()` — Parses divisi tables from repertoire markdown
- `extract_program()` — Extracts program details from agenda markdown
- `generate_project_html()` — Renders project pages with all tabs

**Project Generation**:
The script automatically loads all projects from the database and generates a page for each. Projects are sorted alphabetically by title and assigned URL-safe filenames using the `slugify()` function.

## Working with the Database

### Data Flow

```
music-projects-database/
├── music-projects/ ──→ Project title, year, status, description
├── agenda/ ──────────→ Rehearsals/concerts with location_id, program
├── repertoire/ ──────→ Music pieces per project with divisi tables
├── music/ ───────────→ Piece titles, composers, score URLs
├── locations/ ───────→ Venue names, addresses
└── composers/ ───────→ Composer names
```

### Field References

**Agenda entries** have:
- `type` — "Rehearsal" or "Concert"
- `do_date` — ISO 8601 timestamp
- `location_id` — UUID reference to locations table
- `music_project_id` — UUID reference to music-projects table
- `## Program` section in markdown — Event description/program

**Repertoire entries** have:
- `order` — Sequence number
- `music_id` — UUID reference to music table
- `music_project_id` — UUID reference to music-projects table
- `## Divisi` section in markdown — Staff and voice assignments table

**Music entries** have:
- `music` — Title
- `composer_id` — UUID reference to composers table
- `voices` — SATB, SSATB, etc.
- `score_url` — Link to PDF

**Locations** have:
- `location` — Venue name
- `address` — Street address
- `city` — City name

### Key Principles

1. **UUID is the primary key** — All relationships use UUID, never text names
2. **YAML frontmatter is structured data** — Treat fields as queryable (like SQL columns)
3. **Markdown body has rich content** — ## Divisi and ## Program sections are parsed
4. **No external dependencies** — YAML parsing is done with regex/string operations
5. **Static output** — Generated HTML is fully independent, no build needed at runtime

## Page Rendering

### Index Page

Shows all Production projects in chronological order with:
- Project title
- Year
- Status badge (Completed/On Going/Cancelled)
- Excerpt
- "View Project" button

### Project Detail Pages

**Tab 1: Description**
- Project description text
- Concert dates with location names and addresses

**Tab 2: Schedule**
- List of all agenda items (rehearsals and concerts)
- Layout: Date | Details | Location (right side)
- Details: Type, time
- Program section from agenda markdown
- Location with address

**Tab 3: Music**
- Repertoire in order
- Each item: Number | Title | Composer | Score Link
- Score URL is a button linking to PDF

**Tab 4: Divisi**
- Each piece: Number, title, composer
- Divisi table (Staff | Voice Type) extracted from repertoire markdown
- "No divisi information available" if not present

## Customization

### Layout Templates

Files in `layout/` are markdown templates that control page structure:
- Edit to change colors, spacing, structure
- Variables like `{project_name}` are placeholder examples
- Run `generate.py` after editing to apply changes

### CSS Styling

`html/css/style.css` controls all visual design:
- **Cards** — Project listing
- **Tabs** — Tab buttons and content areas
- **Schedule items** — Layout with date, details, location
- **Tables** — Divisi tables
- **Links** — Score buttons, back navigation
- **Responsive** — Mobile-first design with media queries

Key classes:
- `.project-card` — Project listing cards
- `.tab-btn`, `.tab-content` — Tab navigation
- `.schedule-item` — Agenda list item
- `.divisi-table` — Voice assignment table
- `.score-link` — Score PDF button

## Development Guidelines

### Adding Features

1. **New tab type** — Add button in `generate_project_html()`, extract data, render section
2. **New data field** — Load from database in `main()`, pass to render functions
3. **Layout change** — Edit `layout/` templates and `html/css/style.css`

### Debugging

- **Check YAML parsing** — Print `parse_yaml()` output to verify field extraction
- **Verify relationships** — Ensure UUID references are correct in database
- **Test file paths** — Use `DB_PATH / 'table' / '*.md'` glob patterns
- **Check HTML generation** — Inspect generated HTML for correct variable substitution

### Performance

- Build time is typically <1 second
- No caching needed since builds are clean each time
- All operations are I/O bound (file reads), not CPU intensive

## Complete Workflow: Database to Website

### Step-by-Step Process

**1. Edit Database Entries**
```
In ../music-projects-database repo:
- Modify composers/ entries
- Update music/ entries with scores
- Edit repertoire/ to add divisi tables
- Update agenda/ rehearsals/concerts
- Edit locations/ venue details
```

**2. Generate Static Website**
```bash
# From music-projects-website directory
python3 generate.py
# ✓ Reads from ../music-projects-database
# ✓ Filters Production projects by UUID
# ✓ Resolves all UUID relationships
# ✓ Parses divisi from markdown
# ✓ Generates html/ folder
```

**3. Review Locally**
```bash
# Open in browser
open html/index.html

# Check all 40 projects display
# Verify all 4 tabs work (Description, Schedule, Music, Divisi)
# Test responsive design
```

**4. Commit to Git**
```bash
git add html/
git commit -m "Update music projects website (Production batch)"
git push origin main
```

**5. GitHub Actions Deploys**
- Automatically triggered by push to main
- Deploys html/ to gh-pages branch
- Site updates at projects.enricoruggieri.com (if DNS configured)
- No manual deployment steps needed

### When to Rebuild

Run `python3 generate.py` when:
- Adding a new project to the database
- Updating project details (title, description, year, status)
- Adding/modifying rehearsals or concerts
- Adding/updating repertoire pieces
- Adding divisi information
- Updating scores or composer names
- Adding locations or changing addresses

### Directory Isolation

Keep two repos separate:
- **music-projects-database**: Source data (all projects, all composers, all music)
- **music-projects-website**: Generated website (all projects rendered as static HTML)

The website repo does NOT contain database files. It only contains:
- generate.py (build script)
- html/ (generated output)
- layout/ (markdown templates)
- .github/workflows/ (deployment automation)

## Testing

### Validation Before Deploy

```bash
python3 generate.py
# Check:
# - No errors during generation
# - All Production projects generated
# - All links work (open html/index.html)
# - Responsive design works on mobile/tablet/desktop
# - All tabs load content
```

### Manual Checks

- [ ] Homepage shows all 40 projects in alphabetical order
- [ ] Clicking project opens detail page
- [ ] All 4 tabs are present and functional
- [ ] Description tab shows concerts with locations
- [ ] Schedule tab shows location on the right
- [ ] Music tab shows score links (where available)
- [ ] Divisi tab shows composer names and tables
- [ ] Back button returns to homepage

## Deployment

### GitHub Pages (Current Setup)

The deployment pipeline is fully automated via GitHub Actions.

**Workflow File**: `.github/workflows/build-and-deploy.yml`

**How it works**:
1. Edit database in `../music-projects-database`
2. Run `python3 generate.py` locally to generate HTML
3. Stage and commit: `git add html/` → `git commit -m "..."`
4. Push to main: `git push origin main`
5. GitHub Actions automatically:
   - Checks out the repo
   - Deploys `./html` folder to gh-pages branch
   - Updates CNAME: `projects.enricoruggieri.com`

**Result**:
- Site live at: https://projects.enricoruggieri.com (after DNS setup)
- Temporary GitHub URL: https://enrico-laboratory.github.io/music-projects-website/

**Manual Setup Steps** (already complete):
- Created gh-pages branch with initial HTML content
- Configured GitHub Pages in repo settings (Source: gh-pages branch, root folder)
- Added CNAME entry pointing to enrico-laboratory.github.io

### DNS Configuration

To use the custom domain `projects.enricoruggieri.com`:
1. Point DNS CNAME record to `enrico-laboratory.github.io`
2. GitHub will automatically validate and enable HTTPS

### Alternative Deployment

**Netlify/Vercel**: Connect repo, set build command to `python3 generate.py`, publish `html/` folder.

---

**Last updated**: 2026-04-30
**Build system**: Python 3.14+
**External dependencies**: None
**Generated output**: 40 project pages + 1 index page
**Deployment**: GitHub Actions + GitHub Pages (gh-pages branch)
**Scope**: All music projects from database (full production website)

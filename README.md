# Music Projects Website

A static website generator that publishes music project information from the music-projects-database workspace.

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

## Deployment

The `html/` folder is ready for static hosting:

- **GitHub Pages** — Push `html/` to `gh-pages` branch
- **Netlify** — Connect repo, set build command to `python3 generate.py`, publish folder to `html/`
- **Vercel** — Similar setup as Netlify
- **Any static host** — Upload contents of `html/` folder

## POC Status

Current build includes 3 proof-of-concept projects:
- Festa (2022, 45 rehearsals, 26 music pieces)
- A day with Arianna (2024, 1 concert, 4 music pieces)
- Echos of Venice (2027, 5 rehearsals, 13 music pieces)

To add more projects, modify `POC_PROJECTS` list in `generate.py` and regenerate.

---

For agent development, see **[CLAUDE.md](./CLAUDE.md)**.

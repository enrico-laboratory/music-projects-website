#!/usr/bin/env python3

import re
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / 'music-projects-database'
HTML_PATH = Path(__file__).parent / 'html'
PROJECTS_PATH = HTML_PATH / 'projects'

def parse_yaml(content):
    """Simple YAML parser for frontmatter."""
    data = {}
    if not content.startswith('---'):
        return data

    parts = content.split('---', 2)
    if len(parts) < 3:
        return data

    for line in parts[1].split('\n'):
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()

        # Clean quotes
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        data[key] = value

    return data

def load_entries(table_name):
    """Load all entries from a table."""
    entries = {}
    table_path = DB_PATH / table_name

    if not table_path.exists():
        return entries

    for file in table_path.glob('*.md'):
        content = file.read_text(encoding='utf-8')
        data = parse_yaml(content)
        if 'uuid' in data:
            entries[data['uuid']] = data

    return entries

def get_composer_name(composer_id, composers):
    """Get composer name from UUID."""
    if composer_id in composers:
        return composers[composer_id].get('name', 'Unknown Composer')
    return 'Unknown Composer'

def format_date(iso_date):
    """Format ISO date to readable format."""
    try:
        clean_date = iso_date.split('+')[0].split('Z')[0]
        dt = datetime.fromisoformat(clean_date)
        return dt.strftime('%b %d, %Y')
    except:
        return iso_date[:10]

def format_time(iso_date):
    """Extract time from ISO date."""
    try:
        clean_date = iso_date.split('+')[0].split('Z')[0]
        dt = datetime.fromisoformat(clean_date)
        return dt.strftime('%H:%M')
    except:
        return ''

def extract_program(file_path):
    """Extract program section from agenda markdown."""
    try:
        content = file_path.read_text(encoding='utf-8')
        if '## Program' in content:
            program_start = content.find('## Program')
            program_section = content[program_start + 10:]
            program_end = program_section.find('## ')
            if program_end != -1:
                return program_section[:program_end].strip()
            return program_section.strip()
    except:
        pass
    return None

def get_location_details(location_uuid, locations):
    """Get location name and address."""
    if location_uuid in locations:
        loc = locations[location_uuid]
        name = loc.get('location', 'Unknown')
        address = loc.get('address', '')
        city = loc.get('city', '')
        full_address = f"{address}, {city}" if address and city else (address or city or '')
        return name, full_address
    return None, None

def get_project_agenda(project_uuid, agenda_entries):
    """Get agenda items for a project."""
    items = []
    for uid, item in agenda_entries.items():
        if item.get('music_project_id') == project_uuid:
            items.append(item)

    items.sort(key=lambda x: x.get('do_date', '9999-12-31'))
    return items

def parse_divisi_table(markdown_text):
    """Parse markdown table to HTML table."""
    lines = markdown_text.strip().split('\n')
    if len(lines) < 3:
        return None

    rows = []
    for line in lines:
        if line.startswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if cells and cells[0]:  # Skip empty lines
                rows.append(cells)

    if len(rows) < 2:
        return None

    # First row is header, skip separator
    headers = rows[0]
    data_rows = rows[2:] if len(rows) > 2 else []

    if not data_rows:
        return None

    html = '<table><thead><tr>'
    for header in headers:
        html += f'<th>{header}</th>'
    html += '</tr></thead><tbody>'

    for row in data_rows:
        html += '<tr>'
        for cell in row:
            html += f'<td>{cell}</td>'
        html += '</tr>'

    html += '</tbody></table>'
    return html

def extract_divisi_html(file_path):
    """Extract divisi table from repertoire file and convert to HTML."""
    try:
        content = file_path.read_text(encoding='utf-8')
        if '## Divisi' in content:
            divisi_start = content.find('## Divisi')
            divisi_section = content[divisi_start + 9:]  # Skip '## Divisi'
            divisi_end = divisi_section.find('\n## ')
            if divisi_end != -1:
                divisi_text = divisi_section[:divisi_end]
            else:
                divisi_text = divisi_section

            return parse_divisi_table(divisi_text)
    except:
        pass
    return None

def get_project_repertoire(project_uuid, repertoire_entries, music_entries):
    """Get repertoire items for a project with music details."""
    items = []
    for uid, rep in repertoire_entries.items():
        if rep.get('music_project_id') == project_uuid:
            music_id = rep.get('music_id')
            if music_id in music_entries:
                music = music_entries[music_id]
                rep['music_title'] = music.get('music', 'Unknown')
                rep['composer_id'] = music.get('composer_id')
                rep['voices'] = music.get('voices')
            items.append(rep)

    items.sort(key=lambda x: int(x.get('order', '999')))
    return items

def generate_index_html(projects):
    """Generate the index page."""
    projects_sorted = sorted(projects, key=lambda x: int(x.get('year', '0')))

    cards = ''
    for proj in projects_sorted:
        status_class = proj.get('status', 'unknown').lower().replace(' ', '-')
        cards += f'''        <div class="project-card {status_class}">
          <div class="project-header">
            <h2><a href="projects/{proj['filename']}.html">{proj.get('title', 'Untitled')}</a></h2>
            <span class="year">{proj.get('year', 'N/A')}</span>
          </div>
          <p class="status">{proj.get('status', 'Unknown')}</p>
          <p class="excerpt">{proj.get('excerpt', 'No description available')}</p>
          <a href="projects/{proj['filename']}.html" class="btn">View Project</a>
        </div>
'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Music Projects</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <div class="container">
    <header>
      <h1>Music Projects</h1>
      <p>A collection of music projects and performances</p>
    </header>

    <main>
      <div class="projects-grid">
{cards}      </div>
    </main>

    <footer>
      <p>&copy; 2026 Enrico Ruggieri. Music Projects</p>
    </footer>
  </div>
</body>
</html>'''
    return html

def generate_project_html(project, agenda_items, repertoire_items, composers, locations, music_entries):
    """Generate a project detail page."""
    project_name = project.get('title', 'Untitled')

    # Concert items with locations
    concerts = [a for a in agenda_items if a.get('type') == 'Concert']
    concert_html = ''
    if concerts:
        concert_html = '<h3>Concert Dates</h3>\n<ul class="dates-list">'
        for concert in concerts:
            date = format_date(concert.get('do_date', ''))
            location_id = concert.get('location_id')
            location_name, location_addr = get_location_details(location_id, locations)
            location_str = f'<br/><em>{location_name}</em>' if location_name else ''
            if location_addr:
                location_str += f'<br/><small>{location_addr}</small>'
            concert_html += f'<li><strong>{concert.get("type", "Concert")}</strong> - {date}{location_str}</li>'
        concert_html += '</ul>'

    # Schedule list with location and program
    schedule_html = ''
    if agenda_items:
        schedule_html = '<div class="schedule-list">'
        for item in agenda_items:
            date = format_date(item.get('do_date', ''))
            time = format_time(item.get('do_date', ''))
            item_type = item.get('type', 'Unknown').lower()
            time_str = f' - {time}' if time else ''

            # Get location
            location_id = item.get('location_id')
            location_name, location_addr = get_location_details(location_id, locations)
            location_html = ''
            if location_name:
                location_html += f'<p class="location"><strong>📍 {location_name}</strong>'
                if location_addr:
                    location_html += f'<br/><small>{location_addr}</small>'
                location_html += '</p>'

            # Get program
            program_html = ''
            item_uuid = item.get('uuid')
            if item_uuid:
                for f in (DB_PATH / 'agenda').glob('*.md'):
                    if parse_yaml(f.read_text()).get('uuid') == item_uuid:
                        program = extract_program(f)
                        if program:
                            program_html = f'<p class="program"><strong>Program:</strong><br/>{program}</p>'
                        break

            schedule_html += f'''            <div class="schedule-item {item_type}">
              <div class="schedule-date">{date}</div>
              <div class="schedule-details">
                <h4>{item.get("type", "Unknown")}</h4>
                <p class="type">{item.get("type", "Unknown")}{time_str}</p>
                {program_html}
              </div>
              <div class="schedule-location">
                {location_html}
              </div>
            </div>
'''
        schedule_html += '</div>'

    # Music list with score links
    music_html = ''
    if repertoire_items:
        music_html = '<div class="music-list">'
        for rep in repertoire_items:
            order = rep.get('order', '?')
            title = rep.get('music_title', 'Unknown Piece')
            composer_id = rep.get('composer_id')
            composer = get_composer_name(composer_id, composers) if composer_id else 'Unknown'

            # Get score URL from music entry
            music_id = rep.get('music_id')
            score_url = ''
            if music_id and music_id in music_entries:
                score_url = music_entries[music_id].get('score_url')

            score_link = f'<p class="score-link"><a href="{score_url}" target="_blank">📄 View Score</a></p>' if score_url else ''

            music_html += f'''            <div class="music-item">
              <span class="order">{order}</span>
              <div class="music-info">
                <h4>{title}</h4>
                <p class="composer">{composer}</p>
                {score_link}
              </div>
            </div>
'''
        music_html += '</div>'

    # Divisi list with composer
    divisi_html = ''
    if repertoire_items:
        divisi_html = '<div class="divisi-list">'
        for rep in repertoire_items:
            order = rep.get('order', '?')
            title = rep.get('music_title', 'Unknown Piece')
            composer_id = rep.get('composer_id')
            composer = get_composer_name(composer_id, composers) if composer_id else 'Unknown'

            # Find divisi table from repertoire file
            divisi_table_html = None
            rep_uuid = rep.get('uuid')
            if rep_uuid:
                for f in (DB_PATH / 'repertoire').glob('*.md'):
                    if parse_yaml(f.read_text()).get('uuid') == rep_uuid:
                        divisi_table_html = extract_divisi_html(f)
                        break

            divisi_html += f'''            <div class="divisi-item">
              <div class="divisi-header">
                <h4>{order}. {title}</h4>
                <p class="composer">{composer}</p>
              </div>
'''
            if divisi_table_html:
                divisi_html += f'<div class="divisi-table">{divisi_table_html}</div>'
            else:
                divisi_html += '<p class="no-divisi">No divisi information available.</p>'

            divisi_html += '''            </div>
'''
        divisi_html += '</div>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} - Music Projects</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="container">
    <header>
      <a href="../index.html" class="back-link">← Back to Projects</a>
      <h1>{project_name}</h1>
      <div class="project-meta">
        <span class="year">Year: {project.get('year', 'N/A')}</span>
        <span class="status">{project.get('status', 'Unknown')}</span>
      </div>
    </header>

    <main>
      <div class="tabs">
        <div class="tab-buttons">
          <button class="tab-btn active" onclick="showTab(event, 'description')">Description</button>
          <button class="tab-btn" onclick="showTab(event, 'schedule')">Schedule</button>
          <button class="tab-btn" onclick="showTab(event, 'music')">Music</button>
          <button class="tab-btn" onclick="showTab(event, 'divisi')">Divisi</button>
        </div>

        <div id="description" class="tab-content active">
          <h2>Project Description</h2>
          <p>{project.get('description', 'No description available.')}</p>
          {concert_html}
        </div>

        <div id="schedule" class="tab-content">
          <h2>Rehearsals & Concerts</h2>
          {schedule_html if schedule_html else '<p>No schedule items available.</p>'}
        </div>

        <div id="music" class="tab-content">
          <h2>Music Repertoire</h2>
          {music_html if music_html else '<p>No music pieces assigned to this project.</p>'}
        </div>

        <div id="divisi" class="tab-content">
          <h2>Voice Assignments</h2>
          {divisi_html if divisi_html else '<p>No voice assignments available.</p>'}
        </div>
      </div>
    </main>

    <footer>
      <p>&copy; 2026 Enrico Ruggieri. Music Projects</p>
    </footer>
  </div>

  <script>
    function showTab(evt, tabName) {{
      const contents = document.querySelectorAll('.tab-content');
      contents.forEach(content => content.classList.remove('active'));

      const buttons = document.querySelectorAll('.tab-btn');
      buttons.forEach(button => button.classList.remove('active'));

      document.getElementById(tabName).classList.add('active');
      evt.currentTarget.classList.add('active');
    }}
  </script>
</body>
</html>'''
    return html

def main():
    print('Loading database...')
    projects = load_entries('music-projects')
    agenda = load_entries('agenda')
    repertoire = load_entries('repertoire')
    music = load_entries('music')
    composers = load_entries('composers')
    locations = load_entries('locations')

    # POC projects
    poc_uuids = {
        '1f455d91-01a7-4d64-a4b9-84bd22c8155e': 'a-day-with-arianna',
        'aeed0ea2-ed36-4e12-b17a-b1f155ecf38c': 'festa',
        '32897f66-5e26-80eb-b724-ed78d2e0266f': 'echos-of-venice'
    }

    poc_projects = []
    for uuid, filename in poc_uuids.items():
        if uuid in projects:
            proj = projects[uuid].copy()
            proj['filename'] = filename
            poc_projects.append(proj)

    # Create output directory
    PROJECTS_PATH.mkdir(parents=True, exist_ok=True)

    print(f'Generating {len(poc_projects)} project pages...')

    # Generate index
    index_html = generate_index_html(poc_projects)
    (HTML_PATH / 'index.html').write_text(index_html)
    print('✓ Generated index.html')

    # Generate project pages
    for proj in poc_projects:
        uuid = [k for k, v in poc_uuids.items() if v == proj['filename']][0]
        proj_agenda = get_project_agenda(uuid, agenda)
        proj_repertoire = get_project_repertoire(uuid, repertoire, music)

        html = generate_project_html(proj, proj_agenda, proj_repertoire, composers, locations, music)
        (PROJECTS_PATH / f"{proj['filename']}.html").write_text(html)
        print(f"✓ Generated {proj['filename']}.html ({len(proj_agenda)} agenda, {len(proj_repertoire)} music)")

    print('\nDone! Open html/index.html to view.')

if __name__ == '__main__':
    main()

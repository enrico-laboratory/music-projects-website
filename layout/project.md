# Project Detail Page Layout

This markdown file shows the structure of individual project pages. Edit this to customize how project details are displayed.

## Structure

Each project page has:
- Header with project title, year, status
- Four tabs: Description, Schedule, Music, Divisi
- Footer

## Tabs

### Tab 1: Description
- Project description text
- Concert dates list with locations and addresses

CSS Classes:
```
#description             Tab content area
.dates-list             List of concerts
  li                    Each concert entry
    em                  Location name
    small               Address
```

### Tab 2: Schedule
- Rehearsals and concerts in chronological order
- Layout: Date | Details | Location (right side)

CSS Classes:
```
#schedule               Tab content area
.schedule-list          Container for items
.schedule-item          Individual event
  .schedule-date        Date column (left)
  .schedule-details     Event info (middle)
    h4                  Event type
    .type               Type and time
    .program            Program details
  .schedule-location    Location column (right)
    .location           Venue name and address
```

Item types (for styling):
- `.rehearsal` — Orange left border
- `.concert` — Red left border
- `.meeting` — Purple left border

### Tab 3: Music
- Repertoire list in performance order
- Each piece shows: Number | Title | Composer | Score Link

CSS Classes:
```
#music                  Tab content area
.music-list            Container for items
.music-item            Individual piece
  .order                Piece number
  .music-info           Piece details
    h4                  Title
    .composer           Composer name (italic)
    .score-link         Score PDF button
      a                 Link to score
```

### Tab 4: Divisi
- Voice assignments for each piece
- Includes composer name and divisi table

CSS Classes:
```
#divisi                 Tab content area
.divisi-list           Container for items
.divisi-item           Individual piece
  .divisi-header       Title and composer
  .divisi-table        Voice assignment table
    table               HTML table with Staff | Voice columns
```

## Tab Navigation

```
.tab-buttons            Button container
  .tab-btn              Individual tab button
    .active             Currently selected tab

Behavior: Clicking button shows corresponding .tab-content with matching ID
```

## Customization Examples

### Change tab layout
```css
/* Make tabs horizontal instead of vertical */
.tab-buttons {
  flex-direction: row;
  flex-wrap: wrap;
}

.tab-btn {
  flex: 1;
  min-width: 150px;
}
```

### Style schedule location differently
```css
.schedule-location {
  background: #f0f0f0;
  padding: 1rem;
  border-radius: 4px;
  text-align: right;
}
```

### Change divisi table colors
```css
.divisi-table table {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.divisi-table table th {
  background: rgba(0, 0, 0, 0.2);
}
```

### Make score links bigger
```css
.score-link a {
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
}
```

## Data Variables

The `generate.py` script injects these values:

```python
{project_name}          Project title
{project.get('year')}   Year
{project.get('status')} Status (Completed, On Going, Cancelled)
{project.get('description')}  Description text

# Concerts
{date}                  Formatted concert date
{location_name}         Venue name
{location_addr}         Full address

# Schedule items
{item.get('type')}      Event type (Rehearsal, Concert)
{time_str}              Start time
{program_html}          Program details from ## Program section

# Music
{title}                 Piece title
{composer}              Composer name
{score_url}             Link to PDF

# Divisi
{divisi_table_html}     HTML table from ## Divisi section
```

## Output

The `generate.py` script renders each project as `html/projects/{uuid}.html` with live data and this layout.

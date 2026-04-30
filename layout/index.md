# Homepage Layout

This markdown file shows the structure of the index page. Edit this to customize the homepage appearance.

## Structure

The homepage displays a grid of project cards, each showing:
- Project title (linked to detail page)
- Year
- Status badge
- Excerpt/description
- "View Project" button

## CSS Classes Available

```
.container              Main container with max-width
.header                 Page header with title
.projects-grid          Grid layout for project cards
.project-card           Individual project card
  .project-header       Title and year
  .status               Status badge
  .excerpt              Project description
.btn                    "View Project" button
```

## Status Classes

Projects are styled with status-specific classes:
- `.completed` — Green theme
- `.on-going` — Orange theme
- `.cancelled` — Red theme

## Customization

To modify this page:

1. Edit text in the header section (title, subtitle)
2. Change `.projects-grid` styling in `css/style.css` for layout changes
3. Modify `.project-card` styles for card appearance
4. Adjust `.btn` for button styling

Example CSS customizations:
```css
/* Change grid columns */
.projects-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

/* Customize card appearance */
.project-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
```

## Output

The `generate.py` script renders this as `html/index.html` with live project data.

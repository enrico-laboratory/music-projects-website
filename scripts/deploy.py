#!/usr/bin/env python3
"""
MPW Deployment Script

Usage:
  python3 scripts/deploy.py          # Full deployment (build + deploy to gh-pages)
  python3 scripts/deploy.py test     # Local test only (build + open in browser)
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(cmd, description):
    """Execute a shell command and handle errors."""
    print(f"\n▶️  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=Path(__file__).parent.parent)
        print(f"✅ {description} complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        sys.exit(1)


def build_website():
    """Build the website by running generate.py"""
    run_command("python3 scripts/generate.py", "Building website")


def test_locally():
    """Test the website locally by opening in browser."""
    build_website()
    html_path = Path(__file__).parent.parent / "html" / "index.html"
    if html_path.exists():
        print(f"\n▶️  Opening website in browser...")
        subprocess.run(f"open {html_path}", shell=True)
        print(f"✅ Website opened at {html_path}")
        print("\n📋 Manual checks:")
        print("  - [ ] Homepage shows all projects in alphabetical order")
        print("  - [ ] Clicking project opens detail page")
        print("  - [ ] All 4 tabs are present and functional")
        print("  - [ ] Description tab shows concerts with locations")
        print("  - [ ] Schedule tab shows location on the right")
        print("  - [ ] Music tab shows score links")
        print("  - [ ] Divisi tab shows composer names and tables")
        print("  - [ ] Back button returns to homepage")
    else:
        print(f"❌ Generated html/index.html not found at {html_path}")
        sys.exit(1)


def deploy_to_gh_pages():
    """Deploy the website to the gh-pages branch."""
    print("\n" + "=" * 60)
    print("DEPLOYING TO GITHUB PAGES")
    print("=" * 60)

    # Backup generated HTML
    run_command("mkdir -p /tmp/mpw-backup && cp -r html/* /tmp/mpw-backup/", "Backing up generated HTML")

    # Checkout gh-pages and clean it
    run_command("git checkout gh-pages", "Checking out gh-pages branch")
    run_command("git reset --hard", "Hard reset gh-pages")
    run_command("git clean -fd", "Cleaning gh-pages")

    # Copy new HTML and deploy
    run_command("cp -r /tmp/mpw-backup/* .", "Copying generated HTML to gh-pages")
    run_command("git add .", "Staging all changes")
    run_command('git commit -m "Deploy: Update Music Projects Website"', "Committing deployment")
    run_command("git push origin gh-pages --force", "Pushing to gh-pages (force)")

    # Return to main
    run_command("git checkout main", "Returning to main branch")

    print("\n" + "=" * 60)
    print("✅ DEPLOYMENT COMPLETE")
    print("=" * 60)
    print("\n🌐 Website is live!")
    print("   - GitHub Pages: https://enrico-laboratory.github.io/music-projects-website/")
    print("   - Custom domain: https://projects.enricoruggieri.com (if configured)")


def main():
    """Main entry point."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "deploy"

    if mode == "test":
        print("🧪 LOCAL TEST MODE")
        test_locally()
    elif mode == "deploy" or mode == "":
        print("🚀 FULL DEPLOYMENT MODE")
        build_website()
        deploy_to_gh_pages()
    else:
        print(f"❌ Unknown mode: {mode}")
        print("\nUsage:")
        print("  python3 scripts/deploy.py          # Full deployment")
        print("  python3 scripts/deploy.py test     # Local test only")
        sys.exit(1)


if __name__ == "__main__":
    main()

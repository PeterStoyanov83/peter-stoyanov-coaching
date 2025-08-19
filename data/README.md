# Database Directory

This directory contains the SQLite database for the coaching site.

## Files:
- `coaching_site.db` - Main SQLite database (auto-created)
- `coaching_site_backup_*.db` - Backup files (if any)

## Security:
- Database contains subscriber emails and personal information
- **Never commit the actual database file to version control**
- Only this README file should be tracked in git

## Local Development:
The database is automatically created when you first run the backend application.

## Production:
In GitHub Codespaces, this directory will contain the persistent database.
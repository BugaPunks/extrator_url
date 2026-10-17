# txt-export Specification

## Purpose
TBD - created by archiving change web-app-youtube-extractor. Update Purpose after archive.
## Requirements
### Requirement: Export a single txt file
The system SHALL generate a single `.txt` file containing all extracted URLs, one per line, downloadable from the browser.

#### Scenario: Single file download
- **WHEN** the user clicks "Descargar .txt único"
- **THEN** the browser downloads a `.txt` file with one URL per line

### Requirement: Export split txt files
The system SHALL support splitting the export into multiple `.txt` files when a maximum number of URLs per file is configured (value > 0). Files SHALL be named `urls_videos_parte_1.txt`, `urls_videos_parte_2.txt`, etc., each containing the configured maximum number of URLs except the last one.

#### Scenario: Split with maximum per file
- **WHEN** the user configures "Máx. URLs por archivo" = 100 and the channel has 250 URLs
- **THEN** the system generates `urls_videos_parte_1.txt` and `urls_videos_parte_2.txt` with 100 URLs each, and `urls_videos_parte_3.txt` with 50 URLs

#### Scenario: Download of multiple split files
- **WHEN** the export generates more than one file
- **THEN** the browser downloads all files as a single ZIP archive

### Requirement: Line format respects titles option
The system SHALL format each line as `URL` when titles are disabled, or `Título - URL` when titles are enabled, matching the option used during extraction.

#### Scenario: Format with titles
- **WHEN** the extraction was done with titles enabled and the user exports
- **THEN** each line in the exported file(s) has the format `Título - URL`

#### Scenario: Format without titles
- **WHEN** the extraction was done with titles disabled and the user exports
- **THEN** each line in the exported file(s) contains only the URL


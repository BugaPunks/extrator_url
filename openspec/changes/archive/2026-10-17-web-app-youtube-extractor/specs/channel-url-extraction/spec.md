## ADDED Requirements

### Requirement: Extract video list from a YouTube channel
The system SHALL accept a YouTube channel URL or handle (e.g. `@tucanal`, `https://www.youtube.com/@tucanal`) and return the flat list of videos of that channel using `yt-dlp` with `extract_flat: True`.

#### Scenario: Extraction by handle
- **WHEN** the user submits `@tucanal` as the channel
- **THEN** the system normalizes it to `https://www.youtube.com/@tucanal/videos` and returns the list of videos of the channel

#### Scenario: Extraction by full URL
- **WHEN** the user submits `https://www.youtube.com/@tucanal`
- **THEN** the system appends `/videos` if missing and returns the list of videos of the channel

### Requirement: Include titles option
The system SHALL support an option to include video titles along with URLs. When disabled (default), only URLs are returned; when enabled, each entry includes the video title and URL.

#### Scenario: Titles disabled (default)
- **WHEN** the user extracts without enabling titles
- **THEN** each result entry contains only the video URL

#### Scenario: Titles enabled
- **WHEN** the user enables "Incluir títulos de videos"
- **THEN** each result entry contains the video title and its URL

### Requirement: Tolerate unavailable videos
The system SHALL continue extraction when individual videos are private, deleted, or unavailable, omitting them from the results without aborting the process.

#### Scenario: Private or deleted video in the channel
- **WHEN** the channel listing contains private or deleted videos
- **THEN** those videos are skipped, the remaining videos are returned, and the extraction completes

### Requirement: Report extraction errors
The system SHALL return a user-facing error when the channel does not exist, the URL is invalid, or the extraction fails due to network problems.

#### Scenario: Invalid or nonexistent channel
- **WHEN** the user submits a URL or handle that does not correspond to an existing channel
- **THEN** the system returns an error message and no results

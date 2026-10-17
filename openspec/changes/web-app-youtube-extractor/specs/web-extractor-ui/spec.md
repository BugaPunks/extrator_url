## ADDED Requirements

### Requirement: Extraction form
The system SHALL provide a main page with a form containing: a text input for the channel URL/handle, a checkbox "Incluir títulos de videos" (unchecked by default), a numeric input "Máx. URLs por archivo" (optional), and a submit button "Extraer URLs".

#### Scenario: Page load
- **WHEN** the user opens the main page
- **THEN** the form is displayed with the titles checkbox unchecked and the numeric input empty

#### Scenario: Submit extraction
- **WHEN** the user fills the channel input and clicks "Extraer URLs"
- **THEN** the system sends the request and displays the extracted URLs in the results area

### Requirement: Loading state during extraction
The system SHALL display a loading indicator with a progress message ("Obteniendo lista de videos...") and disable the form buttons while extraction is in progress.

#### Scenario: Extraction in progress
- **WHEN** an extraction request is running
- **THEN** a loading indicator is shown and the buttons are disabled until the response arrives

### Requirement: Read-only results area
The system SHALL display the extracted results in a read-only textarea, showing URLs only or titles plus URLs according to the option used.

#### Scenario: Results displayed
- **WHEN** an extraction completes successfully
- **THEN** the results area shows the extracted URLs (and titles if enabled) in read-only mode

### Requirement: Friendly error display
The system SHALL display user-friendly error messages in the UI when extraction or export fails (invalid channel, no videos, network error), without showing stack traces.

#### Scenario: Extraction fails
- **WHEN** the extraction request returns an error
- **THEN** the UI shows a friendly error message and no results

### Requirement: Responsive layout
The UI SHALL be responsive, rendering correctly on desktop and mobile viewports.

#### Scenario: Mobile viewport
- **WHEN** the page is opened on a mobile-sized viewport
- **THEN** the form, results area, and buttons are usable and correctly laid out

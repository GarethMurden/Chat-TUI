from textual.theme import Theme

arasaka_theme = Theme(
    name="arasaka",
    primary="#D00000",          # Arasaka red
    secondary="#8B0000",        # Dark red
    accent="#FF4040",           # Bright warning red
    foreground="#F0F0F0",       # Near-white text
    background="#0A0A0A",       # Deep black
    success="#00C853",          # Corporate green
    warning="#FFB300",          # Amber warning
    error="#FF1744",            # Critical red
    surface="#141414",          # Raised surfaces
    panel="#1F1F1F",            # Panels/dialogs
    dark=True,
    variables={
        # Cursor
        "block-cursor-text-style": "bold",

        # Footer
        "footer-key-foreground": "#D00000",
        "footer-key-background": "#0A0A0A",

        # Inputs
        "input-selection-background": "#D00000 40%",
        "input-cursor-background": "#D00000",

        # Borders
        "border": "#D00000",
        "border-blurred": "#550000",

        # Focus states
        "button-focus-text-style": "bold",
        "button-focus-background": "#D00000",

        # Data tables
        "datatable-hover-background": "#220000",
        "datatable-cursor-background": "#330000",

        # Links
        "link-color": "#FF4040",
    },
)

night_city_theme = Theme(
    name="night_city",
    primary="#FCEE09",          # HUD cyan
    secondary="#00F0FF",        # Brand yellow
    accent="#FF3D9A",           # Hot pink accents
    foreground="#E8FFFF",
    background="#0D0D12",
    success="#00FF85",
    warning="#FCEE09",
    error="#FF5555",
    surface="#151520",
    panel="#1C1C2A",
    dark=True,
    variables={
        "footer-key-foreground": "#FCEE09",
        "input-selection-background": "#00F0FF 35%",
        "link-color": "#00F0FF",
        "border": "#FCEE09",
        "border-title-color": "#FCEE09",
        "header-background": "#0D0D12",
        "header-color": "#FCEE09",
    },
)

decker_theme = Theme(
    name="decker",
    primary="#FF4FD8",
    secondary="#00CFFF",
    accent="#FF8A00",
    foreground="#E0E6FF",
    background="#0A0C14",
    success="#00FF88",
    warning="#FFC107",
    error="#FF4D6D",
    surface="#121827",
    panel="#1B2233",
    dark=True,
    variables={
        "footer-key-foreground": "#00CFFF",
        "input-selection-background": "#FF4FD8 20%",
        "link-color": "#00CFFF",
        "border": "#FF4FD8",
        "border-title-color": "#FF8A00",
        "header-color": "#FF4FD8",
    },
)

kusanagi_theme = Theme(
    name="kusanagi",
    primary="#4DD0E1",
    secondary="#80DEEA",
    accent="#00E5FF",
    foreground="#D8F3FF",
    background="#071018",
    success="#00E676",
    warning="#FFD54F",
    error="#FF5252",
    surface="#0D1B2A",
    panel="#162330",
    dark=True,
    variables={
        "footer-key-foreground": "#00E5FF",
        "input-selection-background": "#00E5FF 25%",
        "link-color": "#4DD0E1",
        "border": "#4DD0E1",
        "border-title-color": "#80DEEA",
    },
)

lcars_theme = Theme(
    name="lcars",
    primary="#FF9900",          # LCARS orange
    secondary="#CC99FF",        # LCARS lavender
    accent="#FFCC66",           # Light orange highlight
    foreground="#F5F5F5",       # Off-white text
    background="#000000",       # Deep black
    success="#66CC99",          # Muted green
    warning="#FFCC00",          # Alert yellow
    error="#FF6666",            # Alert red
    surface="#1A1A1A",          # Raised surface
    panel="#2A2A2A",            # Dialog and panel bg
    dark=True,
    variables={
        # Header/Footer
        "header-background": "#FF9900",
        "header-color": "#000000",
        "footer-key-foreground": "#000000",
        "footer-key-background": "#FFCC66",

        # Input widgets
        "input-selection-background": "#CC99FF 40%",
        "input-cursor-background": "#FF9900",

        # Borders
        "border": "#FF9900",
        "border-title-color": "#CC99FF",

        # Buttons
        "button-focus-background": "#FF9900",
        "button-focus-color": "#000000",

        # Tables
        "datatable-hover-background": "#332200",
        "datatable-cursor-background": "#664400",

        # Links
        "link-color": "#CC99FF",
    },
)

pipboy_theme = Theme(
    name="pipboy",
    primary="#2AFF2A",          # Main phosphor green
    secondary="#1CCF1C",        # Darker green
    accent="#66FF66",           # Highlight green
    foreground="#AAFFAA",       # Terminal text
    background="#081008",       # Deep green-black
    success="#66FF66",
    warning="#D4FF00",          # Yellow-green warning
    error="#FF6666",
    surface="#0D160D",
    panel="#122012",
    dark=True,
    variables={
        # Header/Footer
        "header-background": "#081008",
        "header-color": "#2AFF2A",
        "footer-key-foreground": "#081008",
        "footer-key-background": "#2AFF2A",

        # Inputs
        "input-selection-background": "#2AFF2A 25%",
        "input-cursor-background": "#2AFF2A",

        # Borders
        "border": "#2AFF2A",
        "border-title-color": "#66FF66",

        # Buttons
        "button-focus-background": "#2AFF2A",
        "button-focus-color": "#081008",

        # Tables
        "datatable-hover-background": "#143014",
        "datatable-cursor-background": "#1D441D",

        # Links
        "link-color": "#66FF66",

        # Make it feel more terminal-like
        "block-cursor-text-style": "bold",
    },
)
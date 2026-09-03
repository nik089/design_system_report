"""
Comprehensive Technology Signatures for:
- 17 CSS Frameworks: Bootstrap, Tailwind CSS, Bulma, Foundation, Semantic UI, Materialize CSS,
  UIkit, Pure CSS, Pico CSS, W3.CSS, Spectre.css, Milligram, Skeleton CSS, Tachyons,
  Halfmoon, UnoCSS, Windi CSS.
- 40 Design Systems & UI Libraries: UX4G Design System, Angular Material, Material UI (MUI),
  Ant Design, PrimeNG, PrimeReact, PrimeVue, Chakra UI, Mantine, Carbon Design System,
  Fluent UI, PatternFly, Salesforce Lightning Design System, Atlassian Design System,
  Adobe Spectrum, Shopify Polaris, SAP Fiori, Oracle Redwood, GOV.UK Design System,
  USWDS, Clarity, Base Web, Evergreen UI, Grommet, Blueprint.js, Elastic UI, Kendo UI,
  Syncfusion, DevExtreme, Nebular, Taiga UI, NG-ZORRO, Vuetify, Quasar, Element Plus,
  Shoelace, Radix UI, HeroUI, React Bootstrap, and Custom Design Systems.
"""

CSS_FRAMEWORKS = {
    "Bootstrap": {
        "cdn_patterns": [
            r"bootstrap(?:\.bundle)?(?:\.min)?\.css",
            r"bootstrap(?:\.bundle)?(?:\.min)?\.js",
            r"/bootstrap/\d+\.\d+",
            r"cdn\.jsdelivr\.net/npm/bootstrap",
            r"cdnjs\.cloudflare\.com/ajax/libs/twitter-bootstrap",
            r"stackpath\.bootstrapcdn\.com/bootstrap",
            r"netdna\.bootstrapcdn\.com/bootstrap"
        ],
        "class_patterns": [
            r"^col-(?:xs|sm|md|lg|xl|xxl)-\d+$",
            r"^container(?:-fluid|-sm|-md|-lg|-xl|-xxl)?$",
            r"^row$",
            r"^d-(?:none|flex|inline-flex|block|inline-block|grid)$",
            r"^navbar(?:-(?:expand|brand|nav|toggler|collapse))?$",
            r"^card(?:-(?:body|title|text|header|footer))?$",
            r"^btn-(?:primary|secondary|success|danger|warning|info|light|dark|link|outline-[a-z]+)$",
            r"^modal(?:-(?:dialog|content|header|body|footer))?$",
            r"^badge(?:-pill)?$",
            r"^alert-(?:primary|secondary|success|danger|warning|info)$"
        ],
        "var_patterns": [
            r"^--bs-",
            r"^--bootstrap-"
        ],
        "attr_patterns": [
            r"data-bs-toggle",
            r"data-bs-target",
            r"data-bs-dismiss",
            r"data-bs-spy",
            r"data-bs-ride",
            r"data-toggle=\"(?:modal|dropdown|collapse|tooltip|popover|tab)\""
        ],
        "meta_patterns": [
            r"Bootstrap"
        ]
    },
    "Tailwind CSS": {
        "cdn_patterns": [
            r"tailwindcss(?:\.min)?\.js",
            r"cdn\.tailwindcss\.com",
            r"/tailwind(?:\.min)?\.css"
        ],
        "class_patterns": [
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?flex-(?:row|col|wrap|1)$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?grid-cols-\d+$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?space-[xy]-\d+$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?bg-(?:red|blue|gray|slate|emerald|amber|indigo|violet|purple|pink|zinc|neutral|stone)-\d{2,3}$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl)$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?rounded-(?:none|sm|md|lg|xl|2xl|3xl|full)$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?shadow-(?:sm|md|lg|xl|2xl|inner|none)$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?items-(?:center|start|end|baseline|stretch)$",
            r"^(?:hover:|focus:|sm:|md:|lg:|xl:|2xl:)?justify-(?:between|center|start|end|around|evenly)$"
        ],
        "var_patterns": [
            r"^--tw-"
        ]
    },
    "Bulma": {
        "cdn_patterns": [
            r"bulma(?:\.min)?\.css",
            r"cdnjs\.cloudflare\.com/ajax/libs/bulma",
            r"cdn\.jsdelivr\.net/npm/bulma"
        ],
        "class_patterns": [
            r"^is-(?:primary|info|success|warning|danger|white|black|light|dark|link)$",
            r"^is-(?:small|normal|medium|large)$",
            r"^is-(?:fullwidth|outlined|inverted|rounded|loading)$",
            r"^columns$",
            r"^column$",
            r"^is-(?:half|one-third|two-thirds|one-quarter|three-quarters)$",
            r"^has-text-(?:primary|info|success|warning|danger|centered|left|right)$",
            r"^has-background-(?:primary|info|success|warning|danger)$",
            r"^hero(?:-body|-head|-foot)?$"
        ],
        "var_patterns": [
            r"^--bulma-"
        ]
    },
    "Foundation": {
        "cdn_patterns": [
            r"foundation(?:\.min)?\.css",
            r"foundation(?:\.min)?\.js",
            r"cdn\.jsdelivr\.net/npm/foundation-sites",
            r"cdnjs\.cloudflare\.com/ajax/libs/foundation"
        ],
        "class_patterns": [
            r"^cell$",
            r"^grid-x$",
            r"^grid-y$",
            r"^grid-container$",
            r"^grid-margin-[xy]$",
            r"^top-bar$",
            r"^callout$",
            r"^button-group$",
            r"^reveal(?:-modal)?$"
        ],
        "attr_patterns": [
            r"data-reveal",
            r"data-dropdown-menu",
            r"data-accordion",
            r"data-off-canvas"
        ]
    },
    "Semantic UI": {
        "cdn_patterns": [
            r"semantic(?:\.min)?\.css",
            r"semantic(?:\.min)?\.js",
            r"semantic-ui",
            r"fomantic-ui"
        ],
        "class_patterns": [
            r"^ui\s+(?:primary|secondary|red|orange|yellow|green|teal|blue|violet|purple|pink|brown|grey|black)?\s*button$",
            r"^ui\s+container$",
            r"^ui\s+grid$",
            r"^ui\s+card$",
            r"^ui\s+menu$",
            r"^ui\s+modal$",
            r"^ui\s+segment$",
            r"^ui\s+header$",
            r"^ui\s+form$"
        ]
    },
    "Materialize CSS": {
        "cdn_patterns": [
            r"materialize(?:\.min)?\.css",
            r"materialize(?:\.min)?\.js",
            r"cdnjs\.cloudflare\.com/ajax/libs/materialize"
        ],
        "class_patterns": [
            r"^waves-effect$",
            r"^waves-light$",
            r"^valign-wrapper$",
            r"^z-depth-\d+$",
            r"^side-nav$",
            r"^sidenav$",
            r"^card-panel$",
            r"^collection-item$"
        ]
    },
    "UIkit": {
        "cdn_patterns": [
            r"uikit(?:\.min)?\.css",
            r"uikit(?:\.min)?\.js",
            r"cdn\.jsdelivr\.net/npm/uikit",
            r"cdnjs\.cloudflare\.com/ajax/libs/uikit"
        ],
        "class_patterns": [
            r"^uk-(?:button|card|grid|container|navbar|nav|modal|alert|badge|table|icon|margin|padding)$",
            r"^uk-button-(?:default|primary|secondary|danger|text|link)$"
        ],
        "attr_patterns": [
            r"^uk-"
        ]
    },
    "Pure CSS": {
        "cdn_patterns": [
            r"pure(?:-min)?\.css",
            r"cdn\.jsdelivr\.net/npm/purecss",
            r"yui\.yahooapis\.com/pure",
            r"cdnjs\.cloudflare\.com/ajax/libs/pure"
        ],
        "class_patterns": [
            r"^pure-g$",
            r"^pure-u-(?:\d+-\d+|\d+)$",
            r"^pure-button(?:-primary|-active|-disabled)?$",
            r"^pure-form(?:-aligned|-stacked)?$",
            r"^pure-menu(?:-horizontal|-scrollable)?$",
            r"^pure-table(?:-striped|-bordered)?$"
        ]
    },
    "Pico CSS": {
        "cdn_patterns": [
            r"pico(?:\.fluid|\.classless|\.min)?\.css",
            r"cdn\.jsdelivr\.net/npm/@picocss/pico"
        ],
        "var_patterns": [
            r"^--pico-"
        ],
        "attr_patterns": [
            r"data-theme=\"(?:dark|light)\""
        ]
    },
    "W3.CSS": {
        "cdn_patterns": [
            r"w3(?:\.min)?\.css",
            r"www\.w3schools\.com/w3css"
        ],
        "class_patterns": [
            r"^w3-(?:container|row|col|panel|card|button|btn|bar|sidebar|modal|badge|tag|table|input|responsive)$",
            r"^w3-(?:red|blue|green|yellow|teal|orange|indigo|purple|black|white|grey)$"
        ]
    },
    "Spectre.css": {
        "cdn_patterns": [
            r"spectre(?:\.min)?\.css",
            r"spectre-exp(?:\.min)?\.css",
            r"spectre-icons(?:\.min)?\.css",
            r"cdnjs\.cloudflare\.com/ajax/libs/spectre\.css"
        ],
        "class_patterns": [
            r"^columns$",
            r"^column\s+col-\d+$",
            r"^navbar-section$",
            r"^form-group$",
            r"^input-group$",
            r"^toast-(?:primary|success|warning|error)$",
            r"^divider(?:-vert)?$"
        ]
    },
    "Milligram": {
        "cdn_patterns": [
            r"milligram(?:\.min)?\.css",
            r"cdnjs\.cloudflare\.com/ajax/libs/milligram"
        ],
        "class_patterns": [
            r"^button-outline$",
            r"^button-clear$",
            r"^float-right$",
            r"^float-left$"
        ]
    },
    "Skeleton CSS": {
        "cdn_patterns": [
            r"skeleton(?:\.min)?\.css",
            r"cdnjs\.cloudflare\.com/ajax/libs/skeleton"
        ],
        "class_patterns": [
            r"^ten\.columns$",
            r"^twelve\.columns$",
            r"^six\.columns$",
            r"^one-half\.column$",
            r"^one-third\.column$",
            r"^button-primary$"
        ]
    },
    "Tachyons": {
        "cdn_patterns": [
            r"tachyons(?:\.min)?\.css",
            r"unpkg\.com/tachyons"
        ],
        "class_patterns": [
            r"^(?:ba|bt|br|bb|bl)$",
            r"^pa[0-7]$",
            r"^ma[0-7]$",
            r"^tc$",
            r"^fl$",
            r"^w-100$",
            r"^mw[1-9]$",
            r"^dim$",
            r"^f[1-7]$"
        ]
    },
    "Halfmoon": {
        "cdn_patterns": [
            r"halfmoon(?:-variables|-core)?(?:\.min)?\.(?:css|js)",
            r"cdn\.jsdelivr\.net/npm/halfmoon"
        ],
        "class_patterns": [
            r"^page-wrapper$",
            r"^sidebar-overlay$",
            r"^content-wrapper$",
            r"^dark-mode-toggle$"
        ],
        "var_patterns": [
            r"^--dm-",
            r"^--lm-"
        ],
        "attr_patterns": [
            r"data-set-preferred-mode-onload"
        ]
    },
    "UnoCSS": {
        "cdn_patterns": [
            r"uno\.css",
            r"@unocss"
        ],
        "attr_patterns": [
            r"un-cloak",
            r"uno-"
        ]
    },
    "Windi CSS": {
        "cdn_patterns": [
            r"windi(?:\.min)?\.css"
        ],
        "class_patterns": [
            r"^windi-"
        ]
    }
}

DESIGN_SYSTEMS = {
    "UX4G Design System": {
        "is_ux4g_ds": True,
        "cdn_patterns": [
            r"cdn\.ux4g\.gov\.in/(?:UX4G|ux4g)@[^/]+/css/ux4g(?:-min)?\.css",
            r"cdn\.ux4g\.gov\.in/.*ux4g.*\.css",
            r"cdn\.digilocker\.gov\.in/ux4g/.*ux4g.*\.css",
            r"/css/ux4g(?:-min|\.min)?\.css",
            r"ux4g(?:-min|\.min)?\.css",
            r"/ux4g/[^/]+/css/ux4g",
            r"ux4g-v\d+.*\.css"
        ],
        "class_patterns": [
            r"^ux4g-",
            r"^ux4g-btn",
            r"^ux4g-card",
            r"^ux4g-navbar",
            r"^ux4g-header",
            r"^ux4g-footer",
            r"^ux4g-tab",
            r"^ux4g-table",
            r"^ux4g-alert",
            r"^ux4g-modal",
            r"^ux4g-badge",
            r"^ux4g-form",
            r"^ux4g-input",
            r"^ux4g-accordion"
        ],
        "var_patterns": [
            r"^--ux4g-"
        ],
        "attr_patterns": [
            r"data-ux4g-",
            r"ux4g-"
        ],
        "meta_patterns": [
            r"UX4G",
            r"UX4G Design System"
        ]
    },
    "UX4G Accessibility CDN": {
        "is_ux4g_acc": True,
        "cdn_patterns": [
            r"accessibility-widget\.js",
            r"cdn\.ux4g\.gov\.in/.*accessibility.*",
            r"accessibility\.ux4g\.gov\.in",
            r"accessibility-v[\d\.]+/accessibility-widget",
            r"cdn\.ux4g\.gov\.in/tools/accessibility-widget\.js",
            r"accessibility-widget\.css"
        ]
    },
    "Angular Material": {
        "class_patterns": [
            r"^mat-(?:mdc-)?button$",
            r"^mat-(?:mdc-)?card$",
            r"^mat-(?:mdc-)?form-field$",
            r"^mat-(?:mdc-)?table$",
            r"^mat-(?:mdc-)?toolbar$",
            r"^mat-(?:mdc-)?icon$",
            r"^mat-(?:mdc-)?menu$",
            r"^mat-(?:mdc-)?dialog-container$",
            r"^mat-(?:mdc-)?tab-group$"
        ],
        "attr_patterns": [
            r"mat-button",
            r"mat-raised-button",
            r"mat-icon-button",
            r"mat-stroked-button",
            r"mat-flat-button",
            r"mat-fab",
            r"mat-mini-fab",
            r"mat-card",
            r"mat-table",
            r"<mat-"
        ]
    },
    "Material UI (MUI)": {
        "class_patterns": [
            r"^MuiButton-root",
            r"^MuiCard-root",
            r"^MuiTypography-root",
            r"^MuiGrid-root",
            r"^MuiBox-root",
            r"^MuiContainer-root",
            r"^MuiAppBar-root",
            r"^MuiPaper-root",
            r"^MuiDialog-root",
            r"^MuiInputBase-root",
            r"^MuiSvgIcon-root"
        ],
        "var_patterns": [
            r"^--mui-"
        ]
    },
    "Ant Design": {
        "cdn_patterns": [
            r"antd(?:\.min)?\.css",
            r"cdnjs\.cloudflare\.com/ajax/libs/antd"
        ],
        "class_patterns": [
            r"^ant-btn(?:-[a-z]+)?$",
            r"^ant-layout(?:-[a-z]+)?$",
            r"^ant-row$",
            r"^ant-col-\d+$",
            r"^ant-card(?:-[a-z]+)?$",
            r"^ant-menu(?:-[a-z]+)?$",
            r"^ant-modal(?:-[a-z]+)?$",
            r"^ant-table(?:-[a-z]+)?$",
            r"^ant-form(?:-[a-z]+)?$",
            r"^ant-input(?:-[a-z]+)?$"
        ],
        "var_patterns": [
            r"^--ant-"
        ]
    },
    "PrimeNG": {
        "cdn_patterns": [
            r"primeng(?:\.min)?\.css",
            r"primeicons\.css"
        ],
        "class_patterns": [
            r"^p-component$",
            r"^p-button(?:-[a-z]+)?$",
            r"^p-datatable(?:-[a-z]+)?$",
            r"^p-card(?:-[a-z]+)?$",
            r"^p-dialog(?:-[a-z]+)?$",
            r"^p-dropdown(?:-[a-z]+)?$",
            r"^p-inputtext$"
        ],
        "attr_patterns": [
            r"pButton",
            r"pRipple",
            r"pTemplate"
        ]
    },
    "PrimeReact": {
        "cdn_patterns": [
            r"primereact(?:\.min)?\.css"
        ],
        "class_patterns": [
            r"^p-component$",
            r"^p-button$",
            r"^p-datatable$",
            r"^p-inputtext$"
        ]
    },
    "PrimeVue": {
        "cdn_patterns": [
            r"primevue(?:\.min)?\.css"
        ],
        "class_patterns": [
            r"^p-component$",
            r"^p-button$",
            r"^p-datatable$"
        ]
    },
    "Chakra UI": {
        "class_patterns": [
            r"^chakra-button",
            r"^chakra-card",
            r"^chakra-stack",
            r"^chakra-heading",
            r"^chakra-text",
            r"^chakra-container",
            r"^chakra-portal"
        ],
        "var_patterns": [
            r"^--chakra-"
        ]
    },
    "Mantine": {
        "class_patterns": [
            r"^mantine-Button-root",
            r"^mantine-Card-root",
            r"^mantine-Container-root",
            r"^mantine-Grid-root",
            r"^mantine-Text-root",
            r"^mantine-Title-root",
            r"^mantine-Header-root"
        ],
        "var_patterns": [
            r"^--mantine-"
        ]
    },
    "Carbon Design System": {
        "cdn_patterns": [
            r"carbon-components(?:\.min)?\.css",
            r"@carbon/styles"
        ],
        "class_patterns": [
            r"^bx--btn",
            r"^bx--grid",
            r"^bx--row",
            r"^bx--col",
            r"^bx--header",
            r"^cds--btn",
            r"^cds--grid",
            r"^cds--row",
            r"^cds--col",
            r"^cds--header"
        ],
        "var_patterns": [
            r"^--cds-"
        ]
    },
    "Fluent UI": {
        "class_patterns": [
            r"^ms-Button",
            r"^ms-Fabric",
            r"^ms-Grid",
            r"^fui-Button",
            r"^fui-Card",
            r"^fui-FluentProvider"
        ],
        "var_patterns": [
            r"^--fluent-"
        ]
    },
    "PatternFly": {
        "cdn_patterns": [
            r"patternfly(?:\.min)?\.css",
            r"@patternfly"
        ],
        "class_patterns": [
            r"^pf-c-button",
            r"^pf-c-card",
            r"^pf-c-page",
            r"^pf-c-nav",
            r"^pf-v5-c-button",
            r"^pf-v5-c-card",
            r"^pf-v6-c-button"
        ],
        "var_patterns": [
            r"^--pf-v\d+-"
        ]
    },
    "Salesforce Lightning Design System": {
        "cdn_patterns": [
            r"salesforce-lightning-design-system(?:\.min)?\.css",
            r"/slds/"
        ],
        "class_patterns": [
            r"^slds-button",
            r"^slds-card",
            r"^slds-grid",
            r"^slds-col",
            r"^slds-box",
            r"^slds-nav-vertical"
        ],
        "var_patterns": [
            r"^--slds-"
        ]
    },
    "Atlassian Design System": {
        "class_patterns": [
            r"^css-[a-zA-Z0-9]+-Button",
            r"^css-[a-zA-Z0-9]+-Modal",
            r"ak-button"
        ],
        "var_patterns": [
            r"^--ds-border-",
            r"^--ds-background-",
            r"^--ds-text-"
        ]
    },
    "Adobe Spectrum": {
        "cdn_patterns": [
            r"@spectrum-css"
        ],
        "class_patterns": [
            r"^spectrum-Button",
            r"^spectrum-Card",
            r"^spectrum-Picker",
            r"^spectrum-Heading"
        ],
        "var_patterns": [
            r"^--spectrum-"
        ]
    },
    "Shopify Polaris": {
        "class_patterns": [
            r"^Polaris-Button",
            r"^Polaris-Card",
            r"^Polaris-Page",
            r"^Polaris-Layout",
            r"^Polaris-Banner",
            r"^Polaris-Text"
        ],
        "var_patterns": [
            r"^--p-color-",
            r"^--p-space-"
        ]
    },
    "SAP Fiori": {
        "cdn_patterns": [
            r"sap-ui-core\.js",
            r"resources/sap/"
        ],
        "class_patterns": [
            r"^sapMBtn",
            r"^sapMPage",
            r"^sapMShell",
            r"^sapUiBody",
            r"^sapFDynamicPage"
        ],
        "var_patterns": [
            r"^--sapUi"
        ]
    },
    "Oracle Redwood": {
        "class_patterns": [
            r"^oj-button",
            r"^oj-card",
            r"^oj-flex",
            r"^oj-hybrid",
            r"^oj-navigationlist"
        ],
        "var_patterns": [
            r"^--oj-"
        ]
    },
    "GOV.UK Design System": {
        "cdn_patterns": [
            r"govuk-frontend(?:\.min)?\.css",
            r"govuk-frontend(?:\.min)?\.js"
        ],
        "class_patterns": [
            r"^govuk-header",
            r"^govuk-button",
            r"^govuk-container",
            r"^govuk-grid-row",
            r"^govuk-grid-column",
            r"^govuk-footer",
            r"^govuk-phase-banner"
        ],
        "var_patterns": [
            r"^--govuk-"
        ]
    },
    "USWDS": {
        "cdn_patterns": [
            r"uswds(?:\.min)?\.css",
            r"uswds(?:\.min)?\.js"
        ],
        "class_patterns": [
            r"^usa-button",
            r"^usa-header",
            r"^usa-card",
            r"^usa-nav",
            r"^usa-banner",
            r"^usa-footer",
            r"^usa-grid"
        ]
    },
    "Clarity": {
        "cdn_patterns": [
            r"clr-ui(?:\.min)?\.css",
            r"@clr/core"
        ],
        "class_patterns": [
            r"^clr-vertical-nav",
            r"^clr-header",
            r"^clr-main-container",
            r"^clr-row",
            r"^clr-col"
        ],
        "attr_patterns": [
            r"<clr-",
            r"clr-icon"
        ]
    },
    "Base Web": {
        "class_patterns": [
            r"^baseui-",
            r"^data-baseweb"
        ],
        "attr_patterns": [
            r"data-baseweb"
        ]
    },
    "Evergreen UI": {
        "class_patterns": [
            r"^ub-f-",
            r"^ub-b-",
            r"^ub-color-"
        ]
    },
    "Grommet": {
        "class_patterns": [
            r"^StyledButton",
            r"^StyledBox",
            r"^StyledHeading",
            r"^StyledGrid"
        ],
        "attr_patterns": [
            r"grommet"
        ]
    },
    "Blueprint.js": {
        "cdn_patterns": [
            r"@blueprintjs/core",
            r"blueprint(?:\.min)?\.css"
        ],
        "class_patterns": [
            r"^bp[345]-button",
            r"^bp[345]-card",
            r"^bp[345]-navbar",
            r"^bp[345]-icon",
            r"^bp[345]-dialog"
        ]
    },
    "Elastic UI": {
        "cdn_patterns": [
            r"@elastic/eui",
            r"eui_theme"
        ],
        "class_patterns": [
            r"^euiButton",
            r"^euiCard",
            r"^euiPage",
            r"^euiFlexGroup",
            r"^euiHeader"
        ]
    },
    "Kendo UI": {
        "cdn_patterns": [
            r"kendo\.(?:all|default|bootstrap|material)(?:\.min)?\.css",
            r"kendo\.(?:all|web)(?:\.min)?\.js"
        ],
        "class_patterns": [
            r"^k-button",
            r"^k-grid",
            r"^k-widget",
            r"^k-input",
            r"^k-dropdown"
        ],
        "var_patterns": [
            r"^--kendo-"
        ]
    },
    "Syncfusion": {
        "cdn_patterns": [
            r"ej2\.(?:min)?\.css",
            r"ej2\.(?:min)?\.js",
            r"cdn\.syncfusion\.com"
        ],
        "class_patterns": [
            r"^e-btn",
            r"^e-grid",
            r"^e-control",
            r"^e-card",
            r"^e-dialog"
        ]
    },
    "DevExtreme": {
        "cdn_patterns": [
            r"dx\.(?:all|light|dark)(?:\.min)?\.css",
            r"dx\.(?:all|web)(?:\.min)?\.js"
        ],
        "class_patterns": [
            r"^dx-button",
            r"^dx-datagrid",
            r"^dx-widget",
            r"^dx-layout"
        ]
    },
    "Nebular": {
        "cdn_patterns": [
            r"@nebular/theme"
        ],
        "class_patterns": [
            r"^nb-card",
            r"^nb-button",
            r"^nb-layout",
            r"^nb-sidebar"
        ],
        "attr_patterns": [
            r"<nb-layout",
            r"<nb-card"
        ]
    },
    "Taiga UI": {
        "class_patterns": [
            r"^tui-button",
            r"^tui-card",
            r"^tui-island",
            r"^tui-space"
        ],
        "attr_patterns": [
            r"tuiButton",
            r"<tui-root"
        ]
    },
    "NG-ZORRO": {
        "cdn_patterns": [
            r"ng-zorro-antd"
        ],
        "class_patterns": [
            r"^ant-btn",
            r"^ant-row",
            r"^ant-card"
        ],
        "attr_patterns": [
            r"nz-button",
            r"nzType",
            r"<nz-"
        ]
    },
    "Vuetify": {
        "cdn_patterns": [
            r"vuetify(?:\.min)?\.css",
            r"vuetify(?:\.min)?\.js",
            r"cdn\.jsdelivr\.net/npm/vuetify"
        ],
        "class_patterns": [
            r"^v-btn(?:--[a-z]+)?$",
            r"^v-card(?:-[a-z]+)?$",
            r"^v-container$",
            r"^v-row$",
            r"^v-col(?:-\d+)?$",
            r"^v-app-bar$",
            r"^v-navigation-drawer$",
            r"^v-main$"
        ],
        "var_patterns": [
            r"^--v-theme-"
        ]
    },
    "Quasar": {
        "cdn_patterns": [
            r"quasar(?:\.min)?\.css",
            r"quasar(?:\.umd)?(?:\.min)?\.js",
            r"cdn\.jsdelivr\.net/npm/quasar"
        ],
        "class_patterns": [
            r"^q-btn",
            r"^q-card",
            r"^q-layout",
            r"^q-page",
            r"^q-header",
            r"^q-toolbar",
            r"^q-input"
        ],
        "var_patterns": [
            r"^--q-"
        ]
    },
    "Element Plus": {
        "cdn_patterns": [
            r"element-plus(?:\.min)?\.css",
            r"element-ui(?:\.min)?\.css",
            r"unpkg\.com/element-plus"
        ],
        "class_patterns": [
            r"^el-button(?:--[a-z]+)?$",
            r"^el-card$",
            r"^el-container$",
            r"^el-header$",
            r"^el-main$",
            r"^el-row$",
            r"^el-col-\d+$",
            r"^el-input(?:__[a-z]+)?$"
        ],
        "var_patterns": [
            r"^--el-"
        ]
    },
    "Shoelace": {
        "cdn_patterns": [
            r"cdn\.jsdelivr\.net/npm/@shoelace-style/shoelace",
            r"shoelace\.style"
        ],
        "class_patterns": [
            r"^sl-button",
            r"^sl-card",
            r"^sl-dialog",
            r"^sl-input"
        ],
        "attr_patterns": [
            r"<sl-button",
            r"<sl-card",
            r"<sl-icon"
        ],
        "var_patterns": [
            r"^--sl-"
        ]
    },
    "Radix UI": {
        "attr_patterns": [
            r"data-radix-",
            r"data-state=\"(?:open|closed|checked|unchecked|active|inactive)\"",
            r"data-orientation=\"(?:horizontal|vertical)\""
        ]
    },
    "HeroUI": {
        "cdn_patterns": [
            r"@heroui"
        ],
        "class_patterns": [
            r"^heroui-button",
            r"^heroui-card"
        ]
    },
    "React Bootstrap": {
        "class_patterns": [
            r"^btn-primary$",
            r"^btn-outline-primary$",
            r"^col-md-\d+$",
            r"^col-lg-\d+$",
            r"^container-fluid$"
        ],
        "attr_patterns": [
            r"data-rr-ui-",
            r"react-bootstrap"
        ]
    }
}

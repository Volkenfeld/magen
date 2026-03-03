#!/usr/bin/env python3
"""Generate Hebrew locale (he.json) from English locale (en.json).

Translates all user-facing strings to Hebrew. For highly technical/military
abbreviations and brand names, keeps English originals.
"""
import json
import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent / "src" / "locales"
en_path = src / "en.json"
he_path = src / "he.json"

with open(en_path, "r", encoding="utf-8") as f:
    en = json.load(f)

# Deep-copy structure, then overlay Hebrew translations
import copy
he = copy.deepcopy(en)

# ── App ──
he["app"] = {
    "title": "מגן",
    "description": "מודיעין הגנה אזרחית בזמן אמת"
}

# ── Country Brief (top level) ──
he["countryBrief"]["identifying"] = "מזהה מדינה..."
he["countryBrief"]["locating"] = "מאתר אזור..."
he["countryBrief"]["limitedCoverage"] = "כיסוי מוגבל"
he["countryBrief"]["instabilityIndex"] = "מדד אי-יציבות"
he["countryBrief"]["notTracked"] = "לא במעקב, {{country}} לא נמצאת ברשימת CII דרג-1"
he["countryBrief"]["intelBrief"] = "תדריך מודיעיני"
he["countryBrief"]["generatingBrief"] = "מייצר תדריך מודיעיני..."
he["countryBrief"]["topNews"] = "חדשות מובילות"
he["countryBrief"]["activeSignals"] = "אותות פעילים"
he["countryBrief"]["timeline"] = "ציר זמן 7 ימים"
he["countryBrief"]["predictionMarkets"] = "שוקי חיזוי"
he["countryBrief"]["loadingMarkets"] = "טוען שוקי חיזוי..."
he["countryBrief"]["infrastructure"] = "חשיפת תשתיות"
he["countryBrief"]["briefUnavailable"] = "תדריך AI לא זמין, הגדר GROQ_API_KEY בהגדרות."
he["countryBrief"]["cached"] = "מהמטמון"
he["countryBrief"]["fresh"] = "עדכני"
he["countryBrief"]["noMarkets"] = "אין שוקי חיזוי פעילים למדינה זו."
he["countryBrief"]["loadingIndex"] = "טוען מדד..."
he["countryBrief"]["components"] = {
    "unrest": "אי-שקט",
    "conflict": "סכסוך",
    "security": "ביטחון",
    "information": "מידע"
}
he["countryBrief"]["signals"] = {
    "protests": "הפגנות",
    "militaryAir": "מטוסים צבאיים",
    "militarySea": "כלי שיט צבאיים",
    "outages": "תקלות",
    "earthquakes": "רעידות אדמה",
    "displaced": "עקורים",
    "climate": "לחץ אקלימי",
    "conflictEvents": "אירועי סכסוך",
    "activeStrikes": "תקיפות פעילות",
    "aviationDisruptions": "שיבושי תעופה",
    "gpsJammingZones": "אזורי שיבוש GPS"
}
he["countryBrief"]["timeAgo"] = {
    "m": "לפני {{count}} דק'",
    "h": "לפני {{count}} שע'",
    "d": "לפני {{count}} ימים"
}
he["countryBrief"]["infra"] = {
    "pipeline": "צינורות",
    "cable": "כבלים תת-ימיים",
    "datacenter": "מרכזי נתונים",
    "base": "בסיסים צבאיים",
    "nuclear": "מתקנים גרעיניים",
    "port": "נמלים"
}
he["countryBrief"]["levels"] = {
    "critical": "קריטי",
    "high": "גבוה",
    "elevated": "מוגבר",
    "moderate": "מתון",
    "normal": "רגיל",
    "low": "נמוך"
}
he["countryBrief"]["trends"] = {
    "rising": "עולה",
    "falling": "יורד",
    "stable": "יציב"
}
he["countryBrief"]["militaryActivity"] = "פעילות צבאית"
he["countryBrief"]["economicIndicators"] = "מדדים כלכליים"
he["countryBrief"]["ownFlights"] = "טיסות עצמיות"
he["countryBrief"]["foreignFlights"] = "טיסות זרות"
he["countryBrief"]["navalVessels"] = "כלי שיט צבאיים"
he["countryBrief"]["foreignPresence"] = "נוכחות זרה"
he["countryBrief"]["nearestBases"] = "בסיסים צבאיים קרובים"
he["countryBrief"]["noBasesNearby"] = "אין בסיסים קרובים ברדיוס 600 ק\"מ."
he["countryBrief"]["noInfrastructure"] = "לא נמצאו תשתיות קריטיות ברדיוס 600 ק\"מ."
he["countryBrief"]["noGeometry"] = "אין נתונים גיאומטריים לניתוח תשתיות."
he["countryBrief"]["noSignals"] = "אין אותות חמורים אחרונים."
he["countryBrief"]["assessmentUnavailable"] = "הערכה לא זמינה."
he["countryBrief"]["noNews"] = "אין כיסוי תקשורתי עדכני למדינה זו."
he["countryBrief"]["noMarkets"] = "אין שוקי חיזוי פעילים למדינה זו."
he["countryBrief"]["noIndicators"] = "אין מדדים כלכליים זמינים למדינה זו."
he["countryBrief"]["nearbyPorts"] = "נמלים קרובים"
he["countryBrief"]["detected"] = "זוהה"
he["countryBrief"]["notDetected"] = "לא"
he["countryBrief"]["ciiUnavailable"] = "ציון CII לא זמין למדינה זו."
he["countryBrief"]["chips"] = {
    "criticalNews": "חדשות קריטיות",
    "protests": "הפגנות",
    "militaryAir": "תעופה צבאית",
    "navalVessels": "כלי שיט צבאיים",
    "outages": "תקלות",
    "aisDisruptions": "שיבושי AIS",
    "satelliteFires": "שריפות לווין",
    "temporalAnomalies": "חריגות זמניות",
    "cyberThreats": "איומי סייבר",
    "earthquakes": "רעידות אדמה",
    "displaced": "עקורים",
    "climateStress": "לחץ אקלימי",
    "conflictEvents": "אירועי סכסוך",
    "activeStrikes": "תקיפות פעילות",
    "doNotTravel": "איסור נסיעה",
    "reconsiderTravel": "שקלו מחדש נסיעה",
    "exerciseCaution": "נקטו זהירות",
    "advisory": "אזהרה",
    "activeSirens": "צפירות פעילות",
    "sirens24h": "צפירות / 24 שע'",
    "aviationDisruptions": "שיבושי תעופה",
    "gpsJammingZones": "אזורי שיבוש GPS"
}
he["countryBrief"]["fallback"] = {
    "instabilityIndex": "**מדד אי-יציבות: {{score}}/100** ({{level}}, {{trend}})",
    "protestsDetected": "{{count}} הפגנות פעילות זוהו",
    "aircraftTracked": "{{count}} מטוסים צבאיים במעקב",
    "vesselsTracked": "{{count}} כלי שיט צבאיים במעקב",
    "internetOutages": "{{count}} תקלות אינטרנט",
    "recentEarthquakes": "{{count}} רעידות אדמה אחרונות",
    "stockIndex": "מדד מניות: {{value}}",
    "recentHeadlines": "**כותרות אחרונות:**",
    "activeStrikes": "{{count}} תקיפות פעילות זוהו"
}

# ── Header ──
he["header"] = {
    "world": "עולם",
    "tech": "טכנולוגיה",
    "live": "שידור חי",
    "search": "חיפוש",
    "settings": "הגדרות",
    "sources": "מקורות",
    "copyLink": "קישור",
    "downloadApp": "הורד אפליקציה",
    "fullscreen": "מסך מלא",
    "pinMap": "הצמד מפה למעלה",
    "viewOnGitHub": "צפה ב-GitHub",
    "filterSources": "סנן מקורות...",
    "sourcesEnabled": "{{enabled}}/{{total}} פעילים",
    "finance": "פיננסים",
    "toggleTheme": "החלף ערכת נושא כהה/בהיר",
    "panelDisplayCaption": "בחרו אילו פאנלים יוצגו בלוח המחוונים",
    "tabGeneral": "כללי",
    "tabPanels": "פאנלים",
    "tabSources": "מקורות",
    "languageLabel": "שפה",
    "sourceRegionAll": "הכל",
    "sourceRegionWorldwide": "עולמי",
    "sourceRegionUS": "ארצות הברית",
    "sourceRegionMiddleEast": "המזרח התיכון",
    "sourceRegionAfrica": "אפריקה",
    "sourceRegionLatAm": "אמריקה הלטינית",
    "sourceRegionAsiaPacific": "אסיה-פסיפיק",
    "sourceRegionEurope": "אירופה",
    "sourceRegionTopical": "נושאי",
    "sourceRegionIntel": "מודיעין",
    "sourceRegionTechNews": "חדשות טכנולוגיה",
    "sourceRegionAiMl": "AI ולמידת מכונה",
    "sourceRegionStartupsVc": "סטארטאפים והון סיכון",
    "sourceRegionRegionalTech": "מערכות אקולוגיות אזוריות",
    "sourceRegionDeveloper": "מפתחים",
    "sourceRegionCybersecurity": "אבטחת סייבר",
    "sourceRegionTechPolicy": "מדיניות ומחקר",
    "sourceRegionTechMedia": "מדיה ופודקאסטים",
    "sourceRegionMarkets": "שווקים וניתוח",
    "sourceRegionFixedIncomeFx": "אג\"ח ומט\"ח",
    "sourceRegionCommodities": "סחורות",
    "sourceRegionCryptoDigital": "קריפטו ודיגיטל",
    "sourceRegionCentralBanks": "בנקים מרכזיים וכלכלה",
    "sourceRegionDeals": "עסקאות ותאגידים",
    "sourceRegionFinRegulation": "רגולציה פיננסית",
    "sourceRegionGulfMena": "מפרץ ומזה\"ת",
    "filterPanels": "סנן פאנלים...",
    "resetLayout": "אפס פריסה",
    "panelCatCore": "ליבה",
    "panelCatIntelligence": "מודיעין",
    "panelCatRegionalNews": "חדשות אזוריות",
    "panelCatMarketsFinance": "שווקים ופיננסים",
    "panelCatTopical": "נושאי",
    "panelCatDataTracking": "נתונים ומעקב",
    "panelCatTechAi": "טכנולוגיה ו-AI",
    "panelCatStartupsVc": "סטארטאפים והון סיכון",
    "panelCatSecurityPolicy": "ביטחון ומדיניות",
    "panelCatMarkets": "שווקים",
    "panelCatFixedIncomeFx": "אג\"ח ומט\"ח",
    "panelCatCommodities": "סחורות",
    "panelCatCryptoDigital": "קריפטו ודיגיטל",
    "panelCatCentralBanks": "בנקים מרכזיים וכלכלה",
    "panelCatDeals": "עסקאות ומוסדיים",
    "panelCatGulfMena": "מפרץ ומזה\"ת",
    "panelCatTradePolicy": "מדיניות סחר"
}

# ── Panels ──
he["panels"] = {
    "liveNews": "חדשות בזמן אמת",
    "markets": "שווקים",
    "map": "מצב גלובלי",
    "techMap": "טכנולוגיה גלובלית",
    "techHubs": "מרכזי טכנולוגיה חמים",
    "status": "סטטוס מערכת",
    "insights": "תובנות AI",
    "strategicPosture": "עמדה אסטרטגית AI",
    "cii": "אי-יציבות מדינתית",
    "strategicRisk": "סקירת סיכונים אסטרטגיים",
    "intel": "פיד מודיעין",
    "gdeltIntel": "מודיעין חי",
    "cascade": "מפל תשתיות",
    "politics": "חדשות העולם",
    "us": "ארצות הברית",
    "europe": "אירופה",
    "middleeast": "המזרח התיכון",
    "africa": "אפריקה",
    "latam": "אמריקה הלטינית",
    "asia": "אסיה-פסיפיק",
    "energy": "אנרגיה ומשאבים",
    "gov": "ממשל",
    "thinktanks": "מכוני מחקר",
    "polymarket": "חיזויים",
    "commodities": "סחורות",
    "economic": "מדדים כלכליים",
    "tradePolicy": "מדיניות סחר",
    "supplyChain": "שרשרת אספקה",
    "finance": "פיננסים",
    "tech": "טכנולוגיה",
    "crypto": "קריפטו",
    "heatmap": "מפת חום מגזרית",
    "ai": "AI/ML",
    "layoffs": "מעקב פיטורים",
    "monitors": "המוניטורים שלי",
    "satelliteFires": "שריפות",
    "macroSignals": "רדאר שווקים",
    "etfFlows": "מעקב BTC ETF",
    "stablecoins": "מטבעות יציבים",
    "deduction": "הסק מצב",
    "ucdpEvents": "אירועי סכסוך מזוין",
    "giving": "תרומות גלובליות",
    "displacement": "עקירה UNHCR",
    "climate": "חריגות אקלים",
    "populationExposure": "חשיפת אוכלוסייה",
    "securityAdvisories": "התראות ביטחון",
    "orefSirens": "צפירות פיקוד העורף",
    "telegramIntel": "מודיעין טלגרם",
    "startups": "סטארטאפים והון סיכון",
    "vcblogs": "תובנות הון סיכון",
    "regionalStartups": "חדשות סטארטאפים גלובליות",
    "unicorns": "מעקב יוניקורנים",
    "accelerators": "מאיצים ויום הדגמות",
    "security": "אבטחת סייבר",
    "policy": "מדיניות ורגולציית AI",
    "regulation": "לוח רגולציית AI",
    "hardware": "מוליכים למחצה וחומרה",
    "cloud": "ענן ותשתיות",
    "dev": "קהילת מפתחים",
    "github": "GitHub Trending",
    "ipo": "IPO ו-SPAC",
    "funding": "מימון והון סיכון",
    "producthunt": "Product Hunt",
    "events": "אירועי טכנולוגיה",
    "serviceStatus": "סטטוס שירותים",
    "techReadiness": "מדד מוכנות טכנולוגית",
    "gccInvestments": "השקעות GCC",
    "geoHubs": "מוקדים גיאופוליטיים",
    "liveWebcams": "מצלמות רשת חיות",
    "gulfEconomies": "כלכלות המפרץ",
    "gulfIndices": "מדדי המפרץ",
    "gulfCurrencies": "מטבעות המפרץ",
    "gulfOil": "נפט המפרץ",
    "credits": "קרדיטים"
}

# ── Commands ──
he["commands"] = {
    "prefixes": {"map": "מפה", "panel": "פאנל", "brief": "תדריך"},
    "categories": {
        "navigate": "ניווט", "layers": "שכבות", "panels": "פאנלים",
        "view": "תצוגה", "actions": "פעולות", "country": "מדינה"
    },
    "regions": {
        "global": "תצוגה גלובלית", "mena": "מזרח תיכון וצפון אפריקה",
        "eu": "אירופה", "asia": "אסיה-פסיפיק", "america": "אמריקה",
        "africa": "אפריקה", "latam": "אמריקה הלטינית", "oceania": "אוקיאניה"
    },
    "tips": {
        "map": "הקלידו שם מדינה כדי לעוף אליה על המפה",
        "panel": "הקלידו שם פאנל כדי לגלול אליו",
        "brief": "הקלידו שם מדינה לתדריך מודיעיני",
        "layers": "הקלידו \"military\" או \"finance\" לשכבות מוגדרות",
        "time": "הקלידו \"1h\", \"24h\", או \"7d\" לסינון לפי זמן",
        "settings": "הקלידו \"dark mode\", \"settings\", או \"fullscreen\""
    }
}

# ── Modals ──
he["modals"]["search"]["placeholder"] = "חפשו או הקלידו פקודה..."
he["modals"]["search"]["hint"] = "חיפוש, מדינות, שכבות, פאנלים, ניווט, הגדרות"
he["modals"]["search"]["placeholderTech"] = "חפשו או הקלידו פקודה..."
he["modals"]["search"]["hintTech"] = "חיפוש, חברות, מעבדות AI, שכבות, ניווט, הגדרות"
he["modals"]["search"]["placeholderFinance"] = "חפשו או הקלידו פקודה..."
he["modals"]["search"]["hintFinance"] = "חיפוש, בורסות, שווקים, שכבות, ניווט, הגדרות"
he["modals"]["search"]["recent"] = "חיפושים אחרונים"
he["modals"]["search"]["empty"] = "חפשו נתונים או הריצו פקודות"
he["modals"]["search"]["noResults"] = "אין תוצאות"
he["modals"]["search"]["navigate"] = "ניווט"
he["modals"]["search"]["select"] = "בחירה"
he["modals"]["search"]["close"] = "סגירה"
he["modals"]["search"]["types"] = {
    "country": "מדינה", "news": "חדשות", "hotspot": "מוקד",
    "market": "שוק", "prediction": "חיזוי", "conflict": "סכסוך",
    "base": "בסיס צבאי", "pipeline": "צינור", "cable": "כבל תת-ימי",
    "datacenter": "מרכז נתונים", "earthquake": "רעידת אדמה",
    "outage": "תקלה", "nuclear": "אתר גרעיני", "irradiator": "מקרין",
    "techcompany": "חברת טכנולוגיה", "ailab": "מעבדת AI",
    "startup": "סטארטאפ", "techevent": "אירוע טכנולוגי",
    "techhq": "מטה טכנולוגי", "accelerator": "מאיץ"
}

he["modals"]["signal"]["title"] = "ממצא מודיעיני"
he["modals"]["signal"]["soundAlerts"] = "התראות קוליות"
he["modals"]["signal"]["dismiss"] = "סגור"
he["modals"]["signal"]["confidence"] = "רמת ביטחון"
he["modals"]["signal"]["country"] = "מדינה:"
he["modals"]["signal"]["scoreChange"] = "שינוי ציון:"
he["modals"]["signal"]["instabilityLevel"] = "רמת אי-יציבות:"
he["modals"]["signal"]["primaryDriver"] = "גורם מניע:"
he["modals"]["signal"]["location"] = "מיקום:"
he["modals"]["signal"]["eventTypes"] = "סוגי אירועים:"
he["modals"]["signal"]["eventCount"] = "מספר אירועים:"
he["modals"]["signal"]["eventCountValue"] = "{{count}} אירועים ב-24 שע'"
he["modals"]["signal"]["source"] = "מקור:"
he["modals"]["signal"]["countriesAffected"] = "מדינות מושפעות:"
he["modals"]["signal"]["impactLevel"] = "רמת השפעה:"
he["modals"]["signal"]["focalPoints"] = "נקודות מיקוד מתואמות"
he["modals"]["signal"]["newsCorrelation"] = "מתאם חדשותי"
he["modals"]["signal"]["viewOnMap"] = "הצג על המפה"
he["modals"]["signal"]["whyItMatters"] = "למה זה חשוב:"
he["modals"]["signal"]["action"] = "פעולה:"
he["modals"]["signal"]["note"] = "הערה:"
he["modals"]["signal"]["suppress"] = "השתק מונח זה"
he["modals"]["signal"]["suppressed"] = "הושתק"
he["modals"]["signal"]["predictionLeading"] = "חיזוי מוביל"
he["modals"]["signal"]["newsLeading"] = "חדשות מובילות"
he["modals"]["signal"]["silentDivergence"] = "סטייה שקטה"
he["modals"]["signal"]["velocitySpike"] = "קפיצת מהירות"
he["modals"]["signal"]["keywordSpike"] = "קפיצת מילות מפתח"
he["modals"]["signal"]["convergence"] = "התכנסות"
he["modals"]["signal"]["triangulation"] = "טריאנגולציה"
he["modals"]["signal"]["flowDrop"] = "ירידת זרימה"
he["modals"]["signal"]["flowPriceDivergence"] = "סטיית זרימה/מחיר"
he["modals"]["signal"]["geoConvergence"] = "התכנסות גיאוגרפית"
he["modals"]["signal"]["marketMove"] = "תנועת שוק מוסברת"
he["modals"]["signal"]["sectorCascade"] = "מפל מגזרי"
he["modals"]["signal"]["militarySurge"] = "עלייה צבאית"

he["modals"]["story"] = {
    "generating": "מייצר סיפור...", "close": "סגור",
    "shareTitle": "שתף סיפור", "save": "שמור",
    "whatsapp": "WhatsApp", "twitter": "X", "linkedin": "LinkedIn",
    "copyLink": "קישור", "saved": "נשמר!", "copied": "הועתק!",
    "opening": "פותח...", "error": "יצירת הסיפור נכשלה."
}

he["modals"]["mobileWarning"] = {
    "title": "תצוגת מובייל",
    "description": "אתם צופים בגרסה מובנית למובייל המתמקדת באזור המזרח התיכון עם שכבות חיוניות.",
    "tip": "טיפ: השתמשו בכפתורי התצוגה (גלובלי/ארה\"ב/מזה\"ת) למעבר בין אזורים. לחצו על סמנים לפרטים.",
    "dontShowAgain": "אל תציג שוב",
    "gotIt": "הבנתי"
}

he["modals"]["downloadBanner"] = {
    "title": "אפליקציית שולחן עבודה זמינה",
    "description": "ביצועים מקומיים, אחסון מפתחות מאובטח, אריחי מפה לא מקוונים.",
    "macSilicon": "macOS (Apple Silicon)", "macIntel": "macOS (Intel)",
    "windows": "Windows (.exe)", "linux": "Linux (.AppImage)",
    "showAllPlatforms": "הצג את כל הפלטפורמות",
    "showLess": "הצג פחות", "dismiss": "סגור"
}

# ── Components ──
he["components"]["webcams"] = {
    "expand": "הרחב", "paused": "מצלמות מושהות",
    "pausedIdle": "מצלמות מושהות, הזיזו את העכבר לחידוש",
    "regions": {
        "iran": "תקיפות איראן", "all": "הכל", "mideast": "מזה\"ת",
        "europe": "אירופה", "americas": "אמריקה", "asia": "אסיה"
    }
}

he["components"]["monitor"] = {
    "placeholder": "מילות מפתח (מופרדות בפסיקים)",
    "add": "+ הוסף מוניטור",
    "addKeywords": "הוסיפו מילות מפתח למעקב אחר חדשות",
    "noMatches": "אין התאמות ב-{{count}} כתבות",
    "showingMatches": "מציג {{count}} מתוך {{total}} התאמות",
    "match": "התאמה", "matches": "התאמות"
}

he["components"]["economic"] = {
    "indicators": "מדדים", "oil": "נפט", "gov": "ממשל",
    "noData": "אין נתונים כלכליים זמינים",
    "noOilData": "נתוני נפט לא זמינים",
    "noOilMetrics": "אין מדדי נפט זמינים. הוסיפו EIA_API_KEY להפעלה.",
    "noSpending": "אין הוצאות ממשלתיות אחרונות",
    "awards": "חוזים",
    "noIndicatorData": "אין נתוני מדדים עדיין, FRED עשוי להיטען",
    "fredKeyMissing": "נדרש מפתח FRED API, הוסיפו אותו בהגדרות להפעלת מדדים כלכליים",
    "noOilDataRetry": "נתוני נפט לא זמינים זמנית, ינסה שוב",
    "vsPreviousWeek": "לעומת השבוע הקודם",
    "in": "ב-",
    "centralBanks": "בנקים מרכזיים",
    "noBisData": "נתוני BIS לא זמינים זמנית, ינסה שוב",
    "policyRate": "ריבית מדיניות", "exchangeRate": "שער חליפין",
    "creditToGdp": "אשראי / תמ\"ג", "realEer": "שער חליפין אפקטיבי ריאלי",
    "change": "שינוי", "cut": "הורדה", "hike": "העלאה", "hold": "ללא שינוי"
}

# OREF Sirens - critical section for Magen
he["components"]["orefSirens"] = {
    "checking": "בודק התראות צפירה...",
    "noAlerts": "אין צפירות פעילות, הכל תקין",
    "notConfigured": "שירות הצפירות לא מוגדר",
    "activeSirens": "{{count}} צפירות פעילות",
    "area": "אזור",
    "time": "זמן",
    "justNow": "עכשיו",
    "historyCount": "{{count}} התראות ב-24 השעות האחרונות",
    "historySummary": "{{count}} התראות ב-24 שע', {{waves}} גלים",
    "loadingHistory": "טוען היסטוריה...",
    "infoTooltip": "<strong>צפירות ישראל</strong><br>התראות טילים וצפירות בזמן אמת מפיקוד העורף.<br><br>הנתונים נבדקים כל 10 שניות. מחוון אדום מהבהב מציין צפירות פעילות."
}

# Telegram Intel
he["components"]["telegramIntel"] = {
    "infoTooltip": "אותות בזמן אמת מערוצי טלגרם OSINT במעקב",
    "loading": "מתחבר לממסר טלגרם...",
    "empty": "אין הודעות זמינות",
    "disabled": "ממסר טלגרם לא פעיל",
    "filterAll": "הכל",
    "filterBreaking": "דחוף",
    "filterConflict": "סכסוך",
    "filterAlerts": "התראות",
    "filterOsint": "OSINT",
    "filterPolitics": "פוליטיקה",
    "filterMiddleeast": "המזרח התיכון"
}

# Insights
he["components"]["insights"] = {
    "noStories": "אין עדיין סיפורים דחופים או רב-מקוריים",
    "step": "שלב {{step}}/{{total}}",
    "waitingForData": "ממתין לנתוני חדשות...",
    "rankingStories": "מדרג סיפורים חשובים...",
    "analyzingSentiment": "מנתח סנטימנט...",
    "generatingBrief": "מייצר תדריך עולמי...",
    "infoTooltip": he["components"]["insights"]["infoTooltip"],  # keep HTML tooltip in English
    "settingsTitle": "הגדרות",
    "sectionMap": "מפה",
    "sectionAi": "ניתוח AI",
    "sectionStreaming": "שידור",
    "streamQualityLabel": "איכות וידאו",
    "streamQualityDesc": "הגדירו איכות לכל השידורים החיים (נמוך יותר חוסך רוחב פס)",
    "mapFlashLabel": "פולס אירוע חי",
    "mapFlashDesc": "הבהב מיקומים על המפה כשמגיעות חדשות דחופות",
    "aiFlowTitle": "הגדרות",
    "aiFlowCloudLabel": "AI ענן (Groq ו-OpenRouter)",
    "aiFlowCloudDesc": "שלחו כותרות לענן לסיכום AI (מומלץ)",
    "aiFlowBrowserLabel": "מודל מקומי בדפדפן",
    "aiFlowBrowserDesc": "הריצו AI מקומית בדפדפן",
    "aiFlowBrowserWarn": "מוריד כ-250 MB של נתוני מודל לדפדפן",
    "aiFlowOllamaCta": "רוצים AI מקומי לחלוטין?",
    "aiFlowOllamaCtaDesc": "הורידו את אפליקציית השולחן עבודה לתמיכה ב-Ollama",
    "aiFlowDownloadDesktop": "הורד אפליקציית שולחן עבודה",
    "aiFlowStatusActive": "AI ענן פעיל",
    "aiFlowStatusCloudAndBrowser": "AI ענן + מודל דפדפן פעילים",
    "aiFlowStatusBrowserOnly": "מודל דפדפן בלבד",
    "aiFlowStatusDisabled": "אין ספקי AI פעילים",
    "insightsDisabledTitle": "ניתוח AI מושבת",
    "insightsDisabledHint": "הפעילו ספקים דרך גלגל ההגדרות בכותרת המפה",
    "sectionPanels": "פאנלים",
    "badgeAnimLabel": "אנימציות תגים",
    "badgeAnimDesc": "הנפשת תגי עדכון בכותרות פאנלים",
    "sectionIntelligence": "מודיעין",
    "headlineMemoryLabel": "זיכרון כותרות",
    "headlineMemoryDesc": "זכור כותרות שנצפו כדי להדגיש סיפורים חדשים"
}

# Strategic Posture
he["components"]["strategicPosture"]["scanningTheaters"] = "סורק זירות"
he["components"]["strategicPosture"]["positions"] = "מיקומי מטוסים"
he["components"]["strategicPosture"]["navalVesselsLoading"] = "כלי שיט צבאיים"
he["components"]["strategicPosture"]["theaterAnalysis"] = "ניתוח זירה"
he["components"]["strategicPosture"]["connectingStreams"] = "מתחבר לזרמי ADS-B ו-AIS חיים..."
he["components"]["strategicPosture"]["initialLoadNote"] = "טעינה ראשונית לוקחת 30-60 שניות בזמן שנתוני מעקב מצטברים"
he["components"]["strategicPosture"]["acquiringData"] = "רוכש נתונים"
he["components"]["strategicPosture"]["acquiringDesc"] = "מתחבר לרשת ADS-B לנתוני טיסות צבאיות. עשוי לקחת 30-60 שניות בטעינה ראשונה."
he["components"]["strategicPosture"]["retryNow"] = "נסה שוב עכשיו"
he["components"]["strategicPosture"]["feedRateLimited"] = "פיד מוגבל קצב"
he["components"]["strategicPosture"]["rateLimitedDesc"] = "ל-OpenSky API יש מגבלות בקשות. הפאנל ינסה שוב אוטומטית בעוד מספר דקות."
he["components"]["strategicPosture"]["tryAgain"] = "נסה שוב"
he["components"]["strategicPosture"]["elapsed"] = "חלפו: {{elapsed}} שנ'"
he["components"]["strategicPosture"]["clickToView"] = "לחצו לצפייה ב-{{name}} על המפה"
he["components"]["strategicPosture"]["clickToViewMap"] = "לחצו לצפייה על המפה"
he["components"]["strategicPosture"]["refresh"] = "רענן"
he["components"]["strategicPosture"]["units"] = {
    "fighters": "מטוסי קרב", "tankers": "מטוסי תדלוק",
    "awacs": "AWACS", "recon": "סיור", "transport": "תובלה",
    "bombers": "מפציצים", "drones": "כטב\"מ", "aircraft": "מטוסים",
    "carriers": "נושאות מטוסים", "destroyers": "משחתות",
    "frigates": "פריגטות", "submarines": "צוללות",
    "patrol": "סיור", "auxiliary": "עזר", "navalVessels": "כלי שיט צבאיים"
}
he["components"]["strategicPosture"]["badges"] = {"critical": "קריטי", "elevated": "מוגבר", "normal": "רגיל"}
he["components"]["strategicPosture"]["trendStable"] = "יציב"
he["components"]["strategicPosture"]["domains"] = {"air": "אוויר", "sea": "ים"}
he["components"]["strategicPosture"]["strike"] = "תקיפה"
he["components"]["strategicPosture"]["staleWarning"] = "משתמש בנתונים מהמטמון, פיד חי לא זמין זמנית"
he["components"]["strategicPosture"]["updated"] = "עודכן:"
he["components"]["strategicPosture"]["theaters"] = {
    "iran-theater": "זירת איראן",
    "taiwan-theater": "מיצר טייוואן",
    "baltic-theater": "זירת הבלטיק",
    "blacksea-theater": "הים השחור",
    "korea-theater": "חצי האי הקוריאני",
    "south-china-sea": "ים סין הדרומי",
    "east-med-theater": "מזרח הים התיכון",
    "israel-gaza-theater": "ישראל/עזה",
    "yemen-redsea-theater": "תימן/ים סוף"
}

# Strategic Risk
he["components"]["strategicRisk"] = {
    "noRisks": "לא זוהו סיכונים משמעותיים",
    "levels": {"critical": "קריטי", "elevated": "מוגבר", "moderate": "מתון", "low": "נמוך"},
    "trend": "מגמה",
    "trends": {"escalating": "מסלים", "deEscalating": "מתמתן", "stable": "יציב"},
    "insufficientData": "נתונים לא מספיקים",
    "unableToAssess": "לא ניתן להעריך רמת סיכון.",
    "enableDataSources": "הפעילו מקורות נתונים להתחלת ניטור.",
    "requiredDataSources": "מקורות נתונים נדרשים",
    "optionalSources": "מקורות אופציונליים",
    "enableCoreFeeds": "הפעל פידים מרכזיים",
    "waitingForData": "ממתין לנתונים...",
    "refresh": "רענן",
    "learningMode": "מצב למידה, {{minutes}} דק' עד מהימנות",
    "noData": "אין נתונים",
    "enable": "הפעל",
    "convergenceMetric": "התכנסות",
    "ciiDeviation": "סטיית CII",
    "infraEvents": "אירועי תשתית",
    "highAlerts": "התראות גבוהות",
    "topRisks": "סיכונים מובילים",
    "recentAlerts": "התראות אחרונות ({{count}})",
    "updated": "עודכן: {{time}}",
    "time": {"justNow": "עכשיו", "minutesAgo": "לפני {{count}} דק'", "hoursAgo": "לפני {{count}} שע'"},
    "infoTooltip": he["components"]["strategicRisk"]["infoTooltip"]  # keep complex HTML in English
}

# Security Advisories
he["components"]["securityAdvisories"] = {
    "loading": "טוען אזהרות נסיעה...",
    "noMatching": "אין אזהרות התואמות לסינון זה",
    "critical": "קריטי", "health": "בריאות",
    "sources": "US State Dept, AU DFAT, UK FCDO, NZ MFAT, CDC, ECDC, WHO, שגרירויות ארה\"ב",
    "refresh": "רענן",
    "levels": {
        "doNotTravel": "איסור נסיעה", "reconsider": "שקלו מחדש נסיעה",
        "caution": "נקטו זהירות", "normal": "רגיל", "info": "מידע"
    },
    "time": {
        "justNow": "עכשיו", "minutesAgo": "לפני {{count}} דק'",
        "hoursAgo": "לפני {{count}} שע'", "daysAgo": "לפני {{count}} ימים"
    },
    "infoTooltip": he["components"]["securityAdvisories"]["infoTooltip"]  # keep HTML tooltip
}

# Cascade
he["components"]["cascade"] = {
    "noImpacts": "לא זוהו השפעות על מדינות",
    "filters": {"cables": "כבלים", "pipelines": "צינורות", "ports": "נמלים", "chokepoints": "צווארי בקבוק"},
    "filterType": {"cable": "כבל", "pipeline": "צינור", "port": "נמל", "chokepoint": "צוואר בקבוק", "country": "מדינה"},
    "selectPrompt": "בחרו {{type}}...",
    "analyzeImpact": "נתח השפעה",
    "impactLevels": {"critical": "קריטי", "high": "גבוה", "medium": "בינוני", "low": "נמוך"},
    "capacityPercent": "{{percent}}% קיבולת",
    "noCountryImpacts": "לא זוהו השפעות על מדינות",
    "alternativeRoutes": "מסלולים חלופיים",
    "countriesAffected": "מדינות מושפעות ({{count}})",
    "links": "קישורים",
    "selectInfrastructureHint": "בחרו תשתית לניתוח מפל השפעות",
    "infoTooltip": he["components"]["cascade"]["infoTooltip"]  # keep HTML
}

# DeckGL / Map
he["components"]["deckgl"] = {
    "zoomIn": "הגדל",
    "zoomOut": "הקטן",
    "resetView": "אפס תצוגה",
    "legend": {
        "title": "מקרא",
        "startupHub": "מרכז סטארטאפים", "techHQ": "מטה טכנולוגי",
        "accelerator": "מאיץ", "cloudRegion": "אזור ענן",
        "datacenter": "מרכז נתונים", "stockExchange": "בורסה",
        "financialCenter": "מרכז פיננסי", "centralBank": "בנק מרכזי",
        "commodityHub": "מרכז סחורות", "waterway": "מסלול מים",
        "highAlert": "התראה גבוהה", "elevated": "מוגבר",
        "monitoring": "ניטור", "base": "בסיס", "nuclear": "גרעיני"
    },
    "layerGuide": "מדריך שכבות",
    "layersTitle": "שכבות",
    "timeAll": "הכל",
    "views": {
        "global": "גלובלי", "americas": "אמריקה", "mena": "מזה\"ת",
        "europe": "אירופה", "asia": "אסיה", "latam": "אמריקה הלטינית",
        "africa": "אפריקה", "oceania": "אוקיאניה"
    },
    "layers": {
        "startupHubs": "מרכזי סטארטאפים", "techHQs": "מטות טכנולוגיים",
        "accelerators": "מאיצים", "cloudRegions": "אזורי ענן",
        "aiDataCenters": "מרכזי נתונים AI", "underseaCables": "כבלים תת-ימיים",
        "internetOutages": "תקלות אינטרנט", "cyberThreats": "איומי סייבר",
        "techEvents": "אירועי טכנולוגיה", "naturalEvents": "אירועי טבע",
        "fires": "שריפות", "intelHotspots": "מוקדי מודיעין",
        "conflictZones": "אזורי סכסוך", "militaryBases": "בסיסים צבאיים",
        "nuclearSites": "אתרים גרעיניים", "gammaIrradiators": "מקריני גמא",
        "spaceports": "נמלי חלל", "pipelines": "צינורות",
        "militaryActivity": "פעילות צבאית", "shipTraffic": "תנועת ספינות",
        "flightDelays": "עיכובי טיסות", "protests": "הפגנות",
        "ucdpEvents": "אירועי סכסוך מזוין", "displacementFlows": "תנועות עקירה",
        "climateAnomalies": "חריגות אקלים", "weatherAlerts": "התראות מזג אוויר",
        "strategicWaterways": "מסלולי מים אסטרטגיים",
        "economicCenters": "מרכזים כלכליים", "criticalMinerals": "מינרלים קריטיים",
        "stockExchanges": "בורסות", "financialCenters": "מרכזים פיננסיים",
        "centralBanks": "בנקים מרכזיים", "commodityHubs": "מרכזי סחורות",
        "gulfInvestments": "השקעות GCC", "tradeRoutes": "מסלולי סחר",
        "iranAttacks": "תקיפות איראן", "gpsJamming": "שיבוש GPS",
        "dayNight": "יום/לילה"
    },
    "tooltip": {
        "earthquake": "רעידת אדמה", "militaryAircraft": "מטוס צבאי",
        "vesselCluster": "קבוצת כלי שיט", "vessels": "כלי שיט",
        "flightCluster": "קבוצת טיסות", "aircraft": "מטוסים",
        "protest": "הפגנה", "protestsCount": "{{count}} הפגנות",
        "techHQsCount": "{{count}} מטות טכנולוגיים",
        "techEventsCount": "{{count}} אירועי טכנולוגיה",
        "dataCentersCount": "{{count}} מרכזי נתונים",
        "underseaCable": "כבל תת-ימי", "pipeline": "צינור",
        "conflictZone": "אזור סכסוך", "naturalEvent": "אירוע טבע",
        "financialCenter": "מרכז פיננסי", "port": "נמל",
        "disruption": "שיבוש", "advisory": "אזהרה",
        "repairShip": "ספינת תיקון", "internetOutage": "תקלת אינטרנט",
        "medium": "בינוני", "news": "חדשות",
        "undisclosed": "לא פורסם", "stake": "אחזקה"
    }
}
# Keep layerHelp in English (too complex with HTML)

# CII
he["components"]["cii"] = {
    "shareStory": "שתף סיפור",
    "noSignals": "לא זוהו אותות אי-יציבות",
    "infoTooltip": he["components"]["cii"]["infoTooltip"]  # keep HTML
}

# News Panel
he["components"]["newsPanel"] = {
    "close": "סגור",
    "summarize": "סכם פאנל זה",
    "generatingSummary": "מייצר סיכום...",
    "sources": "{{count}} מקורות",
    "relatedAssetsNear": "נכסים קשורים ליד {{location}}"
}

# Breaking News
he["components"]["breakingNews"] = {
    "critical": "קריטי", "high": "גבוה",
    "dismiss": "סגור", "enableNotifications": "הפעל התראות שולחן עבודה"
}

# Intelligence Findings
he["components"]["intelligenceFindings"] = {
    "breakingAlerts": "התראות דחופות",
    "popupAlerts": "הצג התראות חדשות",
    "badgeTitle": "ממצאים מודיעיניים",
    "title": "ממצאים מודיעיניים",
    "none": "אין ממצאים מודיעיניים אחרונים",
    "monitoring": "ניטור",
    "scanning": "סורק מתאמים וחריגות...",
    "reviewRecommended": "{{count}} ממצאים מודיעיניים, מומלץ לבדוק",
    "count": "{{count}} ממצא מודיעיני",
    "detected": "{{count}} זוהו",
    "critical": "{{count}} קריטיים",
    "highPriority": "{{count}} עדיפות גבוהה",
    "hideFindings": "הסתר ממצאים",
    "more": "+{{count}} ממצאים נוספים",
    "all": "כל הממצאים המודיעיניים ({{count}})",
    "priority": {"critical": "קריטי", "high": "גבוה", "medium": "בינוני", "low": "נמוך"},
    "insights": {
        "criticalDestabilization": "ערעור יציבות קריטי, דורש תשומת לב מיידית",
        "significantShift": "שינוי משמעותי, עקבו מקרוב",
        "developingSituation": "מצב מתפתח, עקבו לאיתור הסלמה",
        "convergence": "ריבוי אירועים מתקבצים באזור",
        "cascade": "שיבוש תשתיות מתפשט",
        "review": "סקירה למודעות מצבית"
    },
    "time": {
        "justNow": "עכשיו", "minutesAgo": "לפני {{count}} דק'",
        "hoursAgo": "לפני {{count}} שע'", "daysAgo": "לפני {{count}} ימים"
    }
}

# Playback
he["components"]["playback"] = {
    "toggleMode": "החלף מצב ניגון",
    "live": "שידור חי", "historicalPlayback": "ניגון היסטורי",
    "close": "סגור", "skipToStart": "דלג להתחלה",
    "previous": "הקודם", "next": "הבא", "skipToEnd": "דלג לסוף"
}

# Map show/hide
he["components"]["map"] = {"showMap": "הצג מפה", "hideMap": "הסתר מפה"}

# Live News
he["components"]["liveNews"] = {
    "retry": "נסה שוב",
    "notLive": "{{name}} לא משדר כרגע",
    "cannotEmbed": "לא ניתן להשמיע את {{name}} כאן, ייתכן שמוגבל באזורך (שגיאה {{code}})",
    "botCheck": "YouTube מבקש התחברות להשמעת {{name}}",
    "signInToYouTube": "התחבר ל-YouTube",
    "openOnYouTube": "פתח ב-YouTube",
    "manage": "ניהול ערוצים",
    "addChannel": "הוסף ערוץ",
    "remove": "הסר",
    "youtubeHandle": "כינוי YouTube (למשל @Channel)",
    "youtubeHandleOrUrl": "כינוי YouTube או כתובת",
    "displayName": "שם תצוגה (אופציונלי)",
    "openPanelSettings": "הגדרות תצוגת פאנל",
    "channelSettings": "הגדרות ערוץ",
    "save": "שמור", "cancel": "ביטול",
    "confirmDelete": "למחוק ערוץ זה?",
    "confirmTitle": "אישור",
    "restoreDefaults": "שחזר ערוצי ברירת מחדל",
    "availableChannels": "ערוצים זמינים",
    "customChannel": "ערוץ מותאם אישית",
    "regionAll": "הכל",
    "regionNorthAmerica": "צפון אמריקה",
    "regionEurope": "אירופה",
    "regionLatinAmerica": "אמריקה הלטינית",
    "regionAsia": "אסיה",
    "regionMiddleEast": "המזרח התיכון",
    "regionAfrica": "אפריקה",
    "regionOceania": "אוקיאניה",
    "invalidHandle": "הזינו כינוי YouTube חוקי (למשל @ChannelName)",
    "channelNotFound": "ערוץ YouTube לא נמצא",
    "verifying": "מאמת..."
}

# Predictions
he["components"]["predictions"] = {
    "tooltip": he["components"]["predictions"]["tooltip"],  # keep HTML
    "error": "טעינת חיזויים נכשלה",
    "yes": "כן", "no": "לא", "vol": "נפח", "closes": "נסגר"
}

# Panel generic
he["components"]["panel"] = {
    "showMethodologyInfo": "הצג מידע מתודולוגי",
    "dragToResize": "גררו לשינוי גודל (לחיצה כפולה לאיפוס)",
    "openSettings": "פתח הגדרות"
}

# Language Selector
he["components"]["languageSelector"] = {"selectLanguage": "בחרו שפה"}

# Verification
he["components"]["verification"] = {
    "title": "רשימת אימות מידע",
    "hint": "מבוסס על מסגרת OSH של Bellingcat",
    "verdicts": {"verified": "מאומת", "likely": "ככל הנראה אותנטי", "uncertain": "לא ודאי", "unreliable": "לא אמין"},
    "notesTitle": "הערות אימות",
    "noNotes": "לא נוספו הערות",
    "addNotePlaceholder": "הוסיפו הערת אימות...",
    "add": "הוסף",
    "resetChecklist": "אפס רשימה",
    "checks": {
        "recency": "חותמת זמן עדכנית אושרה", "geolocation": "מיקום אומת",
        "source": "מקור ראשוני זוהה", "crossref": "הוצלב עם מקורות אחרים",
        "noAi": "אין סימני יצירת AI", "noRecrop": "לא צילום ממוחזר/ישן",
        "metadata": "מטא-נתונים אומתו", "context": "הקשר הוגדר"
    }
}

# Export
he["components"]["export"] = {"exportData": "ייצוא נתונים"}

# Community
he["components"]["community"] = {
    "joinDiscussion": "הצטרפו לדיון",
    "openDiscussion": "פתח דיון",
    "dontShowAgain": "אל תציג שוב"
}

# Threat Labels
he["components"]["threatLabels"] = {
    "critical": "קריטי", "high": "גבוה", "medium": "בינוני", "low": "נמוך", "info": "מידע"
}

# ── Popups ──
he["popups"]["startDate"] = "תאריך התחלה"
he["popups"]["endDate"] = "תאריך סיום"
he["popups"]["magnitude"] = "עוצמה"
he["popups"]["depth"] = "עומק"
he["popups"]["intensity"] = "עצימות"
he["popups"]["type"] = "סוג"
he["popups"]["status"] = "סטטוס"
he["popups"]["severity"] = "חומרה"
he["popups"]["location"] = "מיקום"
he["popups"]["coordinates"] = "קואורדינטות"
he["popups"]["casualties"] = "נפגעים"
he["popups"]["displaced"] = "עקורים"
he["popups"]["belligerents"] = "צדדים לוחמים"
he["popups"]["keyDevelopments"] = "התפתחויות מרכזיות"
he["popups"]["unknown"] = "לא ידוע"
he["popups"]["source"] = "מקור"
he["popups"]["target"] = "מטרה"
he["popups"]["events"] = "אירועים"
he["popups"]["impact"] = "השפעה"
he["popups"]["capacity"] = "קיבולת"
he["popups"]["alerts"] = "התראות פעילות"
he["popups"]["updated"] = "עודכן"
he["popups"]["common"] = {"start": "התחלה", "end": "סיום", "updated": "עודכן"}
he["popups"]["conflict"]["title"] = "אזור סכסוך"
he["popups"]["earthquake"]["levels"] = {"major": "חזק", "moderate": "בינוני", "minor": "קל"}
he["popups"]["base"]["types"] = {"us-nato": "ארה\"ב/נאט\"ו", "china": "סין", "russia": "רוסיה"}
he["popups"]["protest"] = {
    "acledVerified": "ACLED (מאומת)", "gdelt": "GDELT",
    "riots": "מהומות", "highSeverity": "חומרה גבוהה"
}
he["popups"]["gpsJamming"] = {
    "title": "הפרעת GPS/GNSS", "interference": "הפרעה",
    "aircraftAffected": "מטוסים מושפעים", "aircraftNormal": "מטוסים תקינים",
    "h3Hex": "משושה H3"
}
he["popups"]["strategic"] = "אסטרטגי"
he["popups"]["verified"] = "מאומת"
he["popups"]["sampledList"] = "מציג רשימה מדגמית של {{count}} אירועים."
he["popups"]["reason"] = "סיבה"
he["popups"]["threat"] = "איום"
he["popups"]["aka"] = "ידוע גם כ-"
he["popups"]["sponsor"] = "חסות"
he["popups"]["origin"] = "מקור"
he["popups"]["country"] = "מדינה"
he["popups"]["lastSeen"] = "נצפה לאחרונה"
he["popups"]["open"] = "פתוח"
he["popups"]["tradingHours"] = "שעות מסחר"
he["popups"]["city"] = "עיר"
he["popups"]["length"] = "אורך"
he["popups"]["operator"] = "מפעיל"
he["popups"]["countries"] = "מדינות"
he["popups"]["near"] = "ליד"
he["popups"]["moreEvents"] = "אירועים נוספים"
he["popups"]["monitoring"] = "ניטור"
he["popups"]["expired"] = "פג תוקף"
he["popups"]["timeAgo"] = {
    "s": "לפני {{count}} שנ'",
    "m": "לפני {{count}} דק'",
    "h": "לפני {{count}} שע'",
    "d": "לפני {{count}} ימים"
}
he["popups"]["region"] = "אזור"
he["popups"]["fatalities"] = "הרוגים"
he["popups"]["actors"] = "שחקנים"
he["popups"]["time"] = "זמן"
he["popups"]["area"] = "אזור"

he["popups"]["hotspot"] = {
    "escalation": "הערכת הסלמה",
    "baseline": "קו בסיס", "score": "ציון", "trend": "מגמה",
    "components": {"news": "חדשות", "cii": "CII", "geo": "גיאו", "military": "צבאי"},
    "levels": {"stable": "יציב", "watch": "מעקב", "elevated": "מוגבר", "high": "גבוה", "critical": "קריטי"}
}

he["popups"]["buttons"] = {"track": "עקוב אחר נושא", "details": "צפה בפרטים"}
he["popups"]["historicalContext"] = "הקשר היסטורי"
he["popups"]["lastMajorEvent"] = "אירוע משמעותי אחרון"
he["popups"]["precedents"] = "תקדימים"
he["popups"]["cyclicalPattern"] = "דפוס מחזורי"
he["popups"]["whyItMatters"] = "למה זה חשוב"
he["popups"]["keyEntities"] = "ישויות מרכזיות"
he["popups"]["relatedHeadlines"] = "כותרות קשורות"
he["popups"]["liveIntel"] = "מודיעין חי"
he["popups"]["loadingNews"] = "טוען חדשות גלובליות..."
he["popups"]["noCoverage"] = "אין כיסוי גלובלי עדכני"

# ── Alerts ──
he["alerts"] = {
    "instabilityRising": "{{country}} אי-יציבות עולה",
    "instabilityFalling": "{{country}} אי-יציבות יורדת",
    "indexRose": "מדד אי-יציבות עלה מ-{{from}} ל-{{to}} ({{change}}). גורם: {{driver}}",
    "indexFell": "מדד אי-יציבות ירד מ-{{from}} ל-{{to}} ({{change}}). גורם: {{driver}}",
    "geoAlert": "התראה גיאוגרפית: {{location}}",
    "cascadeAlert": "התראת מפל תשתיות",
    "infraAlert": "התראת תשתיות: {{name}}",
    "countriesAffected": "{{count}} מדינות מושפעות, השפעה גבוהה ביותר: {{impact}}",
    "alert": "התראה: {{location}}",
    "multipleRegions": "מספר אזורים",
    "trending": "\"{{term}}\" במגמה, {{count}} אזכורים ב-{{hours}} שע'",
    "eventsDetected": "{{count}} אירועים זוהו באזור ({{lat}}°, {{lon}}°)"
}

# ── Intel Topics ──
he["intel"]["topics"] = {
    "military": {"name": "פעילות צבאית", "description": "תרגילים, פריסות ומבצעים צבאיים"},
    "cyber": {"name": "איומי סייבר", "description": "מתקפות סייבר, כופרה ואיומים דיגיטליים"},
    "nuclear": {"name": "גרעין", "description": "תוכניות גרעין, ביקורות IAEA, הפצה"},
    "sanctions": {"name": "סנקציות", "description": "סנקציות כלכליות והגבלות סחר"},
    "intelligence": {"name": "מודיעין", "description": "ריגול, פעולות מודיעין, מעקב"},
    "maritime": {"name": "ביטחון ימי", "description": "פעולות ימיות, צווארי בקבוק ימיים, נתיבי שיט"}
}

# ── Common ──
he["common"] = {
    "loading": "טוען...",
    "error": "שגיאה",
    "noData": "אין נתונים זמינים",
    "noDataAvailable": "אין נתונים זמינים",
    "updated": "עודכן הרגע",
    "ago": "לפני {{time}}",
    "retrying": "מנסה שוב...",
    "failedToLoad": "טעינת נתונים נכשלה",
    "noDataShort": "אין נתונים",
    "upstreamUnavailable": "API חיצוני לא זמין, ינסה שוב אוטומטית",
    "loadingUcdpEvents": "טוען אירועי סכסוך מזוין",
    "loadingStablecoins": "טוען מטבעות יציבים...",
    "scanningThermalData": "סורק נתונים תרמיים",
    "calculatingExposure": "מחשב חשיפה",
    "computingSignals": "מחשב אותות...",
    "loadingEtfData": "טוען נתוני ETF...",
    "loadingGiving": "טוען נתוני תרומות גלובליות",
    "loadingDisplacement": "טוען נתוני עקירה",
    "loadingClimateData": "טוען נתוני אקלים",
    "failedTechReadiness": "טעינת נתוני מוכנות טכנולוגית נכשלה",
    "failedRiskOverview": "חישוב סקירת סיכונים נכשל",
    "failedPredictions": "טעינת חיזויים נכשלה",
    "failedCII": "חישוב CII נכשל",
    "failedDependencyGraph": "בניית גרף תלויות נכשלה",
    "failedIntelFeed": "טעינת פיד מודיעין נכשלה",
    "failedMarketData": "טעינת נתוני שוק נכשלה",
    "failedSectorData": "טעינת נתוני מגזר נכשלה",
    "failedCommodities": "טעינת סחורות נכשלה",
    "failedCryptoData": "טעינת נתוני קריפטו נכשלה",
    "rateLimitedMarket": "נתוני שוק לא זמינים זמנית (הגבלת קצב), ינסה שוב בקרוב",
    "failedClusterNews": "קיבוץ חדשות נכשל",
    "noNewsAvailable": "אין חדשות זמינות",
    "noActiveTechHubs": "אין מרכזי טכנולוגיה פעילים",
    "noActiveGeoHubs": "אין מוקדים גיאופוליטיים פעילים",
    "allSourcesDisabled": "כל המקורות מושבתים",
    "allIntelSourcesDisabled": "כל מקורות המודיעין מושבתים",
    "noEventsInCategory": "אין אירועים בקטגוריה זו",
    "exportCsv": "ייצוא CSV",
    "exportJson": "ייצוא JSON",
    "exportData": "ייצוא נתונים",
    "selectAll": "בחר הכל",
    "selectNone": "בטל בחירה",
    "unrest": "אי-שקט",
    "conflict": "סכסוך",
    "security": "ביטחון",
    "information": "מידע",
    "shareStory": "שתף סיפור",
    "exportImage": "ייצוא תמונה",
    "exportPdf": "ייצוא PDF",
    "new": "חדש",
    "live": "שידור חי",
    "cached": "מטמון",
    "unavailable": "לא זמין",
    "close": "סגור",
    "currentVariant": "(נוכחי)",
    "retry": "נסה שוב",
    "refresh": "רענן",
    "all": "הכל"
}

# ── Magen-specific keys (not in en.json) ──
he["magen"] = {
    "credits": {
        "basedOn": "מבוסס על",
        "by": "מאת",
        "visualInspiration": "השראה ויזואלית",
        "license": "רישיון",
        "sourceCode": "קוד מקור",
        "builtWithLove": "נבנה באהבה עבור אזרחי ישראל."
    }
}

# ── Write the file ──
with open(he_path, "w", encoding="utf-8") as f:
    json.dump(he, f, ensure_ascii=False, indent=2)

print(f"Written {he_path} ({he_path.stat().st_size:,} bytes)")

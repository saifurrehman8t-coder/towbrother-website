# -*- coding: utf-8 -*-
"""
Tow Brothers website builder.

    python3 build.py

Reads src/content.py + src/style.css and writes the full static site to ./site
(upload the *contents* of ./site to your hosting).
Change phone / domain / socials in CONFIG below, then run again.
"""
import json
import os
import shutil
import sys
from datetime import date
from html import escape
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
from content import SERVICES, AREAS, GUIDES, ROUTES  # noqa: E402

# ---------------------------------------------------------------------------
# CONFIG — edit these
# ---------------------------------------------------------------------------
CONFIG = {
    "name": "Tow Brothers",
    "site": "https://towbrother.com",
    "phone_display": "0308 9176474",
    "phone_e164": "+923089176474",
    "whatsapp": "923089176474",
    "email": "",                                     # optional, e.g. info@towbrother.com
    "street": "Near Pepsi Warehouse, Hanjarwal",
    "city": "Lahore",
    "region": "Punjab",
    "postcode": "54500",
    "country": "PK",
    # Google Business Profile (from the shared Maps link)
    "maps_cid": int("7267f70a2fe86ed2", 16),
    "maps_query": "Tow Brothers, near papsi wherehouse, Hanjarwal, Lahore, 54500",
    "lat": None,                                     # optional: exact pin, e.g. 31.4800
    "lng": None,                                     # optional: exact pin, e.g. 74.2600
    "social": [],                                    # e.g. ["https://www.facebook.com/towbrothers"]
}
TODAY = date.today().isoformat()
OUT = os.path.join(ROOT, "site")
C = CONFIG
SITE = C["site"].rstrip("/")
MAPS_URL = "https://maps.google.com/?cid=%d" % C["maps_cid"]
MAPS_EMBED = "https://maps.google.com/maps?q=%s&z=15&output=embed" % quote(C["maps_query"])
TEL = "tel:" + C["phone_e164"]
WA = "https://wa.me/%s?text=%s" % (C["whatsapp"], quote("Hi Tow Brothers, I need car recovery. My location is: "))
ADDRESS_LINE = "%s, %s %s" % (C["street"], C["city"], C["postcode"])
BIZ_ID = SITE + "/#business"


def area_url(a):
    return "/car-recovery-%s-lahore/" % a["slug"]


def area_full(a):
    return a["name"] if "Lahore" in a["name"] else a["name"] + ", Lahore"


AREA_BY_SLUG = {a["slug"]: a for a in AREAS}
CORE = [s for s in SERVICES if s.get("group", "core") == "core"]
EXTRA = [s for s in SERVICES if s.get("group") == "keyword"]


def route_url(r):
    return "/car-transport-lahore-to-%s/" % r["slug"]


def route_pills():
    return '<ul class="area-links">%s</ul>' % "".join(
        '<li><a href="%s">Lahore to %s</a></li>' % (route_url(r), r["city"]) for r in ROUTES)


def service_pills(services):
    return '<ul class="area-links">%s</ul>' % "".join(
        '<li><a href="/%s/">%s Lahore</a></li>' % (s["slug"], s["name"]) for s in services)

# ---------------------------------------------------------------------------
# Icons (24x24 stroke icons)
# ---------------------------------------------------------------------------
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8v.5z"/>',
    "truck": '<rect x="1" y="3" width="15" height="13"/><path d="M16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    "hook": '<path d="M8 3h8M12 3v9"/><path d="M12 12a4 4 0 1 1-4 4"/>',
    "lift": '<path d="M12 18V5"/><path d="M5 12l7-7 7 7"/><path d="M4 21h16"/>',
    "road": '<path d="M4 21L8 3M20 21L16 3M12 4v2M12 10v3M12 17v3"/>',
    "alert": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
    "bike": '<circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6h3l-3.5 11.5M5.5 17.5L9 10h6M9 10L7 6H5"/>',
    "flatbed": '<path d="M1 16h15l3-4h4v4"/><circle cx="6" cy="18.5" r="2"/><circle cx="18" cy="18.5" r="2"/><path d="M3 12l2-3h6l2 3z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>',
    "route": '<circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "tag": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><path d="M7 7h.01"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONS[name])


LOGO_MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#ffc21a"/>'
             '<path d="M6 25h17V15h5l5 5v5h1v3H6z" fill="#0b1f3a"/><path d="M8 22l4-6h7l2 6z" fill="#fff"/>'
             '<circle cx="12" cy="29" r="3" fill="#0b1f3a" stroke="#ffc21a" stroke-width="1.5"/>'
             '<circle cx="29" cy="29" r="3" fill="#0b1f3a" stroke="#ffc21a" stroke-width="1.5"/>'
             '<rect x="25" y="17" width="4" height="3" rx=".5" fill="#9fd3ff"/></svg>')

TRUCK_ART = """<svg viewBox="0 0 640 360" role="img" aria-label="Tow Brothers flatbed recovery truck carrying a car in Lahore">
<rect x="0" y="300" width="640" height="60" fill="#1b355c"/>
<g fill="#ffc21a" opacity=".85"><rect x="20" y="327" width="60" height="6" rx="3"/><rect x="140" y="327" width="60" height="6" rx="3"/><rect x="260" y="327" width="60" height="6" rx="3"/><rect x="380" y="327" width="60" height="6" rx="3"/><rect x="500" y="327" width="60" height="6" rx="3"/></g>
<circle cx="560" cy="60" r="34" fill="#ffc21a" opacity=".18"/>
<rect x="44" y="214" width="380" height="20" rx="4" fill="#ffc21a"/>
<rect x="44" y="234" width="500" height="22" rx="4" fill="#0e2140"/>
<text x="70" y="229" font-family="Arial,Helvetica,sans-serif" font-size="13" font-weight="700" fill="#0b1f3a">TOW BROTHERS · 24/7 RECOVERY LAHORE</text>
<path d="M420 118h78c10 0 18 5 23 13l34 52c4 6 6 13 6 20v53H420z" fill="#ffc21a"/>
<path d="M440 134h52c6 0 11 3 14 8l26 40h-92z" fill="#9fd3ff"/>
<rect x="436" y="196" width="24" height="5" rx="2" fill="#0b1f3a"/>
<rect x="458" y="104" width="34" height="14" rx="5" fill="#ff7a1a"/>
<rect x="548" y="214" width="16" height="10" rx="3" fill="#fff6c2"/>
<path d="M86 210c4-24 18-40 44-46l40-30c10-7 22-10 34-10h70c14 0 26 5 36 14l32 28c24 3 40 16 44 40l2 4H84z" fill="#e8eef7"/>
<path d="M188 140h48v34h-78zM248 140h28c8 0 15 3 21 9l22 25h-71z" fill="#4c6a94"/>
<circle cx="146" cy="206" r="20" fill="#111"/><circle cx="146" cy="206" r="8" fill="#9aa5b4"/>
<circle cx="322" cy="206" r="20" fill="#111"/><circle cx="322" cy="206" r="8" fill="#9aa5b4"/>
<path d="M60 214l-28 30" stroke="#ffc21a" stroke-width="8" stroke-linecap="round"/>
<g fill="#111"><circle cx="128" cy="270" r="32"/><circle cx="216" cy="270" r="32"/><circle cx="488" cy="270" r="32"/></g>
<g fill="#c7cfdb"><circle cx="128" cy="270" r="13"/><circle cx="216" cy="270" r="13"/><circle cx="488" cy="270" r="13"/></g>
</svg>"""


# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------
def business_schema():
    s = {
        "@context": "https://schema.org",
        "@type": ["AutomotiveBusiness", "EmergencyService"],
        "@id": BIZ_ID,
        "name": C["name"],
        "alternateName": "Tow Brothers Car Recovery & Towing Lahore",
        "description": "24/7 car recovery, car towing and car lifter service in Lahore, with flatbed recovery, motorway recovery and inter-city car transport.",
        "url": SITE + "/",
        "telephone": C["phone_e164"],
        "image": SITE + "/assets/og-image.png",
        "logo": SITE + "/assets/logo-512.png",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": C["street"],
            "addressLocality": C["city"],
            "addressRegion": C["region"],
            "postalCode": C["postcode"],
            "addressCountry": C["country"],
        },
        "hasMap": MAPS_URL,
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        }],
        "areaServed": [{"@type": "City", "name": "Lahore"}] + [
            {"@type": "Place", "name": area_full(a)} for a in AREAS],
        "sameAs": [MAPS_URL] + C["social"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Car recovery and towing services in Lahore",
            "itemListElement": [{
                "@type": "Offer",
                "itemOffered": {"@type": "Service", "name": s["name"], "url": SITE + "/" + s["slug"] + "/"},
            } for s in SERVICES],
        },
    }
    if C["lat"] and C["lng"]:
        s["geo"] = {"@type": "GeoCoordinates", "latitude": C["lat"], "longitude": C["lng"]}
    if C["email"]:
        s["email"] = C["email"]
    return s


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website",
            "url": SITE + "/", "name": C["name"], "inLanguage": "en-PK", "publisher": {"@id": BIZ_ID}}


def breadcrumb_schema(crumbs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def service_schema(name, url, desc, area_name="Lahore"):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
            "description": desc, "url": SITE + url, "provider": {"@id": BIZ_ID},
            "areaServed": {"@type": "Place", "name": area_name},
            "availableChannel": {"@type": "ServiceChannel", "servicePhone": {
                "@type": "ContactPoint", "telephone": C["phone_e164"], "contactType": "emergency",
                "areaServed": "PK", "availableLanguage": ["English", "Urdu", "Punjabi"]}}}


# ---------------------------------------------------------------------------
# Layout pieces
# ---------------------------------------------------------------------------
NAV = [("Services", "/services/"), ("Areas", "/areas/"), ("Guides", "/blog/"),
       ("About", "/about/"), ("Contact", "/contact/")]


def cta_buttons(size=""):
    cls = " btn-lg" if size == "lg" else ""
    return ('<a class="btn btn-call%s" href="%s">%s Call %s</a>'
            '<a class="btn btn-wa%s" href="%s" rel="nofollow noopener" target="_blank">%s WhatsApp Us</a>'
            % (cls, TEL, icon("phone"), C["phone_display"], cls, WA, icon("chat")))


def header(path):
    links = "".join('<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if path.startswith(u) else "", n)
                    for n, u in NAV)
    return """<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>24/7 Car Recovery &amp; Towing in Lahore<span class="hide-sm"> · Flatbed · Lifter · Motorway</span></span><a href="%s">Call now: %s</a></div></div>
<header class="site-header"><div class="wrap">
<a class="logo" href="/" aria-label="Tow Brothers home">%s<span>Tow Brothers<small>Car Recovery Lahore</small></span></a>
<nav class="nav" id="nav" aria-label="Main"><ul>%s</ul></nav>
<div class="header-cta"><a class="btn btn-call" href="%s">%s %s</a><button class="nav-toggle" aria-controls="nav" aria-expanded="false">Menu</button></div>
</div></header>""" % (TEL, C["phone_display"], LOGO_MARK, links, TEL, icon("phone"), C["phone_display"])


def footer():
    svc = "".join('<li><a href="/%s/">%s</a></li>' % (s["slug"], s["name"]) for s in CORE)
    areas = "".join('<li><a href="%s">Car recovery %s</a></li>' % (area_url(a), a["short"]) for a in AREAS[:10])
    email = '<br><a href="mailto:%s">%s</a>' % (C["email"], C["email"]) if C["email"] else ""
    return """<section class="cta-band"><div class="wrap"><h2>Stuck? Recovery is one call away — 24/7.</h2><div style="display:flex;gap:10px;flex-wrap:wrap">%s</div></div></section>
<footer class="site-footer"><div class="wrap">
<div class="footer-grid">
<div><a class="logo" href="/" style="color:#fff">%s<span>Tow Brothers<small style="color:#9fb0c8">Car Recovery Lahore</small></span></a>
<p style="margin-top:14px"><strong style="color:#fff">Tow Brothers</strong><br>%s<br>%s, %s %s, Pakistan<br>
<a href="%s">%s</a>%s<br>Open 24 hours, 7 days a week<br><a href="%s" target="_blank" rel="noopener">View on Google Maps</a></p></div>
<div><h3>Services</h3><ul>%s</ul></div>
<div><h3>Areas in Lahore</h3><ul>%s<li><a href="/areas/">All areas →</a></li></ul></div>
<div><h3>Company</h3><ul><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/blog/">Guides</a></li><li><a href="/services/">All services</a></li></ul></div>
</div>
<div class="footer-bottom"><span>© %d Tow Brothers — Car Recovery &amp; Towing Service in Lahore</span><span>Emergency: Rescue 1122 · Police 15 · Motorway Police 130</span></div>
</div></footer>
<nav class="callbar" aria-label="Quick contact"><a class="c" href="%s">%s Call Now</a><a class="w" href="%s" rel="nofollow noopener" target="_blank">%s WhatsApp</a></nav>""" % (
        cta_buttons("lg"), LOGO_MARK, C["street"], C["city"], C["region"], C["postcode"],
        TEL, C["phone_display"], email, MAPS_URL, svc, areas, date.today().year,
        TEL, icon("phone"), WA, icon("chat"))


SCRIPT = ("<script>(function(){var b=document.querySelector('.nav-toggle'),n=document.getElementById('nav');"
          "if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');"
          "b.setAttribute('aria-expanded',o?'true':'false');b.textContent=o?'Close':'Menu';});})();</script>")


def page(path, title, desc, body, schemas=(), og_type="website", robots="index,follow"):
    url = SITE + path
    ld = "".join('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False, separators=(",", ":"))
                 for s in schemas)
    return """<!doctype html>
<html lang="en-PK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="geo.region" content="PK-PB">
<meta name="geo.placename" content="Lahore">
<meta name="theme-color" content="#0b1f3a">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Tow Brothers">
<meta property="og:locale" content="en_PK">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css?v={ver}">
{ld}
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
{script}
</body>
</html>
""".format(title=escape(title), desc=escape(desc), robots=robots, url=url, og_type=og_type, site=SITE,
           ver=TODAY.replace("-", ""), ld=ld, header=header(path), body=body, footer=footer(), script=SCRIPT)


def crumbs_html(crumbs):
    items = []
    for i, (n, u) in enumerate(crumbs):
        items.append('<li>%s</li>' % (n if i == len(crumbs) - 1 else '<a href="%s">%s</a>' % (u, n)))
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(items)


def page_hero(crumbs, h1, lead, eyebrow="24/7 · All of Lahore"):
    return """<section class="hero page-hero"><div class="wrap"><div>
{crumbs}<span class="eyebrow">{eyebrow}</span>
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="ctas">{cta}</div>
<ul class="ticks"><li>Open 24/7</li><li>Price confirmed before dispatch</li><li>Flatbed &amp; lifter</li><li>All Lahore + motorways</li></ul>
</div></div></section>""".format(crumbs=crumbs_html(crumbs), eyebrow=eyebrow, h1=h1, lead=lead, cta=cta_buttons("lg"))


def faq_html(faqs, heading="Frequently asked questions"):
    items = "".join("<details><summary>%s</summary><p>%s</p></details>" % (escape(q), escape(a)) for q, a in faqs)
    return '<div class="faq"><h2>%s</h2>%s</div>' % (heading, items)


def service_cards(services, n=None):
    out = []
    for s in services[:n] if n else services:
        out.append('<article class="card"><div class="icon">%s</div><h3><a href="/%s/">%s</a></h3><p>%s</p>'
                   '<a class="more" href="/%s/">%s in Lahore →</a></article>'
                   % (icon(s["icon"]), s["slug"], s["name"], s["card"], s["slug"], s["name"]))
    return "".join(out)


def area_pills(areas=AREAS, prefix="Car recovery in "):
    return '<ul class="area-links">%s</ul>' % "".join(
        '<li><a href="%s">%s%s</a></li>' % (area_url(a), prefix, a["name"]) for a in areas)


def sidebar(current_slug=None):
    others = "".join('<li><a href="/%s/">%s</a></li>' % (s["slug"], s["name"])
                     for s in CORE if s["slug"] != current_slug)
    return """<aside class="sidebar">
<div class="card callbox"><h3 style="color:#fff">Need help right now?</h3><p>Call or WhatsApp your location. Open 24/7 across Lahore.</p>{cta}</div>
<div class="card"><h3>Our services</h3><ul>{others}</ul></div>
<div class="card"><h3>Our base</h3><p>{addr}<br>Lahore, Pakistan</p><a href="{maps}" target="_blank" rel="noopener">Get directions →</a></div>
</aside>""".format(cta=cta_buttons(), others=others, addr=C["street"], maps=MAPS_URL)


def map_embed():
    return ('<iframe title="Tow Brothers location on Google Maps" src="%s" width="100%%" height="340" '
            'style="border:0;border-radius:14px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
            % MAPS_EMBED)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
PAGES = []  # (path, priority) for sitemap


def write(path, html, priority="0.7"):
    rel = path.strip("/")
    target = os.path.join(OUT, rel, "index.html") if not rel.endswith(".html") else os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html.replace("{phone}", C["phone_display"]))
    if priority:
        PAGES.append((path, priority))


HOME_FAQS = [
    ("Is Tow Brothers available 24 hours?", "Yes. Our car recovery and towing service in Lahore runs 24 hours a day, 7 days a week, including nights, weekends, Eid and public holidays."),
    ("How do I get car recovery near me in Lahore?", "Call or WhatsApp Tow Brothers and share your live location. We confirm the price and send the nearest recovery van or car lifter straight to you."),
    ("Is car recovery the same as car towing?", "Yes. In Pakistan people say car recovery, recovery van, car lifter or towing for the same service: moving a car that can't or shouldn't be driven."),
    ("Which areas of Lahore do you cover?", "All of Lahore — including DHA, Gulberg, Johar Town, Bahria Town, Model Town, Cantt, Iqbal Town, Township, Wapda Town, Valencia, Lake City, Shahdara, Thokar Niaz Baig, Multan Road, Canal Road and the Ring Road — plus motorways and inter-city routes."),
    ("Do you tow automatic and luxury cars?", "Yes. Automatic, 4x4, luxury and low cars are moved on a flatbed so the gearbox and body stay safe."),
    ("How much do you charge for car recovery in Lahore?", "Charges depend on distance, vehicle type and whether a flatbed is needed. We give you the full price before we dispatch — no hidden charges."),
    ("Do you recover cars from the motorway?", "Yes. We recover cars from the M-2 Lahore–Islamabad Motorway, M-3, M-11, the Lahore Ring Road and highways around Lahore."),
]


def build_home():
    title = "Car Recovery & Towing Service in Lahore 24/7 | Tow Brothers"
    desc = ("24/7 car recovery & car towing service in Lahore. Flatbed recovery van, car lifter, motorway & "
            "accident recovery. Fast car recovery near you — call now.")
    why = [
        ("clock", "Open 24/7", "Day, night, weekends and Eid — our phone is always answered."),
        ("tag", "Clear upfront price", "You know the full price before the recovery van is sent."),
        ("shield", "Careful handling", "Flatbeds and soft straps for automatic, luxury and damaged cars."),
        ("pin", "All of Lahore", "From our Hanjarwal base we cover every part of Lahore, plus motorways."),
    ]
    why_html = "".join('<div class="card"><div class="icon">%s</div><h3>%s</h3><p>%s</p></div>' % (icon(i), h, p)
                       for i, h, p in why)
    body = """
<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">24/7 Car Recovery in Lahore</span>
<h1>Car Recovery &amp; Towing Service in Lahore</h1>
<p class="lead">Broken down, had an accident or need your car moved? <strong>Tow Brothers</strong> is a Lahore towing service with flatbed recovery vans and car lifters on call 24 hours a day. Call now for fast car recovery near you.</p>
<div class="ctas">{cta}</div>
<ul class="ticks"><li>Open 24/7</li><li>Price confirmed before dispatch</li><li>Flatbed &amp; lifter</li><li>All Lahore + motorways</li></ul>
</div>
<div class="hero-art">{art}</div>
</div></section>

<section><div class="wrap">
<div class="stats">
<div><b>24/7</b><span>Recovery &amp; towing</span></div>
<div><b>{n_areas}+</b><span>Lahore areas covered</span></div>
<div><b>M-2 · M-3 · M-11</b><span>Motorway recovery</span></div>
<div><b>Car · SUV · Bike</b><span>All vehicle types</span></div>
</div>
</div></section>

<section class="alt" id="services"><div class="wrap">
<div class="section-head"><h2>Car recovery &amp; towing services in Lahore</h2>
<p>Whatever stopped your car, we have the right recovery vehicle for it — from a quick jump start to a flatbed trip to another city.</p></div>
<div class="grid g3">{cards}</div>
<h3 style="margin-top:32px">More towing &amp; recovery help in Lahore</h3>
{extra}
<h3 style="margin-top:24px">Car transport from Lahore</h3>
{routes}
</div></section>

<section><div class="wrap two-col">
<div class="prose">
<h2>Lahore's 24/7 towing service — when you need it most</h2>
<p>Cars break down at the worst moments: in Canal Road traffic, on a dark stretch of the Ring Road, or in the middle of the night on Multan Road. Tow Brothers was set up to be the call that fixes that. We are a local <strong>car recovery service in Lahore</strong> based in Hanjarwal, running recovery vans, flatbeds and car lifters around the clock.</p>
<p>In Lahore, people use different words for the same job — <strong>car recovery</strong>, <strong>car towing</strong>, <strong>recovery van</strong> or <strong>car lifter</strong>. Whatever you call it, we come to your location, load your car safely and take it to your mechanic, dealer, home or any city in Pakistan.</p>
<p>People find us by many names: <a href="/tow-truck-lahore/">tow truck Lahore</a>, <a href="/car-crane-service-lahore/">car crane service</a>, <a href="/car-lifter-lahore/">car lifter</a>, <a href="/car-recovery-near-me/">car recovery near me</a>, <a href="/car-towing-lahore/">towing service near me</a>, <a href="/24-hour-car-recovery-lahore/">24 hour car recovery</a>, <a href="/breakdown-recovery-lahore/">breakdown recovery</a> and <a href="/vehicle-recovery-lahore/">vehicle recovery Lahore</a>. It's all the same trusted team.</p>
<h3>How it works</h3>
<ol class="steps">
<li><strong>Call or WhatsApp</strong> — share your live location and car model.</li>
<li><strong>Get your price</strong> — confirmed before we dispatch.</li>
<li><strong>We arrive &amp; load</strong> — the right vehicle, handled with care.</li>
<li><strong>Drop-off</strong> — anywhere in Lahore or another city.</li>
</ol>
</div>
<div class="card callbox"><h3 style="color:#fff">Searching "car recovery near me"?</h3><p>We cover every part of Lahore from our base near the Pepsi warehouse in Hanjarwal. Send your live location on WhatsApp for the fastest response.</p>{cta}</div>
</div></section>

<section class="alt" id="areas"><div class="wrap">
<div class="section-head"><h2>Car recovery near you — anywhere in Lahore</h2>
<p>Our recovery vans cover the whole city. Pick your area to see local details.</p></div>
{pills}
</div></section>

<section><div class="wrap">
<div class="section-head"><h2>Why drivers in Lahore choose Tow Brothers</h2></div>
<div class="grid g4">{why}</div>
</div></section>

<section class="alt"><div class="wrap two-col">
<div class="prose">
<h2>Vehicles we recover</h2>
<p>Hatchbacks, sedans, SUVs, 4x4s, vans, pickups, motorcycles and heavy bikes — Suzuki Alto, Cultus, Mehran and Swift, Honda City and Civic, Toyota Corolla, Yaris, Fortuner and Hilux, Kia Sportage and Picanto, Hyundai Tucson, MG, Haval, Changan and imported cars.</p>
<p>Automatic, hybrid, electric, 4x4 and luxury vehicles travel on a <a href="/flatbed-towing-lahore/">flatbed</a>. Manual cars on short trips can go by <a href="/car-lifter-lahore/">car lifter</a>. Not sure which you need? Read <a href="/blog/flatbed-vs-wheel-lift-towing/">flatbed vs wheel-lift towing</a>.</p>
<h2>Motorway &amp; inter-city recovery</h2>
<p>From Hanjarwal we are close to Thokar Niaz Baig and the start of the M-2. We handle <a href="/motorway-recovery/">motorway recovery</a> on M-2, M-3, M-11 and the Ring Road, and <a href="/car-transport-lahore/">car transport</a> from Lahore to Islamabad, Faisalabad, Multan, Sialkot and beyond.</p>
</div>
<div>{faq}</div>
</div></section>

<section><div class="wrap two-col">
<div><h2>Find Tow Brothers</h2>
<p><strong>Tow Brothers</strong><br>{addr}<br>Lahore, Punjab {pc}, Pakistan</p>
<p>Open 24 hours · 7 days a week<br><a href="{tel}">{phone}</a></p>
<p><a class="btn btn-ghost" href="{maps}" target="_blank" rel="noopener">{pin} Open in Google Maps</a></p></div>
<div>{map}</div>
</div></section>
""".format(cta=cta_buttons("lg"), art=TRUCK_ART, n_areas=len(AREAS), cards=service_cards(CORE),
           extra=service_pills(EXTRA), routes=route_pills(),
           pills=area_pills(), why=why_html, faq=faq_html(HOME_FAQS), addr=C["street"], pc=C["postcode"],
           tel=TEL, phone=C["phone_display"], maps=MAPS_URL, pin=icon("pin"), map=map_embed())
    write("/", page("/", title, desc, body, [business_schema(), website_schema(), faq_schema(HOME_FAQS)]), "1.0")


def build_services():
    crumbs = [("Home", "/"), ("Services", "/services/")]
    body = page_hero(crumbs, "Car Recovery &amp; Towing Services in Lahore",
                     "Every service you need when your car can't be driven — available 24/7 across Lahore.") + \
        ('<section><div class="wrap"><div class="grid g3">%s</div></div></section>' % service_cards(CORE)) + \
        ('<section class="alt"><div class="wrap"><div class="section-head"><h2>More towing &amp; recovery services</h2></div>'
         '<div class="grid g3">%s</div></div></section>' % service_cards(EXTRA)) + \
        ('<section><div class="wrap"><div class="section-head"><h2>Car transport from Lahore to other cities</h2></div>%s</div></section>'
         % route_pills())
    write("/services/", page("/services/", "Car Recovery & Towing Services in Lahore | Tow Brothers",
                             "All Tow Brothers services in Lahore: car recovery, car towing, car lifter, flatbed, motorway, accident and bike recovery, roadside assistance and car transport.",
                             body, [breadcrumb_schema(crumbs)]), "0.8")

    for s in SERVICES:
        path = "/%s/" % s["slug"]
        crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
        body = page_hero(crumbs, s["h1"], s["lead"]) + """
<section><div class="wrap two-col">
<div class="prose">{body}</div>
{sidebar}
</div></section>
<section class="alt"><div class="wrap">
<div class="section-head"><h2>{name} across Lahore</h2><p>Available in every area of Lahore, including:</p></div>
{pills}
</div></section>
<section><div class="wrap prose">{faq}</div></section>
<section class="alt"><div class="wrap"><div class="section-head"><h2>{more_h}</h2></div>{more}</div></section>
""".format(body=s["body"], sidebar=sidebar(s["slug"]), name=s["name"], pills=area_pills(prefix=""), faq=faq_html(s["faqs"]),
           more_h="Car transport routes from Lahore" if s["slug"] == "car-transport-lahore" else "Related towing &amp; recovery services",
           more=route_pills() if s["slug"] == "car-transport-lahore" else service_pills([x for x in SERVICES if x["slug"] != s["slug"]]))
        schemas = [service_schema(s["name"], path, s["desc"]), breadcrumb_schema(crumbs), faq_schema(s["faqs"])]
        write(path, page(path, s["title"], s["desc"], body, schemas), "0.9")


def build_routes():
    for r in ROUTES:
        path = route_url(r)
        both = r["city"] + (" & " + r["also"] if r["also"] else "")
        crumbs = [("Home", "/"), ("Services", "/services/"), ("Car Transport", "/car-transport-lahore/"),
                  ("Lahore to " + r["city"], path)]
        title = "Car Transport Lahore to %s | Car Shifting & Recovery" % r["city"]
        desc = ("Door-to-door car transport from Lahore to %s on a recovery vehicle. Running or non-running cars, "
                "price confirmed first. Call {phone}." % both)
        faqs = [
            ("How much does car transport from Lahore to %s cost?" % r["city"],
             "It depends on the car and the exact pickup and drop-off addresses. WhatsApp us both addresses and your car model for an exact quote."),
            ("Do you also bring cars from %s to Lahore?" % r["city"],
             "Yes. We transport cars both ways between Lahore and %s." % both),
            ("Can you transport a non-running car to %s?" % r["city"],
             "Yes. The car is carried on the recovery vehicle, so it does not need to run."),
        ]
        body = page_hero(crumbs, "Car Transport from Lahore to %s" % escape(both), escape(r["note"]),
                         eyebrow="Lahore ⇄ %s" % r["city"]) + """
<section><div class="wrap two-col">
<div class="prose">
<h2>Lahore to {city} car shifting, door to door</h2>
<p>Tow Brothers collects your car from your door in Lahore and delivers it to your address in {both} — or brings it from {city} to Lahore. The car travels on a recovery vehicle, so there is no extra mileage, no wear and no risk of a breakdown on the way.</p>
<h2>Route details</h2>
<ul>
<li><strong>Distance:</strong> {km}</li>
<li><strong>Route:</strong> {road}</li>
<li><strong>Timing:</strong> {timing}</li>
<li><strong>Vehicles:</strong> cars, SUVs, 4x4s, vans and bikes — running or non-running</li>
</ul>
<h2>How it works</h2>
<ol class="steps">
<li><strong>Send details</strong> — pickup address in Lahore, drop-off address in {city}, car model.</li>
<li><strong>Get your price</strong> — confirmed before we book the trip.</li>
<li><strong>Pickup</strong> — we load and strap the car at your door.</li>
<li><strong>Delivery</strong> — the car is unloaded and handed over at the destination.</li>
</ol>
<h2>Before pickup</h2>
<ul>
<li>Keep a copy of the registration book and your CNIC ready</li>
<li>Remove valuables and loose items from the car</li>
<li>Note any existing scratches or dents together with our driver</li>
</ul>
<h2>Broken down on the way to {city}?</h2>
<p>If your car stopped on the road between Lahore and {city}, see our <a href="/motorway-recovery/">motorway recovery</a> service — we can recover it and deliver it to either city.</p>
</div>
{sidebar}
</div></section>
<section class="alt"><div class="wrap two-col">
<div class="prose">{faq}</div>
<div><h2>Other routes from Lahore</h2>{routes}</div>
</div></section>
""".format(city=r["city"], both=escape(both), km=r["km"], road=r["road"], timing=r["timing"],
           sidebar=sidebar(), faq=faq_html(faqs), routes=route_pills())
        schemas = [service_schema("Car transport from Lahore to " + both, path, desc, "Lahore to " + both),
                   breadcrumb_schema(crumbs), faq_schema(faqs)]
        write(path, page(path, title, desc, body, schemas), "0.7")


def build_areas():
    crumbs = [("Home", "/"), ("Areas", "/areas/")]
    cards = "".join('<article class="card"><div class="icon">%s</div><h3><a href="%s">%s</a></h3><p>%s</p></article>'
                    % (icon("pin"), area_url(a), area_full(a), escape(a["intro"].split(". ")[0]) + ".") for a in AREAS)
    body = page_hero(crumbs, "Car Recovery Near You — Areas We Cover in Lahore",
                     "Tow Brothers covers the whole of Lahore from our base in Hanjarwal. Choose your area for local details.") + \
        '<section><div class="wrap"><div class="grid g3">%s</div></div></section>' % cards
    write("/areas/", page("/areas/", "Car Recovery Near Me in Lahore — Areas We Cover | Tow Brothers",
                          "Car recovery and towing near you in every part of Lahore: DHA, Gulberg, Johar Town, Bahria Town, Model Town, Cantt, Multan Road, Thokar and more. 24/7.",
                          body, [breadcrumb_schema(crumbs)]), "0.8")

    core = ["car-recovery-lahore", "car-towing-lahore", "car-lifter-lahore", "flatbed-towing-lahore",
            "accident-car-recovery-lahore", "roadside-assistance-lahore"]
    core_services = [s for s in SERVICES if s["slug"] in core]
    for a in AREAS:
        path = area_url(a)
        full = area_full(a)
        crumbs = [("Home", "/"), ("Areas", "/areas/"), (a["name"], path)]
        title = "Car Recovery in %s Lahore | 24/7 Towing — Tow Brothers" % a["short"]
        desc = ("24/7 car recovery & towing in %s, Lahore. Recovery van, car lifter and flatbed for breakdowns "
                "and accidents. Call Tow Brothers." % a["short"])
        faqs = list(a["faqs"]) + [
            ("Is car recovery available 24/7 in %s?" % a["name"],
             "Yes. Tow Brothers provides car recovery and towing in %s 24 hours a day, 7 days a week." % full),
            ("How do I book car towing in %s?" % a["name"],
             "Call or WhatsApp us your live location in %s and where you want the car dropped. We confirm the price and send the nearest recovery vehicle." % a["name"]),
        ]
        nearby = [AREA_BY_SLUG[n] for n in a["nearby"] if n in AREA_BY_SLUG]
        spots = "".join("<li>%s</li>" % escape(x) for x in a["spots"])
        base_note = ("<p><strong>This is our home area</strong> — our recovery vans are based right here near the Pepsi warehouse in Hanjarwal.</p>"
                     if a.get("base") else
                     "<p>Our recovery vans are based in Hanjarwal, Lahore, and are dispatched across the city 24/7, so help can head to %s as soon as you call.</p>" % a["name"])
        body = page_hero(crumbs, "Car Recovery &amp; Towing in %s" % escape(full), escape(a["intro"]),
                         eyebrow="24/7 · %s" % escape(a["name"])) + """
<section><div class="wrap two-col">
<div class="prose">
<h2>Car recovery near you in {name}</h2>
<p>{local}</p>
{base_note}
<h3>Places we often cover in {name}</h3>
<ul>{spots}</ul>
<h2>Our services in {name}</h2>
<ul>
<li><a href="/car-recovery-lahore/">Car recovery</a> for breakdowns, dead batteries and engine failure</li>
<li><a href="/car-towing-lahore/">Car towing</a> to any workshop, dealer or home</li>
<li><a href="/car-lifter-lahore/">Car lifter</a> for quick shifting of non-running cars</li>
<li><a href="/flatbed-towing-lahore/">Flatbed recovery</a> for automatic, luxury and 4x4 cars</li>
<li><a href="/accident-car-recovery-lahore/">Accident car recovery</a> with careful handling</li>
<li><a href="/bike-recovery-lahore/">Bike recovery</a> for motorcycles and heavy bikes</li>
<li><a href="/roadside-assistance-lahore/">Roadside assistance</a> — jump start, tyre change, fuel</li>
</ul>
<h2>How to get help fast in {name}</h2>
<ol class="steps">
<li><strong>Stay safe</strong> — hazards on, passengers away from traffic.</li>
<li><strong>Call or WhatsApp</strong> — share your live location and nearest landmark in {name}.</li>
<li><strong>Confirm the price</strong> and drop-off point.</li>
<li><strong>We recover your car</strong> and deliver it where you need it.</li>
</ol>
</div>
{sidebar}
</div></section>
<section class="alt"><div class="wrap">
<div class="section-head"><h2>Popular services in {name}</h2></div>
<div class="grid g3">{cards}</div>
</div></section>
<section><div class="wrap two-col">
<div class="prose">{faq}</div>
<div><h2>Nearby areas</h2>{nearby}<p style="margin-top:18px"><a href="/areas/">See all areas we cover →</a></p></div>
</div></section>
""".format(name=escape(a["name"]), local=escape(a["local"]), base_note=base_note, spots=spots,
           sidebar=sidebar(), cards=service_cards(core_services), faq=faq_html(faqs),
           nearby=area_pills(nearby))
        schemas = [service_schema("Car recovery and towing in " + full, path, desc, full),
                   breadcrumb_schema(crumbs), faq_schema(faqs)]
        write(path, page(path, title, desc, body, schemas), "0.8")


def build_blog():
    crumbs = [("Home", "/"), ("Guides", "/blog/")]
    cards = "".join('<article class="card"><h3><a href="/blog/%s/">%s</a></h3><p>%s</p><a class="more" href="/blog/%s/">Read guide →</a></article>'
                    % (g["slug"], g["h1"], g["desc"], g["slug"]) for g in GUIDES)
    body = page_hero(crumbs, "Car Recovery &amp; Breakdown Guides for Lahore Drivers",
                     "Practical advice on breakdowns, towing and recovery in Lahore.", eyebrow="Guides") + \
        '<section><div class="wrap"><div class="grid g3">%s</div></div></section>' % cards
    write("/blog/", page("/blog/", "Car Recovery & Breakdown Guides for Lahore | Tow Brothers",
                         "Guides for Lahore drivers: what to do in a breakdown, car recovery charges, and flatbed vs lifter towing.",
                         body, [breadcrumb_schema(crumbs)]), "0.6")
    for g in GUIDES:
        path = "/blog/%s/" % g["slug"]
        crumbs = [("Home", "/"), ("Guides", "/blog/"), (g["h1"], path)]
        body = page_hero(crumbs, g["h1"], g["desc"], eyebrow="Guide") + """
<section><div class="wrap two-col"><article class="prose">{b}</article>{sb}</div></section>""".format(b=g["body"], sb=sidebar())
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"],
               "datePublished": g["date"], "dateModified": TODAY, "inLanguage": "en-PK",
               "mainEntityOfPage": SITE + path, "image": SITE + "/assets/og-image.png",
               "author": {"@type": "Organization", "name": C["name"], "url": SITE + "/"},
               "publisher": {"@id": BIZ_ID}}
        write(path, page(path, g["title"], g["desc"], body, [art, breadcrumb_schema(crumbs)], og_type="article"), "0.6")


def build_about_contact():
    crumbs = [("Home", "/"), ("About", "/about/")]
    body = page_hero(crumbs, "About Tow Brothers — Car Recovery in Lahore",
                     "A local Lahore towing and recovery team, on call 24/7.", eyebrow="About us") + """
<section><div class="wrap two-col"><div class="prose">
<h2>Who we are</h2>
<p>Tow Brothers is a car recovery and towing company based near the Pepsi warehouse in Hanjarwal, Lahore. We started with a simple idea: when someone's car stops, they should be able to make one call and know help is coming — at a fair price they know in advance.</p>
<p>Today we run recovery vans, flatbeds and car lifters across Lahore, handling breakdowns, accidents, workshop shifting, motorway recoveries and inter-city car transport.</p>
<h2>What we promise</h2>
<ul>
<li><strong>We answer, 24/7.</strong> Day or night, someone picks up.</li>
<li><strong>Clear pricing.</strong> The price is confirmed before we dispatch.</li>
<li><strong>Your car, handled with care.</strong> The right vehicle for your car, proper straps, no dragging.</li>
<li><strong>Local knowledge.</strong> We know Lahore's roads, underpasses, societies and workshops.</li>
</ul>
<h2>Where we work</h2>
<p>Every part of Lahore — see <a href="/areas/">all areas</a> — plus motorways and routes to other cities.</p>
</div>{sb}</div></section>""".format(sb=sidebar())
    write("/about/", page("/about/", "About Tow Brothers | Car Recovery & Towing Company in Lahore",
                          "Tow Brothers is a Lahore car recovery and towing company based in Hanjarwal, running recovery vans, flatbeds and car lifters 24/7.",
                          body, [breadcrumb_schema(crumbs)]), "0.5")

    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    email = '<p><strong>Email:</strong> <a href="mailto:%s">%s</a></p>' % (C["email"], C["email"]) if C["email"] else ""
    body = page_hero(crumbs, "Contact Tow Brothers — 24/7 Car Recovery Lahore",
                     "Call or WhatsApp for immediate help. Share your live location for the fastest response.", eyebrow="Contact") + """
<section><div class="wrap two-col">
<div class="prose">
<h2>Get help now</h2>
<p><strong>Phone:</strong> <a href="{tel}">{phone}</a></p>
<p><strong>WhatsApp:</strong> <a href="{wa}" rel="nofollow noopener" target="_blank">Message us on WhatsApp</a></p>
{email}
<p><strong>Address:</strong> Tow Brothers, {addr}, Lahore, Punjab {pc}, Pakistan</p>
<p><strong>Hours:</strong> Open 24 hours, 7 days a week</p>
<h3>When you call, tell us</h3>
<ul><li>Your exact location (or share a live pin on WhatsApp)</li><li>Car make, model and whether it's automatic</li><li>What happened — breakdown, accident, flat tyre, etc.</li><li>Where you want the car dropped</li></ul>
<p><a class="btn btn-ghost" href="{maps}" target="_blank" rel="noopener">{pin} Get directions on Google Maps</a></p>
</div>
<div>{map}</div>
</div></section>""".format(tel=TEL, phone=C["phone_display"], wa=WA, email=email, addr=C["street"], pc=C["postcode"],
                           maps=MAPS_URL, pin=icon("pin"), map=map_embed())
    write("/contact/", page("/contact/", "Contact Tow Brothers | 24/7 Car Recovery in Lahore",
                            "Call or WhatsApp Tow Brothers for 24/7 car recovery and towing in Lahore. Based near Pepsi Warehouse, Hanjarwal, Lahore 54500.",
                            body, [business_schema(), breadcrumb_schema(crumbs)]), "0.7")

    body = page_hero([("Home", "/"), ("Page not found", "/404.html")], "Page not found",
                     "This page doesn't exist — but if your car is stuck, we can still help right now.", eyebrow="404") + \
        '<section><div class="wrap"><div class="grid g3">%s</div></div></section>' % service_cards(SERVICES, 6)
    write("/404.html", page("/404.html", "Page not found | Tow Brothers", "Page not found.", body,
                            robots="noindex,follow"), priority=None)


# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
def build_static():
    assets = os.path.join(OUT, "assets")
    os.makedirs(assets, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "src", "style.css"), os.path.join(assets, "style.css"))
    with open(os.path.join(OUT, "favicon.svg"), "w") as f:
        f.write(LOGO_MARK.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
    # GitHub Pages custom domain
    with open(os.path.join(OUT, "CNAME"), "w") as f:
        f.write(SITE.split("://", 1)[1] + "\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    urls = "".join("<url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (SITE, p, TODAY, pr)
                   for p, pr in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % urls)
    build_images(assets)


def _font(size, bold=True):
    from PIL import ImageFont
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial Bold.ttf", "DejaVuSans-Bold.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _mark(d, x, y, s):
    """Draw the logo mark at (x, y) with size s using PIL."""
    k = s / 40.0
    P = lambda pts: [(x + a * k, y + b * k) for a, b in pts]  # noqa: E731
    d.rounded_rectangle([x, y, x + s, y + s], radius=9 * k, fill="#ffc21a")
    d.polygon(P([(6, 25), (23, 25), (23, 15), (28, 15), (33, 20), (33, 25), (34, 25), (34, 28), (6, 28)]), fill="#0b1f3a")
    d.polygon(P([(8, 22), (12, 16), (19, 16), (21, 22)]), fill="#ffffff")
    for cx in (12, 29):
        d.ellipse([x + (cx - 3.6) * k, y + 25.4 * k, x + (cx + 3.6) * k, y + 32.6 * k], fill="#0b1f3a", outline="#ffc21a", width=max(1, int(1.5 * k)))
    d.rectangle([x + 25 * k, y + 17 * k, x + 29 * k, y + 20 * k], fill="#9fd3ff")


def build_images(assets):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("! Pillow not installed — skipping PNG images (pip3 install pillow)")
        return
    # Logo PNGs + favicon.ico
    for size, name in [(512, "logo-512.png"), (180, "apple-touch-icon.png")]:
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        _mark(ImageDraw.Draw(im), 0, 0, size)
        im.save(os.path.join(assets, name))
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    _mark(ImageDraw.Draw(im), 0, 0, 64)
    im.save(os.path.join(OUT, "favicon.ico"), sizes=[(32, 32), (16, 16)])
    # Open Graph share image
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#0b1f3a")
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 90, W, H], fill="#ffc21a")
    _mark(d, 70, 70, 110)
    d.text((205, 82), "TOW BROTHERS", font=_font(64), fill="#ffffff")
    d.text((207, 152), "Car Recovery Lahore", font=_font(30, False), fill="#9fb0c8")
    d.text((70, 250), "Car Recovery & Towing", font=_font(74), fill="#ffffff")
    d.text((70, 340), "Service in Lahore — 24/7", font=_font(74), fill="#ffc21a")
    d.text((70, 448), "Flatbed · Car Lifter · Motorway · Accident Recovery", font=_font(34, False), fill="#d9e2f0")
    d.text((70, H - 68), "Call %s  ·  Hanjarwal, Lahore" % C["phone_display"], font=_font(40), fill="#111111")
    im.save(os.path.join(assets, "og-image.png"), optimize=True)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    build_home()
    build_services()
    build_routes()
    build_areas()
    build_blog()
    build_about_contact()
    build_static()
    print("Built %d pages into %s" % (len(PAGES) + 1, OUT))
    if "0000000" in C["phone_e164"]:
        print("! WARNING: phone number is still the placeholder — set it in CONFIG in build.py")


if __name__ == "__main__":
    main()

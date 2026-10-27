# Tow Brothers — Website

Static, SEO-optimised website for Tow Brothers (car recovery & towing, Lahore).

## Update karna
1. `build.py` ke upar `CONFIG` mein phone, WhatsApp number aur domain likhein.
2. Text badalna ho to `src/content.py` edit karein (services, areas, guides).
3. Terminal mein chalayein:

```bash
python3 build.py
```

4. `site/` folder ke andar ki saari files apni hosting par upload karein (public_html / root).

## Live karne ke baad (SEO checklist)
- Google Search Console mein domain add karein aur `sitemap.xml` submit karein.
- Google Business Profile mein website link daalein; naam, address aur phone bilkul website jaisa rakhein.
- Customers se Google reviews mangwayein (sab se bara local ranking factor).
- Apne trucks/team ki asli photos add karein.
- Facebook / Instagram page bana kar `CONFIG["social"]` mein link daalein.

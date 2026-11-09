# Emilia — a Bavarian hospital by measurement

**Author:** Abhishek Kr Gupta
**Event:** SpookyCTF 2026
**Status:** Derived (unconfirmed) — no platform result was reported before close

## Flag (derived, not confirmed)

```
spooky{bezirkskrankenhaus_passau}
```

Alternative capitalisation (per the series convention the lowercase-underscore form is the primary candidate):

```
spooky{Bezirkskrankenhaus_Passau}
```

## Challenge

A geolocation puzzle. The target is a hospital in a Bavarian mountain town, with constraints:

- under 15 km from the subject's home
- under 6 km from a university
- the building's perimeter between 245 and 335 m
- a Catholic church 400 m to 1 km away

Find the hospital.

## Derivation

A systematic search over mountain university towns (Kempten, Rosenheim, Deggendorf, Passau, Landshut, Bayreuth, Hof) using Nominatim / OpenStreetMap leaves a unique fit:

**Bezirkskrankenhaus Passau**, Wörthstraße 5, 94032 Passau (48.5666202, 13.4468771; OSM way 248978536).

Independently verified:

- Main building footprint perimeter: **249.83 m** (haversine, confirmed by three methods) — inside the 245–335 m band.
- Universität Passau: **399 m** away — inside 6 km.
- Catholic church Sankt Anton (Neuburger Straße 70): **409 m** away — inside the 400 m–1 km band. (Also Christi Himmelfahrt at 858 m and St. Nikola at 895 m.)

Near-miss that rules itself out: Schön Klinik Rosenheim, whose perimeter is 243.0 m — just below the 245 m lower bound.

## Flag (derived, not confirmed)

```
spooky{bezirkskrankenhaus_passau}
```

This is a complete geolocation derivation, but it was **not** confirmed by a platform submission before the window closed.

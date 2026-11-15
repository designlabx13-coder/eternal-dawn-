# Eternal Dawn: Lunar Landing Site Navigator

▶ **Demo video:** https://youtu.be/jFDBcngQbZk  
🚀 **Live app:** https://designlabx13-coder.github.io/eternal-dawn-/
**Team Polaris Path · NASA Space Apps Challenge 2026 · Challenge: Lunar Landing Site Navigator**

Eternal Dawn helps mission planners, educators and the public compare lunar landing sites and dates in seconds. It shows where the Sun and Earth sit over each site's horizon, and what that means for solar power and direct-to-Earth communication.

**Live app:** `https://<your-username>.github.io/eternal-dawn/` (open `index.html`; it works offline, with no install and no login)

## What it does
- **Site selection:** 15 curated sites (Apollo 11/17, Chandrayaan-3, Chang'e 4/6, SLIM, Blue Ghost M1, IM-1, IM-2, Shackleton ridge and floor, Malapert, Haworth, Chang'e 7 target) plus any custom latitude and longitude.
- **Date flexibility:** pick a landing date in 2027–2028, slip the launch by up to 60 days, set the mission length, and see a 60-day "best landing window" bar chart.
- **Sun and Earth visualisation:** a 360° horizon panorama with the Sun and Earth tracks, time to sunset and Earthset, and a scrubbable, playable timeline.
- **Power and comms assessment:** Sun elevation, % sunlit, % Earth visible, longest night, longest comms blackout, and a GO / MARGINAL / NO-GO score.
- **Compare:** pin scenarios, or compare every site on one date, with bar charts side by side.
- **Multiple views:** a 3D Moon lit by the real Sun direction, a 3D and 2D rover atlas with every lunar rover's driving range, and a drivable 3D rover (PP-1 Polaris Prospector concept) with a stone-picker arm and drill, landing at any site.

## Data and method
- **Sun and Earth positions:** JPL DE421 planetary ephemeris (via `jplephem`), including the Moon's physical librations. Vectors are precomputed every 2 hours for 2027–2028 in the Moon's principal-axis frame (`tools/gen_data.py`) and turned into local altitude and azimuth for any coordinate in the browser.
- **Horizons:** **modelled** terrain masks shaped to each site type (rim, massif, crater floor). Next step: replace them with LOLA-derived horizon masks from LROC Quickmap and Moon Trek.
- **Site and rover data:** public mission reports (NASA/LROC, CNSA, ISRO, JAXA, Firefly, Intuitive Machines). Some coordinates are approximate, as marked in the app.
- **Banner render:** Blender (`tools/scene.py`) with real DE421 Sun and Earth geometry over modelled terrain.

## Limitations (stated honestly)
- Horizon masks and drive-mode terrain are modelled, not LOLA data.
- The PP-1 rover, its power figures and its science rates are design estimates, not flight hardware.
- The rover atlas map is schematic; the range circles show distance driven, not the actual routes.

## Run it
Open `index.html` in any modern browser. To host it, upload it to GitHub Pages or drag it onto app.netlify.com/drop.

## Tech
A single self-contained HTML file using Three.js r128, canvas, and vanilla JavaScript.

## License
Our own code, text, renders and models are released under the MIT License (see LICENSE). Third-party software, fonts, data and design references keep their own terms; see THIRD_PARTY_NOTICES.md.

## Disclaimer
This is a NASA Space Apps Challenge entry. It is not affiliated with or endorsed by NASA or any agency or company named here. No NASA logos or insignia are used.

# Space Apps 2026 project page: copy each block into the matching field

Team: **Polaris Path** · Challenge: **Lunar Landing Site Navigator**

---

## Project Name
Eternal Dawn: Lunar Landing Site Navigator

## High-Level Project Summary
Eternal Dawn is a free browser tool that lets mission planners, educators and the public compare lunar landing sites and dates in seconds. Pick a site (Apollo 11, Chandrayaan-3, Chang'e, SLIM, CLPS landers or the south pole) or type any coordinates, choose a date, and see where the Sun and Earth sit over that site's horizon, how long until sunset and Earthset, and how much of the mission has solar power and a direct radio link to Earth, ending in a clear GO / NO-GO score. A launch-slip slider shows instantly how a schedule change affects feasibility, and every site can be compared side by side. This matters because at the lunar south pole the Sun barely clears the horizon, so a few days or a few kilometres can decide whether a mission survives. To make the problem tangible for students, the app also includes a 3D Moon, an atlas of every lunar rover, and a playable rover game (PP-1 Polaris Prospector) that lands at any analysed site under its real Sun angle.

## Link to Project Demo
[YouTube link to polaris_path_demo_30s.mp4 — 28 s, public or unlisted]

## Link to Final Project
App: [https://<username>.github.io/eternal-dawn/ or Netlify link]
Code: [https://github.com/<username>/eternal-dawn]
Extended 3-minute walkthrough: [YouTube link to polaris_path_walkthrough_3min.mp4]

## Detailed Project Description
**What it does**
- Site selection: 15 curated landing sites plus any custom latitude and longitude.
- Date flexibility: any landing date in 2027–2028, a 0–60 day launch-slip slider, a mission-length slider, and a 60-day "best landing window" chart.
- Sun and Earth visualisation: a 360° horizon panorama with the Sun and Earth tracks; Locate Sun, Next sunrise and Highest Sun tools; drag along the Sun path or the timeline to move through time.
- Power and communication assessment: Sun elevation, % sunlit, % Earth visible, power + comms together, time to sunset and Earthset, longest night, longest comms blackout, Earth–Moon distance, radio delay, and a GO / MARGINAL / NO-GO score.
- Comparison: pin scenarios or compare every site on one date with side-by-side bar charts.
- 3D views: a Moon lit by the real Sun direction; a 3D/2D atlas of every lunar rover with its driving range.
- Education: "Why is the south pole so hard?" explainer and Lunar Stone Run, a game where the PP-1 concept rover lands at a chosen site, drives under that site's real Sun angle, collects stones with a microspine gripper into a front cage, and reports each stone's shape factor. Works on desktop and phones.

**How it works**
We precomputed Sun and Earth position vectors every 2 hours for 2027–2028 from the JPL DE421 ephemeris (including the Moon's physical librations) in the Moon's principal-axis frame. In the browser, these are converted to local altitude and azimuth for any coordinate and compared with each site's horizon mask to score power and communications. Everything runs in one self-contained HTML file with no server or login.

**Benefits**
Planners can re-evaluate sites and dates in seconds when a launch slips; students and the public can see why polar landings are hard.

**What we hope to achieve**
Replace the modelled horizon masks with LOLA-derived masks from LROC Quickmap / Moon Trek, add real CLPS and Artemis III candidate regions, and export results for mission teams.

**Tools**
JavaScript, HTML/CSS, three.js (3D), Python (jplephem, NumPy) for data processing, Blender for the banner render.

**Limitations (stated honestly)**
Horizon masks and game terrain are modelled, not yet LOLA data. Some site coordinates are approximate. PP-1 is a fictional concept; its figures are design estimates.

## Use of Super Intelligence (SI)
Yes. We used Claude (Anthropic), a large language model, as a coding and writing assistant. Where it was used:
- **Code:** most of the HTML/JavaScript app, the Python ephemeris-processing scripts and the Blender scene script were drafted with Claude and then directed, reviewed and tested by the team.
- **Text:** the project descriptions, README and on-page explanations were drafted with Claude and edited by the team.
- **Images and videos:** the banner, screenshots and demo videos are renders and screen recordings of our own app (no AI image generator was used). Because the app itself was built with AI help, every image and video carries a visible "AI-assisted (Claude)" watermark.
- **No NASA branding:** no NASA logos, insignia, flags or mission identifiers were generated or used.
The project idea, challenge choice, design direction (rover, wheels, gripper, cage, game), and all testing decisions came from the team.

## NASA Data
- **JPL DE421 planetary and lunar ephemeris** (NASA/JPL): Sun, Earth and Moon positions and lunar librations, the core of every Sun/Earth calculation (same ephemeris family as the JPL Horizons System).
- **LRO / LROC landing-site coordinates** (NASA/GSFC/ASU), e.g. Chang'e 4 and Chang'e 6.
- Reference resources from the challenge: NASA Moon Trek, LROC Quickmap, JPL Horizons.
- Design inspiration (no data or images copied): NASA Glenn superelastic tire, NASA JPL microspine gripper, NASA VIPER rover.

## Space Agency Partner Data and Other References
- ISRO: Chandrayaan-3 / Pragyan landing site (Shiv Shakti point).
- JAXA: SLIM landing site (Shioli crater).
- CNSA: Chang'e 4, Chang'e 6 and Chang'e 7 sites (public mission reports).
- Commercial CLPS missions: Firefly Blue Ghost M1, Intuitive Machines IM-1 and IM-2 (public mission reports).
- HTR SA metal-tile wheel (US patent 11,623,472 B2): design inspiration only.
- Open-source tools: three.js (MIT), jplephem (MIT), de421 (MIT), NumPy (BSD), Blender (GPL; used only as a tool). Fonts: Orbitron, Rajdhani, Barlow (SIL OFL); DejaVu Sans.
- Rover distances and dates: public mission reports and Wikipedia summaries (facts only).
- Full list: THIRD_PARTY_NOTICES.md in the repository.

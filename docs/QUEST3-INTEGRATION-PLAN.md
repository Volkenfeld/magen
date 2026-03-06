# Meta Quest 3 Integration Plan -- Volkenfeld System

> Created: 2026-03-06 (Session 88)
> Status: Research complete, planning phase

---

## Executive Summary

Meta Quest 3 integration across 4 Volkenfeld brands. Two distinct development paths:

1. **Magen-Live VR** (WebXR, web-based) -- immersive 3D data visualization
2. **BodyCraft AI** (Unity native, Quest app) -- AR tattoo preview on real skin

These are separate products with different tech stacks but shared infrastructure (AI generation, data APIs, cloud backend).

---

## Critical Finding: Magen-Live Architecture

**Magen-Live does NOT use Three.js.** The 3D globe is built on:

- **Deck.gl** v9.2.6 (WebGL2 visualization framework, 60+ data layers)
- **MapLibre GL** v5.16.0 (map rendering with globe projection)
- **satellite.js** (SGP4 orbit propagation)
- **Supercluster** (point clustering)
- **D3** (SVG fallback for mobile)

The main renderer is `DeckGLMap.ts` (4,913 lines). MapLibre handles the basemap/globe. Deck.gl handles all data overlays (flights, satellites, alerts, earthquakes, military tracking, etc.).

**Implication:** WebXR integration is NOT as simple as adding `VRButton` to a Three.js scene. MapLibre and Deck.gl have no native WebXR support. Two options exist (see Section 1).

---

## 1. Magen-Live VR (WebXR Path)

### Option A: Hybrid Rendering (Recommended)

Render the MapLibre/Deck.gl output to a texture, then display it inside a Three.js WebXR scene.

**How it works:**
1. MapLibre/Deck.gl renders to an offscreen canvas (existing code, minimal changes)
2. Three.js WebXR scene uses that canvas as a texture on a curved surface or sphere
3. User interacts via hand tracking/controllers in the Three.js VR environment
4. Data overlays (flights, satellites) are rendered as Three.js objects in 3D space around the user

**Pros:** Reuses existing rendering code, fast path to POC
**Cons:** Map interactions need bridging, dual rendering pipeline

### Option B: Three.js Globe Rebuild (Higher quality, more work)

Build a dedicated VR globe experience in Three.js, consuming the same data APIs as Magen-Live.

**How it works:**
1. New Three.js scene with a textured sphere (globe)
2. Same satellite.js propagation, same API endpoints
3. Flights, satellites, alerts rendered as Three.js objects in 3D
4. Full VR-native interaction (reach out and grab the globe, pinch to zoom)

**Pros:** True VR-native experience, best visual quality
**Cons:** Significant rebuild effort, two codebases to maintain

### Recommended: Start with Option A for POC

**Estimated effort:** 2-3 weeks for POC
**Tech:** Three.js + WebXR + existing Magen APIs
**Deployment:** Same Vercel deploy, "Enter VR" button on Magen-Live page

### Quest 3 WebXR Features Available

| Feature | Status | Useful for Magen VR |
|---------|--------|-------------------|
| immersive-vr | Supported | Core VR mode |
| hand-tracking | Supported | Gesture interaction |
| hit-test | Supported | Not needed (no real surfaces) |
| depth-sensing | Supported | Not needed for VR mode |
| layers | Supported | Performance optimization |

### Performance Budget (Quest 3 Browser)

- Target: 90 FPS (11.1ms per frame)
- Draw calls: under 100
- Triangles: 50-100K visible
- Texture memory: 256-512MB
- Use foveated rendering: `renderer.xr.setFoveation(1.0)`

---

## 2. BodyCraft AI (Native Unity Path)

### Why Native, Not WebXR

WebXR CANNOT do what BodyCraft AI needs:
- No raw camera access (Passthrough Camera API is native-only until v77)
- No custom ML model execution (MediaPipe for body detection)
- No Depth API access from WebXR
- No body tracking data from WebXR

**Required stack:** Unity 6 LTS + Meta XR SDK

### Product Vision

Client wears Quest 3 in the studio. Sees tattoo designs on their own body in mixed reality. Artist adjusts placement, size, rotation. Client sees life-size, stereoscopic preview before committing.

### Development Phases

**Phase 1: MVP (3-4 months)**
- Manual placement: artist/client positions a flat tattoo design in 3D space near body
- Hand controllers for position, rotation, scale
- Spatial anchors to persist placement between sessions
- Passthrough AR with transparent rendering
- Design library: load PNG/SVG tattoo designs
- Simple UI: browse designs, select, place

**Phase 2: Smart Placement (3-4 months after MVP)**
- MediaPipe Pose detection on passthrough camera frames
- Geometric proxy: approximate arm as cylinder, leg as cylinder, torso as plane
- Auto-conform tattoo to proxy geometry
- Depth API for surface alignment
- Design sizing suggestions based on body part detection

**Phase 3: AI Integration (2-3 months after Phase 2)**
- AI tattoo generation (Stable Diffusion with tattoo LoRA, cloud API)
- Text-to-tattoo: client describes what they want, AI generates options
- Style transfer: take a sketch, output polished design in chosen style
- Companion web app for design generation (syncs to Quest)
- Client portfolio: save designs across sessions

### Meta APIs Used

| API | Phase | Purpose |
|-----|-------|---------|
| Passthrough | 1 | See real world through cameras |
| Hand Tracking | 1 | Interaction/UI |
| Spatial Anchors | 1 | Persist tattoo position |
| Passthrough Camera API | 2 | Raw frames for body detection |
| Depth API | 2 | Surface distance/alignment |
| IOBT (Body Tracking) | 2 | Upper body landmark positions |

### Market Numbers

- Virtual Tattoo Preview market: $315M (2024) to $1.52B (2033), 19.2% CAGR
- NO ONE has built Quest 3 tattoo AR yet
- First customer: HIGHLIGHT Tattoo Studio (own studio = real testbed)

### Business Models

| Model | Price | Target |
|-------|-------|--------|
| Per-studio SaaS | $99-299/mo | Individual studios |
| Per-consultation | $5-15/session | Client pass-through |
| Hardware + software bundle | $999-1,999 | Studios without Quest 3 |
| AI design generation | $2-5/design | Direct-to-consumer add-on |

---

## 3. Brand Integration Map

### BodyCraft AI (Primary product)
- Quest 3 tattoo visualization app
- AI design generation
- Studio tool + client-facing experience

### Magen-Live (Showcase/wow factor)
- VR globe visualization
- WebXR on existing web platform
- Demonstrates platform capabilities in immersive format

### HIGHLIGHT Studio (First customer, testbed)
- BodyCraft AI MVP testing with real clients
- 360 studio tour (simple, good marketing content)
- Portfolio showcase in VR gallery

### Winging AI (Content play)
- "AI meets Spatial Computing" content vertical
- Reviews, tutorials, case studies about Quest 3 + AI
- Newsletter content about XR trends

---

## 4. Infrastructure Support

### What We Have

| Capability | System | Quest 3 Connection |
|------------|--------|-------------------|
| Image generation | NanoBanana MCP (Gemini) | Generate tattoo designs |
| Real-time data | Magen WebSocket relay | Feed VR globe with live data |
| Content pipeline | 6 sources, daily drafts | XR content for Winging AI |
| Web deployment | Vercel | WebXR apps (Magen VR) |
| AI agents (5) | Ivan, Arthur, Beski, Dafi, Luchi | Backend processing |
| Dashboard | Holt | Monitor VR usage/metrics |

### What We Need

| Need | For What | Effort |
|------|----------|--------|
| Unity 6 LTS + Meta XR SDK | BodyCraft AI native development | Luchi/Volken's PC |
| Quest 3 hardware | Testing | $500, purchase needed |
| Stable Diffusion API | Tattoo AI generation | Cloud host or API service |
| Three.js WebXR knowledge | Magen VR | Beski can research + build |

---

## 5. Priority Order

1. **Magen-Live VR POC** (WebXR) -- fastest path to "wow," builds on existing code, Beski can build autonomously on Ivan. Estimated 2-3 weeks.

2. **BodyCraft AI MVP design** -- architecture, wireframes, user flow. Can start without Quest 3. Beski + Volken collaborative.

3. **BodyCraft AI development** -- requires Unity on a machine with GPU. Volken's PC (Luchi) or contracted developer.

4. **HIGHLIGHT VR tour** -- low effort, high marketing value. Can be done with existing 360 camera + hosting.

5. **Winging AI XR content** -- ongoing, start writing about XR+AI as soon as Magen VR POC exists.

---

## 6. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Deck.gl/MapLibre WebXR incompatibility | HIGH | Option A (texture bridge) or Option B (Three.js rebuild) |
| BodyCraft AI body mesh quality | HIGH | Start with manual placement, iterate |
| Unity development skill gap | MEDIUM | Volken learns or hire contractor |
| Quest 3 install base too small for D2C | HIGH | Start B2B (studios), not D2C |
| Performance in Quest browser | MEDIUM | Aggressive optimization, reduce layers in VR mode |
| Quest 3 passthrough resolution for fine tattoo detail | LOW | Position as "placement preview," not "exact rendering" |

---

## Next Steps (Immediate)

- [ ] Volken: confirm Quest 3 purchase/access
- [ ] Beski: build Magen-Live WebXR POC (Option A, hybrid rendering)
- [ ] Beski: research Three.js globe rendering for VR fallback (Option B)
- [ ] Volken: review BodyCraft AI Phase 1 scope, adjust priorities
- [ ] Document in vault as official project under BodyCraft AI brand

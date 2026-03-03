# Volkenfeld Product Family Vision

> Captured: 2026-03-03, Session with Volken
> Status: PLANNING (not in development)

## Core Concept

One platform architecture, multiple vertical products. Same UI/UX framework,
different data sources and branding per vertical. Only Magen-Live is free.
The paid products fund the ecosystem.

## Products

### 1. Magen-Live (FREE)
- **Domain:** magenlive.org
- **Focus:** Israeli civil defense, conflict intelligence, security awareness
- **Audience:** Israeli citizens, security-aware individuals, families
- **Status:** IN DEVELOPMENT (priority)
- **International branding:** Different name/config for non-Israeli users

### 2. Shipping & Logistics Platform (PAID)
- **Focus:** All-in-one shipping/logistics intelligence hub
- **Audience spectrum:**
  - Customs agents and importers (professional)
  - Private consumers tracking personal purchases
  - Freight forwarders, supply chain managers
- **Core features:**
  - Compare ALL shipping companies and rates
  - Real-time tracking across carriers
  - AI assistant for logistics decisions
  - Personal account centralizing all shipping activity
  - Customs documentation and guidance
  - Rate alerts and cost optimization
- **Research needed:**
  - Pain points across the logistics industry spectrum
  - Existing solutions and their gaps
  - Pricing models (freemium, subscription tiers, per-shipment)
  - APIs available from major carriers
  - Regulatory requirements by country

### 3. Finance & Trading Platform (PAID)
- **Focus:** Stock trading, financial data, market intelligence
- **Audience:** Retail traders, investors, financial professionals
- **Core features:**
  - Real-time market data and analysis
  - AI-powered trading insights
  - Portfolio tracking and management
  - Cross-market comparison tools
  - Personal account with trade history
- **Research needed:**
  - Competitor landscape (TradingView, Bloomberg Terminal alternatives)
  - Data provider costs and APIs
  - Regulatory requirements (financial advice disclaimers)
  - Pricing tiers that work for retail vs professional

## Future Verticals (Ideas)

| Vertical | Focus | Notes |
|----------|-------|-------|
| Music/Entertainment | Series, movies, music discovery | Content aggregation dashboard |
| AI & Dev News | AI news, development tools, research | Tech-focused intelligence |
| Travel & Tourism | Trip planning, destination intel | Location-aware dashboard |
| Surf & Extreme Sports | Weather-dependent sports conditions | Real-time weather/wave data |

## Architecture Principle

All products share:
- Same frontend framework (Vite + TypeScript)
- Same panel/map/dashboard architecture
- Same Vercel deployment pattern
- Variant system for branding (already exists in worldmonitor.app)
- Shared backend APIs where applicable

Each product adds:
- Domain-specific data sources and APIs
- Specialized panels and visualizations
- Tailored AI features
- Payment/subscription system (for paid products)

## Development Approach

- Use BMAD method for product specs and sprint planning
- Ralph Wigen calculated prompts for development
- Split work between Beski (infrastructure) and Luchi (frontend/features)
- Research competitors thoroughly before building

## Revenue Priority

Focus on fastest path to paid revenue:
1. Fix Magen-Live (proves the platform works)
2. Research shipping + finance verticals in parallel
3. Build whichever vertical has clearer product-market fit first
4. Launch with minimal viable paid tier

---

*This document captures Volken's vision. Development starts after Magen-Live is stable.*

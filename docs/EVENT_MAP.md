# 🗺️ Event Map - Technical Specification

**Status**: Planning Phase  
**Version**: 0.1.0-draft  
**Last Updated**: 2025-11-21

---

## 📋 Overview

Interactive fullscreen map showing all published events with minimal UI, maximum accessibility, and responsive design. Users can filter events by category, time, distance, and location with touch/keyboard controls.

---

## 🎯 Design Principles

1. **Mobile First** - Touch-optimized, responsive across all devices
2. **Accessibility** - WCAG 2.1 AA compliant, keyboard navigable
3. **Minimal Design** - Dark mode, no UI clutter, focus on content
4. **Performance** - Lazy loading, optimized markers, smooth animations
5. **Privacy** - LocalStorage only, no tracking, no cookies

---

## 🏗️ Architecture

### Component Structure

```
map.html (Jekyll Template)
├── _sass/map.scss (Styling)
├── assets/js/map.js (Logic)
├── _config.yml (Configuration)
└── _events/*.md (Data Source)
```

### Data Flow

```
Event Markdown (Frontmatter)
  → Jekyll Collection (_events)
    → JSON via Liquid
      → LeafletJS Markers
        → Interactive Map
          → Filter Updates
            → Event Flyer Display
```

---

## 🎨 Visual Design

### Map Style

- **Base Map**: Dark mode tiles (CartoDB Dark Matter or custom)
- **Elements Visible**:
  - Water bodies (subtle blue)
  - Streets (gray lines)
  - Public transport lines (colored)
  - Iconic places (small labels)
  - Town hall & central stations (markers)
- **Elements Hidden**:
  - Buttons, legends, zoom controls
  - Info boxes, tooltips (except attribution watermark)
  - Borders, frames, empty spaces

### Event Flyer

```css
/* Paper flyer effect */
.event-flyer {
  shape: paper-like, slightly bent (3D papercut)
  size: 72% of viewport (responsive)
  position: centered, floating above map
  animation: fade-in (300ms), scale with map zoom
  text: fixed to flyer, scales with flyer
}
```

### Filter Box

```
[17 events][all categories][till sunrise][within 3km][from town hall]
```

Centered near top, shabby chic styling, transforms into readable sentence.

---

## 🛠️ Technical Implementation

### 1. HTML Structure (map.html)

```liquid
---
layout: default
title: Event Map
permalink: /map/
---

<div id="map-container" role="application" aria-label="Interactive Event Map">
  <!-- Leaflet Map -->
  <div id="map" tabindex="0"></div>
  
  <!-- Filter Sentence -->
  <div id="filter-bar" role="region" aria-live="polite">
    <span class="event-count">{{ site.events | where: "published", true | size }} events</span>
    <select id="category-filter" aria-label="Filter by category">
      <option value="all">all categories</option>
      <!-- Populated by JS -->
    </select>
    <!-- More filters -->
  </div>
  
  <!-- Event Flyer (hidden by default) -->
  <details id="event-flyer" class="flyer" aria-hidden="true">
    <summary class="sr-only">Event Details</summary>
    <article class="flyer-content">
      <!-- Populated by JS on marker click -->
    </article>
  </details>
</div>

<!-- Event Data (JSON) -->
<script type="application/json" id="events-data">
  [
    {% for event in site.events %}
    {% if event.published %}
    {
      "id": "{{ event.slug }}",
      "title": "{{ event.title | escape }}",
      "date": "{{ event.date | date_to_xmlschema }}",
      "lat": {{ event.latitude | default: site.map.center.lat }},
      "lng": {{ event.longitude | default: site.map.center.lng }},
      "category": "{{ event.category }}",
      "organizer": {
        "name": "{{ event.organizer }}",
        "avatar": "{{ event.organizer_avatar | default: '/assets/img/default-avatar.svg' }}"
      },
      "venue": {
        "name": "{{ event.venue }}",
        "address": "{{ event.address }}"
      }
    }{% unless forloop.last %},{% endunless %}
    {% endif %}
    {% endfor %}
  ]
</script>
```

### 2. Stylesheet (_sass/map.scss)

```scss
// Base64 Inline Fonts
@font-face {
  font-family: 'Roboto';
  src: url(data:font/woff2;base64,...) format('woff2');
  font-display: swap;
}

@font-face {
  font-family: 'New Rocker';
  src: url(data:font/woff2;base64,...) format('woff2');
  font-display: swap;
}

// Map Container (Fullscreen)
#map-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

#map {
  width: 100%;
  height: 100%;
  z-index: 0;
  
  // Remove Leaflet UI
  .leaflet-control-zoom,
  .leaflet-control-attribution { display: none; }
  
  .leaflet-control-attribution.watermark {
    display: block;
    opacity: 0.3;
    font-size: 0.7rem;
  }
}

// Filter Bar
#filter-bar {
  position: absolute;
  top: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 2rem;
  padding: 1rem 2rem;
  
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  color: #fff;
  
  backdrop-filter: blur(10px);
  
  @media (max-width: 768px) {
    top: 1rem;
    font-size: 0.875rem;
  }
}

// Event Flyer (Paper Effect)
.flyer {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotateZ(-1deg);
  z-index: 200;
  
  width: min(72vw, 600px);
  max-height: 80vh;
  
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 
    0 10px 40px rgba(0, 0, 0, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.2);
  
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s;
  
  &.active {
    opacity: 1;
    visibility: visible;
  }
  
  // Paper bend effect
  &::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    border-width: 0 16px 16px 0;
    border-style: solid;
    border-color: #ddd #fff;
  }
}

.flyer-content {
  padding: 2rem;
  overflow-y: auto;
  max-height: 80vh;
  
  font-family: 'Roboto', sans-serif;
  
  h2 {
    font-family: 'New Rocker', cursive;
    font-size: 2rem;
    margin-bottom: 1rem;
  }
}

// Responsive Scaling
@media (orientation: landscape) {
  .flyer { width: min(60vw, 700px); }
}

@media (orientation: portrait) {
  .flyer { width: 85vw; }
}

// Zoom Synchronization
.flyer {
  font-size: calc(1rem + 0.1vw);
}
```

### 3. JavaScript (assets/js/map.js)

```javascript
// Initialize Map
const map = L.map('map', {
  center: [52.5200, 13.4050], // Berlin (from config)
  zoom: 13,
  zoomControl: false,
  attributionControl: false
});

// Dark Mode Tiles
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '<span class="watermark">© OpenStreetMap</span>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);

// Load Events
const eventsData = JSON.parse(document.getElementById('events-data').textContent);

// Create Markers
const markers = L.markerClusterGroup({
  maxClusterRadius: 50,
  spiderfyOnMaxZoom: true
});

eventsData.forEach(event => {
  const marker = L.marker([event.lat, event.lng], {
    icon: L.icon({
      iconUrl: event.organizer.avatar,
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -40]
    })
  });
  
  marker.eventData = event;
  marker.on('click', showEventFlyer);
  markers.addLayer(marker);
});

map.addLayer(markers);

// Show Event Flyer
function showEventFlyer(e) {
  const event = e.target.eventData;
  const flyer = document.getElementById('event-flyer');
  const content = flyer.querySelector('.flyer-content');
  
  content.innerHTML = `
    <h2>${event.title}</h2>
    <p><strong>Date:</strong> ${new Date(event.date).toLocaleString()}</p>
    <p><strong>Venue:</strong> ${event.venue.name}</p>
    <p><strong>Address:</strong> ${event.venue.address}</p>
  `;
  
  flyer.classList.add('active');
  flyer.setAttribute('aria-hidden', 'false');
}

// Close Flyer (click outside)
document.addEventListener('click', (e) => {
  const flyer = document.getElementById('event-flyer');
  if (!flyer.contains(e.target) && !e.target.closest('.leaflet-marker-icon')) {
    flyer.classList.remove('active');
    flyer.setAttribute('aria-hidden', 'true');
  }
});

// Keyboard Navigation (Escape to close)
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.getElementById('event-flyer').classList.remove('active');
  }
});

// Filter Logic
const categoryFilter = document.getElementById('category-filter');
categoryFilter.addEventListener('change', (e) => {
  const category = e.target.value;
  markers.clearLayers();
  
  const filtered = category === 'all' 
    ? eventsData 
    : eventsData.filter(ev => ev.category === category);
  
  filtered.forEach(event => {
    const marker = L.marker([event.lat, event.lng]);
    marker.eventData = event;
    marker.on('click', showEventFlyer);
    markers.addLayer(marker);
  });
  
  // Update count
  document.querySelector('.event-count').textContent = `${filtered.length} events`;
});
```

---

## ⚙️ Configuration (_config.yml)

```yaml
# Map Settings
map:
  enabled: true
  
  # Default Center
  center:
    lat: 52.5200  # Berlin Town Hall
    lng: 13.4050
    label: "Town Hall"
  
  # Alternative Centers
  locations:
    - name: "Town Hall"
      lat: 52.5200
      lng: 13.4050
    - name: "Central Train Station"
      lat: 52.5251
      lng: 13.3694
  
  # Filter Defaults
  filters:
    category: "all"
    time: "tillSunrise"
    distance: "withinThreeKm"
    location: "townHall"
  
  # Categories
  categories:
    - id: "dancefloor"
      label: "Dancefloor"
      icon: "🕺"
    - id: "onStage"
      label: "On Stage"
      icon: "🎭"
    - id: "exhibitions"
      label: "Exhibitions"
      icon: "🖼️"
    - id: "markets"
      label: "Markets"
      icon: "🛍️"
    - id: "concerts"
      label: "Concerts"
      icon: "🎵"
    - id: "education"
      label: "Education"
      icon: "📚"
    - id: "withChildren"
      label: "With Children"
      icon: "👨‍👩‍👧"
  
  # Time Filters
  time_filters:
    - id: "tillSunrise"
      label: "till sunrise"
      hours: 12
    - id: "thisWeek"
      label: "this week"
      days: 7
    - id: "tillFullMoon"
      label: "till full moon"
      dynamic: true
    - id: "withoutLimit"
      label: "without limit"
      unlimited: true
  
  # Distance Filters
  distance_filters:
    - id: "withinOneKm"
      label: "within 1km"
      meters: 1000
    - id: "withinThreeKm"
      label: "within 3km"
      meters: 3000
    - id: "withinTenKm"
      label: "within 10km"
      meters: 10000
    - id: "geoLocation"
      label: "from my location"
      use_geolocation: true
```

---

## 📝 Event Schema Extension

Add to event frontmatter:

```yaml
---
# ... existing fields ...

# Geolocation
latitude: 52.5200
longitude: 13.4050

# Venue Details
venue: "Kulturzentrum Berlin"
address: "Musterstraße 123, 10115 Berlin"

# Organizer
organizer: "Punk im Hof"
organizer_avatar: "/assets/img/organizers/punkimhof.jpg"

# Category (from _config.yml)
category: "concerts"
---
```

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Now)
- [ ] Create map.html template
- [ ] Implement basic LeafletJS integration
- [ ] Add dark mode tiles
- [ ] Create minimal CSS

### Phase 2: Core Features
- [ ] Event markers with organizer avatars
- [ ] Flyer popup on click
- [ ] Filter bar with sentence display
- [ ] Touch/click outside to close

### Phase 3: Advanced Filters
- [ ] Category filter
- [ ] Time filter (sunrise, week, moon phases)
- [ ] Distance filter (haversine calculation)
- [ ] Location switcher (town hall, station, geolocation)

### Phase 4: Polish
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] Responsive design testing
- [ ] Performance optimization (lazy loading)

### Phase 5: Future Features
- [ ] LocalStorage bookmarks
- [ ] Visitor stats (privacy-friendly)
- [ ] i18n support
- [ ] Custom themes (_themes/dirty/, _themes/minimal/)
- [ ] Export (print, RSS, iCal)
- [ ] Community feedback
- [ ] ML-based recommendations (client-side)
- [ ] Desktop notifications (Web Notifications API)

---

## 🎨 Theming

### Minimal Theme (_themes/minimal/)
- Clean design, high contrast
- System font stack
- Simple marker icons
- Standard flyer layout

### Dirty Theme (_themes/dirty/) - Future
- South Park-style papercut landscape
- 3D paper layers for locations
- Hand-drawn marker icons
- Torn paper flyer with coffee stains

---

## ♿ Accessibility

- **Keyboard**: Tab, Enter, Escape, Arrow keys
- **Screen Reader**: ARIA labels, live regions, semantic HTML
- **Touch**: Large tap targets (min 44x44px), swipe gestures
- **Color Contrast**: WCAG AA (4.5:1 text, 3:1 UI)
- **Focus Indicators**: Visible keyboard focus

---

## 📊 Performance

- **Lazy Loading**: Load events in viewport only
- **Marker Clustering**: Reduce DOM nodes (L.markerClusterGroup)
- **Debounced Filters**: Prevent excessive re-renders
- **Font Subsetting**: Only load used glyphs (base64 inline)
- **Image Optimization**: WebP avatars, lazy loading

---

## 🔒 Privacy

- **No Tracking**: No Google Analytics, no cookies
- **LocalStorage Only**: Bookmarks stored client-side
- **No CDN**: All assets self-hosted
- **Optional Geolocation**: Requires user permission

---

## 📚 Dependencies

### Required
- LeafletJS 1.9+
- CartoDB Dark Matter tiles (or custom)

### Optional
- Leaflet.markercluster (for clustering)
- Turf.js (for distance calculations)

---

## 🧪 Testing

### Manual Tests
- [ ] Desktop (Chrome, Firefox, Safari)
- [ ] Mobile (iOS Safari, Android Chrome)
- [ ] Tablet (landscape/portrait)
- [ ] Screen readers (NVDA, VoiceOver)
- [ ] Keyboard navigation

### Automated Tests
- [ ] Lighthouse (Performance, Accessibility)
- [ ] axe-core (WCAG compliance)
- [ ] Percy (Visual regression)

---

## 📖 Documentation

### User Docs
- How to use the map
- Filter explanations
- Accessibility features

### Developer Docs
- Theming guide
- Custom tile layers
- Filter customization
- Event schema validation

---

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guide
- PR process
- Testing requirements

---

**Next Steps**: Implement Phase 1 (Foundation)

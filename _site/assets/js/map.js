/**
 * EVENT MAP - Minimal Theme Foundation
 * Leaflet-based interactive event map with accessibility
 */

(function() {
  'use strict';

  // Load configuration and event data
  const config = JSON.parse(document.getElementById('map-config').textContent);
  const eventsData = JSON.parse(document.getElementById('events-data').textContent);
  
  let map, markers;
  let activeFilters = { ...config.defaults };
  
  /**
   * Initialize Leaflet Map
   */
  function initMap() {
    map = L.map('map', {
      center: [config.center.lat, config.center.lng],
      zoom: config.zoom,
      zoomControl: false,
      attributionControl: false
    });
    
    // Add dark mode tiles
    L.tileLayer(config.tiles.url, {
      attribution: config.tiles.attribution,
      maxZoom: config.tiles.maxZoom,
      subdomains: 'abcd'
    }).addTo(map);
    
    // Add optional watermark attribution
    L.control.attribution({
      position: 'bottomright',
      prefix: false,
      className: 'watermark'
    }).addTo(map).addAttribution(config.tiles.attribution);
  }
  
  /**
   * Create Event Markers
   */
  function createMarkers(events) {
    const markerGroup = L.layerGroup();
    
    events.forEach(event => {
      // Skip events without coordinates
      if (!event.lat || !event.lng) {
        console.warn('Event missing coordinates:', event.title);
        return;
      }
      
      // Create marker with organizer avatar
      const marker = L.marker([event.lat, event.lng], {
        icon: L.icon({
          iconUrl: event.organizer.avatar,
          iconSize: [40, 40],
          iconAnchor: [20, 40],
          popupAnchor: [0, -40],
          className: 'event-marker'
        }),
        title: event.title,
        alt: `Event: ${event.title} by ${event.organizer.name}`
      });
      
      // Store event data for flyer display
      marker.eventData = event;
      
      // Click handler
      marker.on('click', function() {
        showFlyer(this.eventData);
      });
      
      // Keyboard handler
      marker.on('keypress', function(e) {
        if (e.originalEvent.key === 'Enter' || e.originalEvent.key === ' ') {
          e.originalEvent.preventDefault();
          showFlyer(this.eventData);
        }
      });
      
      markerGroup.addLayer(marker);
    });
    
    return markerGroup;
  }
  
  /**
   * Filter Events
   */
  function filterEvents() {
    const filtered = eventsData.filter(event => {
      // Category filter
      if (activeFilters.category !== 'all' && event.category !== activeFilters.category) {
        return false;
      }
      
      // Time filter
      if (!matchesTimeFilter(event, activeFilters.time)) {
        return false;
      }
      
      // Distance filter
      if (!matchesDistanceFilter(event, activeFilters.distance)) {
        return false;
      }
      
      return true;
    });
    
    // Update event count
    document.getElementById('event-count').textContent = `${filtered.length} events`;
    
    // Recreate markers
    if (markers) {
      map.removeLayer(markers);
    }
    markers = createMarkers(filtered);
    markers.addTo(map);
  }
  
  /**
   * Time Filter Logic
   */
  function matchesTimeFilter(event, filterId) {
    if (filterId === 'withoutLimit') return true;
    
    const eventDate = new Date(event.date);
    const now = new Date();
    const filter = config.filters.time.find(f => f.id === filterId);
    
    if (!filter) return true;
    
    if (filter.hours) {
      const maxDate = new Date(now.getTime() + filter.hours * 60 * 60 * 1000);
      return eventDate <= maxDate;
    }
    
    if (filter.days) {
      const maxDate = new Date(now.getTime() + filter.days * 24 * 60 * 60 * 1000);
      return eventDate <= maxDate;
    }
    
    if (filter.dynamic && filterId === 'tillFullMoon') {
      // TODO: Implement moon phase calculation
      return true;
    }
    
    return true;
  }
  
  /**
   * Distance Filter Logic (Haversine Formula)
   */
  function matchesDistanceFilter(event, filterId) {
    const filter = config.filters.distance.find(f => f.id === filterId);
    if (!filter || !filter.meters) return true;
    
    // Get current map center as reference point
    const center = map.getCenter();
    const distance = haversineDistance(
      center.lat, center.lng,
      event.lat, event.lng
    );
    
    return distance <= filter.meters;
  }
  
  /**
   * Haversine Distance Calculation
   */
  function haversineDistance(lat1, lon1, lat2, lon2) {
    const R = 6371000; // Earth radius in meters
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }
  
  function toRad(deg) {
    return deg * (Math.PI / 180);
  }
  
  /**
   * Show Event Flyer
   */
  function showFlyer(eventData) {
    const flyer = document.getElementById('event-flyer');
    const content = flyer.querySelector('.flyer-content');
    
    // Format date
    const eventDate = new Date(eventData.date);
    const dateStr = eventDate.toLocaleString('de-DE', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
    
    // Populate flyer
    content.innerHTML = `
      <h2 id="flyer-title">${escapeHtml(eventData.title)}</h2>
      <p><strong>📅 ${dateStr}</strong></p>
      ${eventData.venue.name ? `<p><strong>📍 Venue:</strong> ${escapeHtml(eventData.venue.name)}</p>` : ''}
      ${eventData.venue.address ? `<p>${escapeHtml(eventData.venue.address)}</p>` : ''}
      ${eventData.organizer.name ? `<p><strong>👤 Organizer:</strong> ${escapeHtml(eventData.organizer.name)}</p>` : ''}
      ${eventData.contact.website ? `<p><a href="${eventData.contact.website}" target="_blank" rel="noopener">🌐 Website</a></p>` : ''}
    `;
    
    // Show flyer
    flyer.classList.add('active');
    flyer.setAttribute('aria-hidden', 'false');
    
    // Focus trap
    const closeBtn = document.getElementById('flyer-close');
    closeBtn.focus();
  }
  
  /**
   * Hide Event Flyer
   */
  function hideFlyer() {
    const flyer = document.getElementById('event-flyer');
    flyer.classList.remove('active');
    flyer.setAttribute('aria-hidden', 'true');
  }
  
  /**
   * HTML Escape (XSS Prevention)
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  /**
   * Setup Filter Listeners
   */
  function setupFilters() {
    // Category filter
    document.getElementById('category-filter').addEventListener('change', function(e) {
      activeFilters.category = e.target.value;
      filterEvents();
    });
    
    // Time filter
    document.getElementById('time-filter').addEventListener('change', function(e) {
      activeFilters.time = e.target.value;
      filterEvents();
    });
    
    // Distance filter
    document.getElementById('distance-filter').addEventListener('change', function(e) {
      activeFilters.distance = e.target.value;
      filterEvents();
    });
    
    // Location filter (changes map center)
    document.getElementById('location-filter').addEventListener('change', function(e) {
      const option = e.target.selectedOptions[0];
      const lat = parseFloat(option.dataset.lat);
      const lng = parseFloat(option.dataset.lng);
      
      if (lat && lng) {
        map.setView([lat, lng], config.zoom);
        activeFilters.location = e.target.value;
        filterEvents();
      }
    });
  }
  
  /**
   * Setup Keyboard Navigation
   */
  function setupKeyboardNav() {
    document.addEventListener('keydown', function(e) {
      // Escape closes flyer
      if (e.key === 'Escape') {
        hideFlyer();
      }
    });
    
    // Close button
    document.getElementById('flyer-close').addEventListener('click', hideFlyer);
  }
  
  /**
   * Setup Click Outside to Close
   */
  function setupClickOutside() {
    document.addEventListener('click', function(e) {
      const flyer = document.getElementById('event-flyer');
      if (!flyer.classList.contains('active')) return;
      
      // Check if click is outside flyer and not on a marker
      if (!flyer.contains(e.target) && !e.target.closest('.leaflet-marker-icon')) {
        hideFlyer();
      }
    });
  }
  
  /**
   * Initialize Application
   */
  function init() {
    initMap();
    filterEvents(); // Initial render
    setupFilters();
    setupKeyboardNav();
    setupClickOutside();
    
    console.log(`✅ Event Map initialized with ${eventsData.length} events`);
  }
  
  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
})();

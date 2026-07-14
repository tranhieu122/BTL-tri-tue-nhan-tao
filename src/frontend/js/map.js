/**
 * map.js - Module bản đồ Việt Nam sử dụng Leaflet.js
 * Thay thế SVG bằng bản đồ tương tác thực tế (OpenStreetMap).
 * Giữ nguyên Public API để tương thích với app.js và visualization.js.
 */

const VietnamMap = (() => {
    // ---- State ----
    let map = null;
    let nodes = [];
    let edges = [];
    let nodeMarkers = {};      // {cityName: L.circleMarker}
    let edgePolylines = {};    // {"cityA|cityB": L.polyline}
    let edgeLabels = {};       // {"cityA|cityB": L.tooltip}
    let pathPolyline = null;   // L.polyline for final path
    let onNodeClick = null;
    let onEdgeClick = null;
    let onNodeHover = null;
    let onNodeOut = null;
    let showLabels = false;

    // Layers
    let edgesLayer = null;
    let nodesLayer = null;
    let pathLayer = null;
    let labelsLayer = null;

    /**
     * Tạo key chuẩn cho edge (luôn sắp xếp theo alphabet).
     */
    function edgeKey(city1, city2) {
        return [city1, city2].sort().join('|');
    }

    /**
     * Khởi tạo bản đồ.
     */
    function init(graphData, nodeClickHandler, edgeClickHandler, nodeHoverHandler, nodeOutHandler) {
        nodes = graphData.nodes || [];
        edges = graphData.edges || [];
        onNodeClick = nodeClickHandler;
        onEdgeClick = edgeClickHandler;
        onNodeHover = nodeHoverHandler;
        onNodeOut = nodeOutHandler;

        // Khởi tạo Leaflet map
        map = L.map('leaflet-map', {
            zoomControl: true,
            attributionControl: true,
            minZoom: 5,
            maxZoom: 18
        });

        // Sử dụng Google Maps với tham số hl=vi (Tiếng Việt) để hiển thị chuẩn xác chủ quyền Biển Đông
        L.tileLayer('http://mt1.google.com/vt/lyrs=m&hl=vi&x={x}&y={y}&z={z}', {
            attribution: '&copy; Google Maps',
            maxZoom: 20
        }).addTo(map);

        // Tạo các layer groups
        edgesLayer = L.layerGroup().addTo(map);
        pathLayer = L.layerGroup().addTo(map);
        nodesLayer = L.layerGroup().addTo(map);
        labelsLayer = L.layerGroup().addTo(map);

        // Render
        renderEdges();
        renderNodes();

        // Fit bounds tới Việt Nam
        if (nodes.length > 0) {
            const bounds = L.latLngBounds(nodes.map(n => [n.lat, n.lng]));
            map.fitBounds(bounds.pad(0.1));
        }
    }

    /**
     * Vẽ các cạnh (đường nối giữa tỉnh thành).
     */
    function renderEdges() {
        edgesLayer.clearLayers();
        labelsLayer.clearLayers();
        edgePolylines = {};
        edgeLabels = {};

        edges.forEach((edge, index) => {
            const fromNode = nodes.find(n => n.name === edge.from);
            const toNode = nodes.find(n => n.name === edge.to);
            if (!fromNode || !toNode) return;

            const latlngs = [[fromNode.lat, fromNode.lng], [toNode.lat, toNode.lng]];
            const key = edgeKey(edge.from, edge.to);

            // Style dựa trên trạng thái
            const style = edge.blocked ? {
                color: '#f43f6e',
                weight: 2.5,
                opacity: 0.7,
                dashArray: '8, 4',
                className: 'leaflet-edge blocked'
            } : {
                color: 'rgba(99, 102, 241, 0.45)',
                weight: 1.8,
                opacity: 1,
                className: 'leaflet-edge'
            };

            const polyline = L.polyline(latlngs, style).addTo(edgesLayer);

            // Invisible thicker line for easier clicking
            const clickLine = L.polyline(latlngs, {
                color: 'transparent',
                weight: 18,
                opacity: 0
            }).addTo(edgesLayer);

            // Hover effect
            clickLine.on('mouseover', () => {
                if (!edge.blocked && !polyline.options.className?.includes('in-path')) {
                    polyline.setStyle({ color: 'rgba(99, 102, 241, 0.8)', weight: 4 });
                }
            });
            clickLine.on('mouseout', () => {
                if (!edge.blocked && !polyline.options.className?.includes('in-path')) {
                    polyline.setStyle({ color: 'rgba(99, 102, 241, 0.45)', weight: 1.8 });
                }
            });

            // Tooltip chỉ hiển thị số km dạng chữ chạy theo chuột (không có khung)
            clickLine.bindTooltip(`${edge.distance} km`, {
                sticky: true,
                direction: 'top',
                className: 'edge-hover-km',
                opacity: 1
            });

            // Click handler
            clickLine.on('click', (e) => {
                L.DomEvent.stopPropagation(e);
                if (onEdgeClick) {
                    onEdgeClick(edge.from, edge.to, index, edge.distance);
                }
            });

            // Store reference
            polyline._edgeData = edge;
            polyline._edgeIndex = index;
            edgePolylines[key] = polyline;

            // Distance label (tooltip marker at midpoint)
            const midLat = (fromNode.lat + toNode.lat) / 2;
            const midLng = (fromNode.lng + toNode.lng) / 2;

            const labelMarker = L.marker([midLat, midLng], {
                icon: L.divIcon({
                    className: 'edge-distance-label' + (showLabels ? ' show' : ''),
                    html: `<span>${edge.distance}km</span>`,
                    iconSize: [50, 16],
                    iconAnchor: [25, 8]
                }),
                interactive: false
            }).addTo(labelsLayer);

            edgeLabels[key] = { marker: labelMarker, edge: edge };
        });
    }

    /**
     * Vẽ các node (tỉnh thành).
     */
    function renderNodes() {
        nodesLayer.clearLayers();
        nodeMarkers = {};

        const tooltip = document.getElementById('map-tooltip');
        const tooltipCity = document.getElementById('tooltip-city');
        const tooltipCoords = document.getElementById('tooltip-coords');

        nodes.forEach(node => {
            const isSpecial = node.type === 'special_zone';

            const marker = L.circleMarker([node.lat, node.lng], {
                radius: isSpecial ? 4 : 4.8,
                fillColor: '#ffffff',
                fillOpacity: 1,
                color: '#70757a',
                weight: 1.8,
                className: 'leaflet-city-marker'
            }).addTo(nodesLayer);

            // City label
            const label = L.marker([node.lat, node.lng], {
                icon: L.divIcon({
                    className: 'leaflet-city-label',
                    html: `<span>${node.name}</span>`,
                    iconSize: [80, 20],
                    iconAnchor: [40, -10]
                }),
                interactive: false
            }).addTo(nodesLayer);

            marker._cityName = node.name;
            marker._cityLabel = label;
            marker._nodeData = node;

            // Hover tooltip
            marker.on('mouseover', (e) => {
                const containerRect = document.getElementById('map-container').getBoundingClientRect();
                const point = map.latLngToContainerPoint(e.latlng);

                tooltipCity.textContent = node.name;
                tooltipCoords.textContent = `${node.lat.toFixed(4)}°N, ${node.lng.toFixed(4)}°E`;

                tooltip.style.left = `${point.x + 15}px`;
                tooltip.style.top = `${point.y - 10}px`;
                tooltip.classList.add('visible');

                // Hover style
                marker.setStyle({ color: '#06c8ec', weight: 3, radius: 10 });
            });

            marker.on('mouseout', () => {
                tooltip.classList.remove('visible');
                // Restore style based on current state
                const state = marker._currentState;
                if (!state) {
                    marker.setStyle({
                        fillColor: '#1e3d6e',
                        color: 'rgba(91, 138, 245, 0.7)',
                        weight: 2,
                        radius: isSpecial ? 6 : 8
                    });
                }
            });

            // Click handler
            marker.on('click', (e) => {
                L.DomEvent.stopPropagation(e);
                if (onNodeClick) {
                    onNodeClick(node.name);
                }
            });

            nodeMarkers[node.name] = marker;
        });
    }

    /**
     * Cập nhật trạng thái visual cho node.
     */
    function setNodeState(cityName, state) {
        const marker = nodeMarkers[cityName];
        if (!marker) return;

        marker._currentState = state;

        const styles = {
            'start': { fillColor: '#1a73e8', color: '#ffffff', weight: 3, radius: 9, fillOpacity: 1, className: 'leaflet-city-marker start-node' },
            'end': { fillColor: '#ea4335', color: '#b31404', weight: 2, radius: 10, fillOpacity: 1, className: 'leaflet-city-marker end-node' },
            'visited': { fillColor: 'rgba(26, 115, 232, 0.2)', color: '#1a73e8', weight: 1, radius: 7, fillOpacity: 0.8, className: 'leaflet-city-marker visited-node' },
            'frontier': { fillColor: 'rgba(251, 188, 4, 0.5)', color: '#fbbc04', weight: 2, radius: 7, fillOpacity: 0.8, className: 'leaflet-city-marker frontier-node' },
            'current': { fillColor: '#ffffff', color: '#1a73e8', weight: 3, radius: 10, fillOpacity: 1, className: 'leaflet-city-marker current-node' },
            'in-path': { fillColor: '#1a73e8', color: '#ffffff', weight: 2, radius: 8, fillOpacity: 1, className: 'leaflet-city-marker in-path-node' }
        };

        const defaultStyle = {
            fillColor: '#ffffff',
            color: '#70757a',
            weight: 2,
            radius: 6,
            fillOpacity: 1,
            className: 'leaflet-city-marker'
        };

        marker.setStyle(state && styles[state] ? styles[state] : defaultStyle);

        // Update label class
        const labelEl = marker._cityLabel?._icon;
        if (labelEl) {
            labelEl.classList.remove('start-label', 'end-label');
            if (state === 'start') labelEl.classList.add('start-label');
            if (state === 'end') labelEl.classList.add('end-label');
        }
    }

    /**
     * Cập nhật trạng thái edge.
     */
    function setEdgeState(fromCity, toCity, state) {
        const key = edgeKey(fromCity, toCity);
        const polyline = edgePolylines[key];
        if (!polyline) return;

        const styles = {
            'in-path': { color: '#1a73e8', weight: 4, opacity: 1 },
            'exploring': { color: '#fbbc04', weight: 3, opacity: 0.8 }
        };

        if (state && styles[state]) {
            polyline.setStyle(styles[state]);
            polyline.options.className = 'leaflet-edge ' + state;
        } else {
            polyline.setStyle({ color: '#bdc1c6', weight: 2.5, opacity: 1 });
            polyline.options.className = 'leaflet-edge';
        }
    }

    /**
     * Toggle chướng ngại vật trên edge.
     */
    function toggleEdgeBlock(fromCity, toCity, blocked) {
        const idx = edges.findIndex(e =>
            (e.from === fromCity && e.to === toCity) ||
            (e.from === toCity && e.to === fromCity)
        );

        if (idx >= 0) {
            edges[idx].blocked = blocked;
            const key = edgeKey(fromCity, toCity);
            const polyline = edgePolylines[key];
            if (polyline) {
                if (blocked) {
                    polyline.setStyle({ color: '#f43f6e', weight: 2.5, opacity: 0.7, dashArray: '8, 4' });
                } else {
                    polyline.setStyle({ color: 'rgba(99, 102, 241, 0.45)', weight: 2.5, opacity: 1, dashArray: null });
                }
            }
        }
    }

    /**
     * Vẽ đường đi cuối cùng (animated polyline).
     */
    function drawPath(path) {
        clearPath();
        if (!path || path.length < 2) return;

        const latlngs = [];
        let totalDistance = 0;

        for (let i = 0; i < path.length; i++) {
            const city = path[i];
            const node = nodes.find(n => n.name === city);
            if (node) latlngs.push([node.lat, node.lng]);

            if (i > 0) {
                // Calculate distance from previous to current
                const prevCity = path[i - 1];
                const edge = edges.find(e =>
                    (e.from === prevCity && e.to === city) ||
                    (e.from === city && e.to === prevCity)
                );
                if (edge) totalDistance += edge.distance;
            }
        }

        // Draw outline (thicker, darker)
        L.polyline(latlngs, {
            color: '#1e3a8a', // Dark blue border
            weight: 8,
            opacity: 0.9,
            lineCap: 'round',
            lineJoin: 'round'
        }).addTo(pathLayer);

        // Draw inner line (Google Maps Blue)
        pathPolyline = L.polyline(latlngs, {
            color: '#3b82f6', // Bright blue
            weight: 3,
            opacity: 1,
            lineCap: 'round',
            lineJoin: 'round',
            className: 'leaflet-path-line'
        }).addTo(pathLayer);

        // Add Google Maps style tooltip at the midpoint
        if (latlngs.length > 1) {
            const midIndex = Math.floor(latlngs.length / 2);
            let midLatLng = latlngs[midIndex];

            // If even number of points, interpolate between the two middle points for exact center
            if (latlngs.length % 2 === 0) {
                const p1 = latlngs[midIndex - 1];
                const p2 = latlngs[midIndex];
                midLatLng = [
                    (p1[0] + p2[0]) / 2,
                    (p1[1] + p2[1]) / 2
                ];
            }

            // Estimate time (assume average speed of 60km/h) -> 1 km = 1 min
            const timeMin = Math.round(totalDistance / 60 * 60); // minutes
            const hours = Math.floor(timeMin / 60);
            const mins = timeMin % 60;
            const timeStr = hours > 0 ? `${hours} h ${mins} p` : `${mins} phút`;

            const tooltipHtml = `
                <div class="gm-tooltip">
                    <div class="gm-time"><span class="car-icon">🚘</span> ${timeStr}</div>
                    <div class="gm-dist">${totalDistance.toFixed(1)} km</div>
                </div>
            `;

            L.marker(midLatLng, {
                icon: L.divIcon({
                    className: 'gm-tooltip-container',
                    html: tooltipHtml,
                    iconSize: [80, 40],
                    iconAnchor: [40, 50]
                }),
                interactive: false
            }).addTo(pathLayer);
        }
    }

    /**
     * Vẽ đường đi phụ (dùng cho tính năng Dual Compare).
     */
    function drawSecondaryPath(path) {
        if (!path || path.length < 2) return;

        const latlngs = [];
        let totalDistance = 0;

        for (let i = 0; i < path.length; i++) {
            const city = path[i];
            const node = nodes.find(n => n.name === city);
            if (node) latlngs.push([node.lat, node.lng]);

            if (i > 0) {
                const prevCity = path[i - 1];
                const edge = edges.find(e =>
                    (e.from === prevCity && e.to === city) ||
                    (e.from === city && e.to === prevCity)
                );
                if (edge) totalDistance += edge.distance;
            }
        }

        // Draw inner line (Red) with dash for secondary path
        L.polyline(latlngs, {
            color: '#ea4335', // Red
            weight: 5,
            opacity: 0.9,
            lineCap: 'round',
            lineJoin: 'round',
            dashArray: '10, 10',
            className: 'leaflet-path-line-secondary'
        }).addTo(pathLayer);

        // Add Google Maps style tooltip at the midpoint
        if (latlngs.length > 1) {
            const midIndex = Math.floor(latlngs.length / 2);
            let midLatLng = latlngs[midIndex];

            if (latlngs.length % 2 === 0) {
                const p1 = latlngs[midIndex - 1];
                const p2 = latlngs[midIndex];
                midLatLng = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2];
            }

            const timeMin = Math.round(totalDistance / 60 * 60); // minutes
            const hours = Math.floor(timeMin / 60);
            const mins = timeMin % 60;
            const timeStr = hours > 0 ? `${hours} h ${mins} p` : `${mins} phút`;

            const tooltipHtml = `
                <div class="gm-tooltip secondary">
                    <div class="gm-time" style="color:#d93025"><span class="car-icon">🚘</span> ${timeStr}</div>
                    <div class="gm-dist">${totalDistance.toFixed(1)} km</div>
                </div>
            `;

            L.marker(midLatLng, {
                icon: L.divIcon({
                    className: 'gm-tooltip-container secondary-offset',
                    html: tooltipHtml,
                    iconSize: [80, 40],
                    iconAnchor: [40, 0] // Offset it so it doesn't overlap perfectly with primary
                }),
                interactive: false
            }).addTo(pathLayer);
        }
    }

    /**
     * Xóa đường đi.
     */
    function clearPath() {
        pathLayer.clearLayers();
        pathPolyline = null;
    }

    /**
     * Reset tất cả trạng thái visual.
     */
    function resetAllStates() {
        // Reset nodes
        Object.keys(nodeMarkers).forEach(cityName => {
            setNodeState(cityName, null);
        });

        // Reset edges
        Object.keys(edgePolylines).forEach(key => {
            const polyline = edgePolylines[key];
            const edgeData = polyline._edgeData;
            if (edgeData && edgeData.blocked) {
                polyline.setStyle({ color: '#f43f6e', weight: 2.5, opacity: 0.7, dashArray: '8, 4' });
            } else {
                polyline.setStyle({ color: '#bdc1c6', weight: 2.5, opacity: 1, dashArray: null });
            }
            polyline.options.className = 'leaflet-edge';
        });

        clearPath();
    }

    /**
     * Toggle hiển thị labels khoảng cách.
     */
    function toggleDistanceLabels() {
        showLabels = !showLabels;
        Object.values(edgeLabels).forEach(({ marker }) => {
            const icon = marker._icon;
            if (icon) {
                icon.querySelector('.edge-distance-label')?.classList.toggle('show', showLabels);
                // Also toggle parent
                icon.classList.toggle('show', showLabels);
            }
        });
        // Re-render labels with correct visibility
        renderEdgeLabels();
        return showLabels;
    }

    /**
     * Re-render chỉ edge labels (khi toggle visibility).
     */
    function renderEdgeLabels() {
        labelsLayer.clearLayers();
        edgeLabels = {};

        edges.forEach(edge => {
            const fromNode = nodes.find(n => n.name === edge.from);
            const toNode = nodes.find(n => n.name === edge.to);
            if (!fromNode || !toNode) return;

            const key = edgeKey(edge.from, edge.to);
            const midLat = (fromNode.lat + toNode.lat) / 2;
            const midLng = (fromNode.lng + toNode.lng) / 2;

            const labelMarker = L.marker([midLat, midLng], {
                icon: L.divIcon({
                    className: 'edge-distance-label' + (showLabels ? ' show' : ''),
                    html: `<span>${edge.distance}km</span>`,
                    iconSize: [50, 16],
                    iconAnchor: [25, 8]
                }),
                interactive: false
            }).addTo(labelsLayer);

            edgeLabels[key] = { marker: labelMarker, edge: edge };
        });
    }

    /**
     * Lấy danh sách tên tỉnh thành.
     */
    function getCityNames() {
        return nodes.map(n => n.name);
    }

    /**
     * Lấy trạng thái edges (blocked/unblocked).
     */
    function getBlockedEdges() {
        return edges.filter(e => e.blocked).map(e => [e.from, e.to]);
    }

    /**
     * Lấy vị trí của một tỉnh thành (trả về latlng).
     */
    function getNodePosition(cityName) {
        const node = nodes.find(n => n.name === cityName);
        if (node) return { x: node.lng, y: node.lat };
        return null;
    }

    /**
     * Cập nhật hiển thị khoảng cách của một cạnh trên bản đồ.
     */
    function updateEdgeDistanceLabel(city1, city2, newDistance) {
        // Cập nhật trong data
        const edge = edges.find(e =>
            (e.from === city1 && e.to === city2) ||
            (e.from === city2 && e.to === city1)
        );
        if (edge) {
            edge.distance = newDistance;
        }

        // Cập nhật label marker
        const key = edgeKey(city1, city2);
        const labelData = edgeLabels[key];
        if (labelData && labelData.marker) {
            const icon = labelData.marker._icon;
            if (icon) {
                const span = icon.querySelector('span');
                if (span) span.textContent = `${newDistance}km`;
            }
        }
    }

    /**
     * Xóa tất cả chướng ngại vật trên bản đồ.
     */
    function clearAllBlocks() {
        edges.forEach(edge => {
            if (edge.blocked) {
                edge.blocked = false;
                const key = edgeKey(edge.from, edge.to);
                const polyline = edgePolylines[key];
                if (polyline) {
                    polyline.setStyle({ color: 'rgba(99, 102, 241, 0.45)', weight: 1.8, opacity: 1, dashArray: null });
                }
            }
        });
    }

    /**
     * Highlight đường đi (dùng cho visualization).
     */
    function highlightPath(path) {
        drawPath(path);
    }

    // Public API (giữ nguyên interface cũ)
    return {
        init,
        setNodeState,
        setEdgeState,
        toggleEdgeBlock,
        drawPath,
        clearPath,
        resetAllStates,
        toggleDistanceLabels,
        getCityNames,
        getBlockedEdges,
        getNodePosition,
        renderEdges,
        updateEdgeDistanceLabel,
        clearAllBlocks,
        highlightPath,
        drawSecondaryPath
    };
})();

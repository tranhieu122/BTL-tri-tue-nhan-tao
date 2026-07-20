/**
 * app.js - Module chính điều phối toàn bộ ứng dụng
 * Quản lý state, xử lý events, và kết nối các module.
 */

const App = (() => {
    // ---- Application State ----
    const state = {
        startCity: null,
        endCity: null,
        mode: 'select',      // 'select' | 'obstacle' | 'weight'
        isStepMode: false,
        isRunning: false,
        graphLoaded: false,
        lastResult: null
    };

    /**
     * Khởi tạo ứng dụng.
     */
    async function init() {
        showToast('Đang kết nối tới server...', 'info');

        // Kiểm tra kết nối API
        const connected = await AlgorithmsAPI.checkConnection();
        updateConnectionStatus(connected);

        if (!connected) {
            showToast('⚠️ Không kết nối được server. Hãy chạy: python app.py', 'error');
            return;
        }

        try {
            // Lấy dữ liệu đồ thị
            const graphData = await AlgorithmsAPI.fetchGraph();

            // Khởi tạo bản đồ
            VietnamMap.init(graphData, handleNodeClick, handleEdgeClick, handleNodeHover, handleNodeOut);

            // Populate dropdowns
            populateCitySelects(graphData.nodes);

            // Cập nhật badge counts
            document.getElementById('city-count').textContent = graphData.nodes.length;
            document.getElementById('edge-count').textContent = graphData.edges.length;

            state.graphLoaded = true;
            showToast('✅ Đã tải bản đồ Việt Nam thành công!', 'success');

        } catch (error) {
            showToast(`❌ Lỗi tải dữ liệu: ${error.message}`, 'error');
        }

        // Setup event listeners
        setupEventListeners();
    }

    /**
     * Setup tất cả event listeners.
     */
    function setupEventListeners() {
        // ---- Toolbar Buttons ----
        document.getElementById('btn-select-mode').addEventListener('click', () => setMode('select'));
        document.getElementById('btn-obstacle-mode').addEventListener('click', () => setMode('obstacle'));
        document.getElementById('btn-weight-mode').addEventListener('click', () => setMode('weight'));
        document.getElementById('btn-clear-obstacles').addEventListener('click', clearObstacles);
        document.getElementById('btn-reset-all').addEventListener('click', resetAll);
        document.getElementById('btn-toggle-labels').addEventListener('click', () => {
            const showing = VietnamMap.toggleDistanceLabels();
            showToast(showing ? '📏 Hiện khoảng cách' : '📏 Ẩn khoảng cách', 'info');
        });

        // ---- Algorithm Controls ----
        document.getElementById('btn-find-path').addEventListener('click', findPath);
        document.getElementById('btn-step-mode').addEventListener('click', toggleStepMode);

        // ---- Playback Controls ----
        document.getElementById('btn-prev-step').addEventListener('click', () => Visualization.prevStep());
        document.getElementById('btn-play-pause').addEventListener('click', () => Visualization.togglePlay());
        document.getElementById('btn-next-step').addEventListener('click', () => Visualization.nextStep());

        // ---- Speed Slider ----
        const speedSlider = document.getElementById('speed-slider');
        const speedValue = document.getElementById('speed-value');
        speedSlider.addEventListener('input', (e) => {
            const speed = parseInt(e.target.value);
            speedValue.textContent = `${speed}ms`;
            Visualization.setSpeed(speed);
        });

        // ---- City Selects ----
        document.getElementById('start-select').addEventListener('change', (e) => {
            if (e.target.value) setStartCity(e.target.value);
        });
        document.getElementById('end-select').addEventListener('change', (e) => {
            if (e.target.value) setEndCity(e.target.value);
        });

        // ---- Compare ----
        document.getElementById('btn-compare').addEventListener('click', compareAll);
        document.getElementById('btn-dual-compare').addEventListener('click', dualCompare);
        document.getElementById('btn-close-compare').addEventListener('click', () => Comparison.hide());
        document.getElementById('comparison-metric').addEventListener('change', (event) => Comparison.renderChart(event.target.value));
        document.getElementById('btn-export-comparison').addEventListener('click', () => {
            if (Comparison.exportCsv()) showToast('&#128190; Đã xuất dữ liệu so sánh dạng CSV', 'success');
        });

        // ---- Demo scenarios & search history ----
        document.getElementById('scenario-select').addEventListener('change', applyScenario);
        document.getElementById('btn-refresh-history').addEventListener('click', loadHistory);
        document.getElementById('btn-random-route').addEventListener('click', createRandomRoute);
        document.getElementById('algorithm-select').addEventListener('change', updateAlgorithmInsight);

        // ---- Tools ----
        document.getElementById('btn-random-blocks').addEventListener('click', generateRandomBlocks);

        // ---- Window resize ----
        window.addEventListener('resize', () => {
            if (Comparison.getData()) {
                Comparison.renderChart();
            }
        });

        // ---- City Search Box ----
        const searchInput = document.getElementById('city-search');
        const searchResults = document.getElementById('city-search-results');
        
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.trim().toLowerCase();
            searchResults.innerHTML = '';
            
            if (query.length === 0) {
                searchResults.classList.remove('visible');
                return;
            }

            const cityNames = VietnamMap.getCityNames();
            const matches = cityNames.filter(name => 
                name.toLowerCase().includes(query)
            ).slice(0, 8);

            if (matches.length === 0) {
                searchResults.classList.remove('visible');
                return;
            }

            matches.forEach(name => {
                const item = document.createElement('div');
                item.className = 'search-result-item';
                item.innerHTML = `<span class="result-icon">📍</span>${name}`;
                item.addEventListener('click', () => {
                    handleNodeClick(name);
                    searchInput.value = '';
                    searchResults.classList.remove('visible');
                });
                searchResults.appendChild(item);
            });

            searchResults.classList.add('visible');
        });

        searchInput.addEventListener('blur', () => {
            setTimeout(() => searchResults.classList.remove('visible'), 200);
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                searchInput.value = '';
                searchResults.classList.remove('visible');
            }
        });

        loadHistory();
        updateAlgorithmInsight();
    }

    const ALGORITHM_INSIGHTS = {
        astar: {
            symbol: 'f(n) = g(n) + h(n)', badge: 'Optimal',
            title: 'A* Search: tối ưu với heuristic admissible',
            text: 'Kết hợp chi phí đã đi và ước lượng đến đích để thu hẹp không gian tìm kiếm.'
        },
        greedy: {
            symbol: 'f(n) = h(n)', badge: 'Nhanh',
            title: 'Greedy Best-First: ưu tiên điểm gần đích',
            text: 'Chỉ dùng heuristic nên thường duyệt ít node, nhưng không đảm bảo đường đi ngắn nhất.'
        },
        dijkstra: {
            symbol: 'f(n) = g(n)', badge: 'Optimal',
            title: 'Dijkstra: chuẩn tối ưu trọng số dương',
            text: 'Mở rộng theo tổng chi phí nhỏ nhất và luôn tìm được đường tối ưu với cạnh có trọng số không âm.'
        },
        bfs: {
            symbol: 'FIFO Queue', badge: 'Đủ',
            title: 'BFS: tối ưu số cạnh, không tối ưu km',
            text: 'Duyệt theo từng lớp nên tìm đường ít chặng nhất, nhưng không phù hợp khi mỗi cạnh có khoảng cách khác nhau.'
        },
        dfs: {
            symbol: 'LIFO Stack', badge: 'Khám phá',
            title: 'DFS: đi sâu trước, không đảm bảo tối ưu',
            text: 'Tốn ít bộ nhớ hơn nhưng thứ tự duyệt có thể tạo ra đường vòng và bỏ lỡ phương án tốt hơn.'
        },
        ucs: {
            symbol: 'Priority Queue: g(n)', badge: 'Optimal',
            title: 'Uniform Cost Search: ưu tiên chi phí thực',
            text: 'Tương đương Dijkstra trên đồ thị này; đảm bảo tối ưu khi trọng số cạnh dương.'
        }
    };

    function updateAlgorithmInsight() {
        const algorithm = document.getElementById('algorithm-select').value;
        const insight = ALGORITHM_INSIGHTS[algorithm];
        if (!insight) return;
        document.getElementById('algo-insight-symbol').textContent = insight.symbol;
        document.getElementById('algo-insight-badge').textContent = insight.badge;
        document.getElementById('algo-insight-title').textContent = insight.title;
        document.getElementById('algo-insight-text').textContent = insight.text;
    }

    const DEMO_SCENARIOS = {
        'north-south': { start: 'Hà Nội', end: 'Hồ Chí Minh', label: 'Hành trình Bắc - Nam' },
        'capital-central': { start: 'Hà Nội', end: 'Đà Nẵng', label: 'Thủ đô - miền Trung' },
        'mekong': { start: 'Cần Thơ', end: 'Cà Mau', label: 'Khám phá miền Tây' }
    };

    function applyScenario(event) {
        const scenario = DEMO_SCENARIOS[event.target.value];
        if (!scenario) return;

        clearSelection();
        setStartCity(scenario.start);
        setEndCity(scenario.end);
        showToast(`&#127891; Đã nạp kịch bản: ${scenario.label}`, 'success');
    }

    function createRandomRoute() {
        const cities = VietnamMap.getCityNames();
        if (cities.length < 2) return;

        const start = cities[Math.floor(Math.random() * cities.length)];
        let end = cities[Math.floor(Math.random() * cities.length)];
        while (end === start) end = cities[Math.floor(Math.random() * cities.length)];

        clearSelection();
        setStartCity(start);
        setEndCity(end);
        document.getElementById('scenario-select').value = '';
        showToast(`&#127922; Tuyến thử thách: ${start} → ${end}`, 'info');
    }

    async function loadHistory() {
        const list = document.getElementById('history-list');
        const summary = document.getElementById('history-summary');
        list.innerHTML = '<div class="history-empty">Đang tải lịch sử...</div>';

        try {
            const { history } = await AlgorithmsAPI.getHistory(8);
            summary.textContent = history.length
                ? `${history.length} lượt chạy gần nhất`
                : 'Chưa có lượt chạy được lưu';

            if (!history.length) {
                list.innerHTML = '<div class="history-empty">Kết quả tìm đường sẽ xuất hiện tại đây.</div>';
                return;
            }

            list.innerHTML = '';
            history.forEach(item => {
                const row = document.createElement('button');
                row.type = 'button';
                row.className = 'history-item';
                row.innerHTML = `
                    <span class="history-route">${item.start_city} <span>&rarr;</span> ${item.end_city}</span>
                    <span class="history-meta">${item.algorithm} &bull; ${Number(item.distance).toFixed(1)} km &bull; ${item.nodes_explored} node</span>
                `;
                row.addEventListener('click', () => {
                    clearSelection();
                    setStartCity(item.start_city);
                    setEndCity(item.end_city);
                    showToast(`&#128193; Đã nạp lại lượt chạy ${item.algorithm}`, 'info');
                });
                list.appendChild(row);
            });
        } catch (error) {
            list.innerHTML = '<div class="history-empty">Không tải được lịch sử truy vấn.</div>';
        }
    }

    /**
     * Xử lý click vào node trên bản đồ.
     */
    function handleNodeClick(cityName) {
        if (state.mode === 'obstacle' || state.mode === 'weight') return;

        if (!state.startCity) {
            // Chưa có điểm đi -> gán làm điểm đi
            setStartCity(cityName);
        } else if (cityName === state.startCity) {
            // Click trùng vào điểm đi hiện tại -> xóa lựa chọn để chọn lại từ đầu
            clearSelection();
        } else {
            // Đã có điểm đi và click vào tỉnh khác -> luôn gán/cập nhật làm điểm đích
            setEndCity(cityName);
        }
    }

    let hoverTimeout = null;

    /**
     * Xử lý hover vào node trên bản đồ (Real-time Hover Routing)
     */
    function handleNodeHover(cityName) {
        if (state.mode !== 'select' || state.isRunning) return;
        if (!state.startCity || state.startCity === cityName) return;
        if (state.endCity) return; // Nếu đã chốt đích thì không vẽ hover

        // Debounce API call để không spam server
        if (hoverTimeout) clearTimeout(hoverTimeout);
        hoverTimeout = setTimeout(async () => {
            const algorithm = document.getElementById('algorithm-select').value;
            const blockedEdges = VietnamMap.getBlockedEdges();
            try {
                const result = await AlgorithmsAPI.findPath(state.startCity, cityName, algorithm, blockedEdges);
                if (result.path && !state.endCity) {
                    VietnamMap.highlightPath(result.path); // Tạm thời vẽ đường đi
                }
            } catch (e) {
                // Ignore hover errors
            }
        }, 100);
    }

    /**
     * Xử lý khi chuột rời khỏi node
     */
    function handleNodeOut(cityName) {
        if (hoverTimeout) clearTimeout(hoverTimeout);
        if (!state.endCity && !state.isRunning) {
            VietnamMap.clearPath(); // Xóa đường đi tạm
        }
    }

    /**
     * Xử lý click vào edge trên bản đồ.
     */
    async function handleEdgeClick(fromCity, toCity, index, currentDistance) {
        if (state.mode === 'obstacle') {
            // Toggle block
            const currentEdges = VietnamMap.getBlockedEdges();
            const isBlocked = currentEdges.some(
                e => (e[0] === fromCity && e[1] === toCity) || (e[0] === toCity && e[1] === fromCity)
            );

            VietnamMap.toggleEdgeBlock(fromCity, toCity, !isBlocked);

            if (!isBlocked) {
                showToast(`🚧 Đã chặn: ${fromCity} ↔ ${toCity}`, 'info');
            } else {
                showToast(`✅ Đã mở: ${fromCity} ↔ ${toCity}`, 'success');
            }
        } else if (state.mode === 'weight') {
            const input = prompt(`Nhập khoảng cách mới (km) cho tuyến đường ${fromCity} - ${toCity}:\n(Hiện tại: ${currentDistance}km)`, currentDistance);
            
            if (input === null) return; // Bị hủy
            
            const newWeight = parseFloat(input);
            if (isNaN(newWeight) || newWeight <= 0) {
                showToast('⚠️ Khoảng cách phải là một số hợp lệ lớn hơn 0', 'error');
                return;
            }

            try {
                const res = await AlgorithmsAPI.updateEdgeWeight(fromCity, toCity, newWeight);
                VietnamMap.updateEdgeDistanceLabel(fromCity, toCity, newWeight);
                showToast(`✅ ${res.message}`, 'success');
            } catch (error) {
                showToast(`❌ Lỗi cập nhật: ${error.message}`, 'error');
            }
        }
    }

    /**
     * Set điểm xuất phát.
     */
    function setStartCity(cityName) {
        if (state.startCity) {
            VietnamMap.setNodeState(state.startCity, null);
        }
        state.startCity = cityName;
        VietnamMap.setNodeState(cityName, 'start');
        document.getElementById('start-select').value = cityName;
        updateToolbarStatus();
        updateButtons();
        showToast(`📍 Xuất phát: ${cityName}`, 'info');
    }

    /**
     * Set điểm đích.
     */
    function setEndCity(cityName) {
        if (state.endCity) {
            VietnamMap.setNodeState(state.endCity, null);
        }
        state.endCity = cityName;
        VietnamMap.setNodeState(cityName, 'end');
        document.getElementById('end-select').value = cityName;
        updateToolbarStatus();
        updateButtons();
        showToast(`🎯 Đích: ${cityName}`, 'info');
    }

    /**
     * Xóa selection.
     */
    function clearSelection() {
        if (state.startCity) VietnamMap.setNodeState(state.startCity, null);
        if (state.endCity) VietnamMap.setNodeState(state.endCity, null);
        state.startCity = null;
        state.endCity = null;
        document.getElementById('start-select').value = '';
        document.getElementById('end-select').value = '';
        updateToolbarStatus();
        updateButtons();
    }

    /**
     * Set chế độ tương tác.
     */
    function setMode(mode) {
        state.mode = mode;
        document.getElementById('btn-select-mode').classList.toggle('active', mode === 'select');
        document.getElementById('btn-obstacle-mode').classList.toggle('active', mode === 'obstacle');
        document.getElementById('btn-weight-mode').classList.toggle('active', mode === 'weight');
        updateToolbarStatus();
    }

    /**
     * Cập nhật trạng thái các nút bấm.
     */
    function updateButtons() {
        const hasStartEnd = state.startCity && state.endCity;
        document.getElementById('btn-find-path').disabled = !hasStartEnd || state.isRunning;
        document.getElementById('btn-step-mode').disabled = !hasStartEnd || state.isRunning;
        document.getElementById('btn-compare').disabled = !hasStartEnd || state.isRunning;
        document.getElementById('btn-dual-compare').disabled = !hasStartEnd || state.isRunning;
        document.getElementById('btn-clear-obstacles').disabled = state.isRunning;
        document.getElementById('btn-random-blocks').disabled = state.isRunning;
        document.getElementById('btn-reset-all').disabled = state.isRunning;
    }

    /**
     * Tạo chướng ngại vật ngẫu nhiên.
     */
    function generateRandomBlocks() {
        const availableEdges = VietnamMap.getAvailableEdges();
        const blockCount = Math.min(10, availableEdges.length);
        for (let index = 0; index < blockCount; index++) {
            const selectedIndex = Math.floor(Math.random() * availableEdges.length);
            const [edge] = availableEdges.splice(selectedIndex, 1);
            VietnamMap.toggleEdgeBlock(edge.from, edge.to, true);
        }
        showToast(`🎲 Đã chặn ngẫu nhiên ${blockCount} tuyến đường có thật trên bản đồ`, 'info');
    }

    /**
     * Toggle chế độ step-by-step.
     */
    function toggleStepMode() {
        state.isStepMode = !state.isStepMode;
        const btn = document.getElementById('btn-step-mode');
        btn.classList.toggle('active', state.isStepMode);
        btn.innerHTML = state.isStepMode ? '👣 Từng bước ✓' : '👣 Từng bước';
    }

    /**
     * Tìm đường - gọi API và hiển thị kết quả.
     */
    async function findPath() {
        if (!state.startCity || !state.endCity) {
            showToast('⚠️ Hãy chọn điểm xuất phát và điểm đích!', 'error');
            return;
        }

        const algorithm = document.getElementById('algorithm-select').value;
        const blockedEdges = VietnamMap.getBlockedEdges();

        state.isRunning = true;
        updateButtons();

        // Reset visualization
        Visualization.reset();
        resetMapTrace();
        VietnamMap.resetAllStates();
        VietnamMap.setNodeState(state.startCity, 'start');
        VietnamMap.setNodeState(state.endCity, 'end');

        showToast(`🔍 Đang tìm đường bằng ${getAlgoDisplayName(algorithm)}...`, 'info');

        try {
            const result = await AlgorithmsAPI.findPath(
                state.startCity, state.endCity, algorithm, blockedEdges
            );

            if (result.path && result.path.length > 0) {
                state.lastResult = result;
                startMapTrace(result, algorithm);
                // Cập nhật statistics
                updateStats(result);

                // Khởi tạo visualization
                const totalSteps = Visualization.init(result, {
                    onStepUpdate: (step, index, total) => {
                        document.getElementById('step-num').textContent = index + 1;
                        document.getElementById('step-current').textContent = step.current;
                        document.getElementById('step-cost').textContent = step.current_cost;
                        updateMapTraceStep(step, index, total);
                    },
                    onComplete: (path) => {
                        completeMapTrace(result);
                        showToast(`✅ Tìm thấy đường đi! ${result.cost} km, ${result.explored_count} node duyệt`, 'success');
                    }
                });

                if (state.isStepMode) {
                    // Chế độ từng bước - chờ user click
                    showToast(`👣 Chế độ từng bước: ${totalSteps} bước. Dùng nút điều khiển.`, 'info');
                } else {
                    // Chạy tự động
                    Visualization.play();
                }
                loadHistory();
            } else {
                showToast('❌ Không tìm được đường đi! Có thể do chướng ngại vật.', 'error');
                updateStats({ cost: -1, time_ms: result.time_ms, explored_count: result.explored_count, exploration_steps: result.exploration_steps });
            }

        } catch (error) {
            showToast(`❌ Lỗi: ${error.message}`, 'error');
        }

        state.isRunning = false;
        updateButtons();
    }

    /**
     * So sánh tất cả thuật toán.
     */
    async function compareAll() {
        if (!state.startCity || !state.endCity) {
            showToast('⚠️ Hãy chọn điểm xuất phát và điểm đích!', 'error');
            return;
        }

        const blockedEdges = VietnamMap.getBlockedEdges();

        showToast('📊 Đang so sánh 6 thuật toán...', 'info');

        try {
            const data = await AlgorithmsAPI.compareAlgorithms(
                state.startCity, state.endCity, blockedEdges
            );

            Comparison.show(data);
            showToast('✅ So sánh hoàn tất!', 'success');

        } catch (error) {
            showToast(`❌ Lỗi so sánh: ${error.message}`, 'error');
        }
    }

    /**
     * Xóa tất cả chướng ngại vật.
     */
    function clearObstacles() {
        VietnamMap.clearAllBlocks();
        showToast('🗑️ Đã xóa tất cả chướng ngại vật', 'success');
    }

    /**
     * Reset toàn bộ ứng dụng.
     */
    function resetAll() {
        Visualization.reset();
        resetMapTrace();
        clearSelection();
        Comparison.hide();
        resetStats();
        state.isStepMode = false;
        state.lastResult = null;
        document.getElementById('btn-step-mode').classList.remove('active');
        document.getElementById('btn-step-mode').innerHTML = '👣 Từng bước';
        document.getElementById('step-info').style.display = 'none';
        document.getElementById('run-report').style.display = 'none';
        showToast('↺ Đã reset tất cả', 'info');
    }

    /**
     * Tính năng Dual Compare (Đấu tay đôi 2 thuật toán)
     */
    async function dualCompare() {
        if (!state.startCity || !state.endCity) {
            showToast('⚠️ Hãy chọn điểm xuất phát và điểm đích!', 'error');
            return;
        }

        const algo1 = document.getElementById('algorithm-select').value;
        const algo2 = document.getElementById('dual-algo-2').value;
        
        if (algo1 === algo2) {
            showToast('⚠️ Bạn đang chọn 2 thuật toán giống nhau!', 'error');
            return;
        }

        const blockedEdges = VietnamMap.getBlockedEdges();
        state.isRunning = true;
        updateButtons();
        
        Visualization.reset();
        VietnamMap.resetAllStates();
        VietnamMap.setNodeState(state.startCity, 'start');
        VietnamMap.setNodeState(state.endCity, 'end');

        showToast(`⚔️ Đang so sánh ${getAlgoDisplayName(algo1)} vs ${getAlgoDisplayName(algo2)}...`, 'info');

        try {
            const [res1, res2] = await Promise.all([
                AlgorithmsAPI.findPath(state.startCity, state.endCity, algo1, blockedEdges),
                AlgorithmsAPI.findPath(state.startCity, state.endCity, algo2, blockedEdges)
            ]);

            if (res1.path && res2.path) {
                let runCount1 = 0;
                let runCount2 = 0;
                const MAX_RUNS = 3;

                function runAlgo2() {
                    if (runCount2 >= MAX_RUNS) {
                        showToast(`✅ Đã vẽ xong. Xanh: ${getAlgoDisplayName(algo2)}, Đỏ: ${getAlgoDisplayName(algo1)}`, 'success');
                        
                        // Hiển thị bảng và biểu đồ so sánh 2 thuật toán
                        const comparisonData = {
                            results: [
                                {
                                    algorithm: res1.algorithm || getAlgoDisplayName(algo1),
                                    type: res1.type || (algo1 === 'astar' || algo1 === 'greedy' ? 'informed' : 'blind'),
                                    path: res1.path || [],
                                    cost: res1.cost,
                                    explored_count: res1.explored_count || 0,
                                    steps_count: res1.exploration_steps ? res1.exploration_steps.length : 0,
                                    time_ms: res1.time_ms || 0
                                },
                                {
                                    algorithm: res2.algorithm || getAlgoDisplayName(algo2),
                                    type: res2.type || (algo2 === 'astar' || algo2 === 'greedy' ? 'informed' : 'blind'),
                                    path: res2.path || [],
                                    cost: res2.cost,
                                    explored_count: res2.explored_count || 0,
                                    steps_count: res2.exploration_steps ? res2.exploration_steps.length : 0,
                                    time_ms: res2.time_ms || 0
                                }
                            ]
                        };
                        Comparison.show(comparisonData);
                        
                        state.isRunning = false;
                        updateButtons();
                        return;
                    }
                    
                    runCount2++;
                    showToast(`⏳ Đang chạy ${getAlgoDisplayName(algo2)} (Lần ${runCount2}/${MAX_RUNS})...`, 'info');
                    
                    Visualization.init(res2, {
                        onStepUpdate: (step, index, total) => {
                            document.getElementById('step-num').textContent = index + 1;
                            document.getElementById('step-current').textContent = step.current;
                            document.getElementById('step-cost').textContent = step.current_cost;
                        },
                        onComplete: (path) => {
                            if (runCount2 < MAX_RUNS) {
                                setTimeout(runAlgo2, 1000); // Nghỉ 1s trước khi chạy lại
                            } else {
                                runAlgo2(); // Kết thúc
                            }
                        }
                    });
                    
                    // Vẽ lại đường đi thuật toán 1 làm nền (màu đỏ đứt nét) sau khi init đã clear map
                    VietnamMap.drawSecondaryPath(res1.path);
                    
                    if (!state.isStepMode) {
                        Visualization.play();
                    } else {
                        state.isRunning = true;
                        updateButtons();
                    }
                }

                function runAlgo1() {
                    if (runCount1 >= MAX_RUNS) {
                        showToast(`⏳ Đã xong thuật toán 1. Đợi 2.5s để xem kết quả thuật toán 2...`, 'info');
                        setTimeout(() => {
                            runAlgo2();
                        }, 2500);
                        return;
                    }
                    
                    runCount1++;
                    showToast(`▶️ Đang chạy ${getAlgoDisplayName(algo1)} (Lần ${runCount1}/${MAX_RUNS})...`, 'info');
                    
                    Visualization.init(res1, {
                        onStepUpdate: (step, index, total) => {
                            document.getElementById('step-num').textContent = index + 1;
                            document.getElementById('step-current').textContent = step.current;
                            document.getElementById('step-cost').textContent = step.current_cost;
                        },
                        onComplete: (path) => {
                            if (runCount1 < MAX_RUNS) {
                                setTimeout(runAlgo1, 1000); // Nghỉ 1s trước khi chạy lại
                            } else {
                                runAlgo1(); // Để chuyển sang bước tiếp theo
                            }
                        }
                    });

                    if (!state.isStepMode) {
                        Visualization.play();
                    } else {
                        state.isRunning = true;
                        updateButtons();
                    }
                }
                
                // Bắt đầu chạy thuật toán 1
                runAlgo1();

            } else {
                showToast('❌ Một trong 2 thuật toán không tìm được đường đi!', 'error');
                state.isRunning = false;
                updateButtons();
            }
        } catch (error) {
            showToast(`❌ Lỗi: ${error.message}`, 'error');
            state.isRunning = false;
            updateButtons();
        }
    }

    /**
     * Cập nhật statistics panel.
     */
    function updateStats(result) {
        const animateStat = (id, value) => {
            const el = document.getElementById(id);
            el.textContent = value;
            el.classList.add('updating');
            setTimeout(() => el.classList.remove('updating'), 300);
        };

        animateStat('stat-distance', result.cost > 0 ? result.cost : '∞');
        animateStat('stat-time', result.time_ms ? result.time_ms.toFixed(4) : '--');
        animateStat('stat-explored', result.explored_count || '--');
        animateStat('stat-steps', result.exploration_steps ? result.exploration_steps.length : '--');
        renderRunReport(result);
    }

    function startMapTrace(result, algorithm) {
        const trace = document.getElementById('map-trace');
        trace.classList.add('visible');
        document.getElementById('trace-state').textContent = getAlgoDisplayName(algorithm);
        document.getElementById('trace-current').textContent = 'Đang khởi tạo không gian tìm kiếm';
        document.getElementById('trace-step').textContent = `0 / ${(result.exploration_steps || []).length}`;
        document.getElementById('trace-frontier').textContent = '0';
        document.getElementById('trace-visited').textContent = '0';
        document.getElementById('trace-score-label').textContent = algorithm === 'astar' || algorithm === 'greedy' ? 'f(n)' : 'g(n)';
        document.getElementById('trace-score').textContent = '0 km';
    }

    function updateMapTraceStep(step, index, total) {
        document.getElementById('trace-current').textContent = `Đang mở rộng: ${step.current}`;
        document.getElementById('trace-step').textContent = `${index + 1} / ${total}`;
        document.getElementById('trace-frontier').textContent = step.frontier.length;
        document.getElementById('trace-visited').textContent = step.visited.length;
        const score = step.f_cost ?? step.current_cost;
        document.getElementById('trace-score').textContent = `${score} km`;
    }

    function completeMapTrace(result) {
        document.getElementById('trace-state').textContent = 'Đã tìm thấy';
        document.getElementById('trace-current').textContent = `Lộ trình tối ưu: ${result.path.length} điểm dừng`;
        document.getElementById('trace-score').textContent = `${result.cost} km`;
    }

    function resetMapTrace() {
        const trace = document.getElementById('map-trace');
        trace.classList.remove('visible');
        document.getElementById('trace-state').textContent = 'Sẵn sàng';
    }

    function renderRunReport(result) {
        const report = document.getElementById('run-report');
        const body = document.getElementById('run-report-body');
        const route = (result.path || []).join(' → ');
        const rows = [
            ['Thuật toán', result.algorithm || getAlgoDisplayName(document.getElementById('algorithm-select').value)],
            ['Tuyến đường', route],
            ['Khoảng cách', `${result.cost} km`],
            ['Thời gian TB', `${result.time_ms.toFixed(4)} ms`],
            ['Node đã duyệt', result.explored_count],
            ['Số bước', (result.exploration_steps || []).length]
        ];

        body.innerHTML = rows.map(([label, value]) => `<tr><th>${label}</th><td>${value}</td></tr>`).join('');
        report.style.display = 'block';
    }

    /**
     * Reset statistics.
     */
    function resetStats() {
        ['stat-distance', 'stat-time', 'stat-explored', 'stat-steps'].forEach(id => {
            document.getElementById(id).textContent = '--';
        });
    }

    /**
     * Populate city select dropdowns.
     */
    function populateCitySelects(cityNodes) {
        const startSelect = document.getElementById('start-select');
        const endSelect = document.getElementById('end-select');

        // Sắp xếp theo tên
        const sorted = [...cityNodes].sort((a, b) => a.name.localeCompare(b.name, 'vi'));

        sorted.forEach(city => {
            const opt1 = new Option(city.name, city.name);
            const opt2 = new Option(city.name, city.name);
            startSelect.appendChild(opt1);
            endSelect.appendChild(opt2);
        });
    }

    /**
     * Cập nhật trạng thái toolbar.
     */
    function updateToolbarStatus() {
        const status = document.getElementById('toolbar-status');
        if (state.mode === 'obstacle') {
            status.textContent = '🚧 Click vào đường để đặt/gỡ chướng ngại vật';
        } else if (state.mode === 'weight') {
            status.textContent = '✏️ Click vào đường để chỉnh sửa trọng số (km)';
        } else if (!state.startCity) {
            status.textContent = '📍 Nhấn vào tỉnh thành để chọn điểm xuất phát';
        } else if (!state.endCity) {
            status.textContent = '🎯 Nhấn vào tỉnh thành để chọn điểm đích';
        } else {
            status.textContent = `✅ ${state.startCity} → ${state.endCity} | Nhấn "Tìm đường" để bắt đầu`;
        }
    }

    // Removed duplicate updateButtons()

    /**
     * Cập nhật trạng thái kết nối.
     */
    function updateConnectionStatus(connected) {
        const badge = document.querySelector('.header-badge .dot');
        if (badge) {
            badge.style.background = connected ? 'var(--accent-emerald)' : 'var(--accent-rose)';
        }
        const label = badge?.nextElementSibling;
        if (label) {
            label.textContent = connected ? 'API Connected' : 'API Disconnected';
        }
    }

    /**
     * Lấy tên hiển thị cho thuật toán.
     */
    function getAlgoDisplayName(algo) {
        const names = {
            'astar': 'A* Search',
            'dijkstra': 'Dijkstra',
            'bfs': 'BFS',
            'dfs': 'DFS',
            'greedy': 'Greedy Best-First',
            'ucs': 'UCS'
        };
        return names[algo] || algo;
    }

    /**
     * Hiện toast notification.
     */
    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        container.innerHTML = ''; // Clear existing toasts to only show 1
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} toast-enter`;

        const icons = {
            'success': '✅',
            'error': '❌',
            'info': 'ℹ️'
        };

        toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
        container.appendChild(toast);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('toast-enter');
            toast.classList.add('toast-exit');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // ---- Initialize on DOM ready ----
    document.addEventListener('DOMContentLoaded', init);

    // Public API (for debugging)
    return {
        getState: () => ({ ...state }),
        showToast
    };
})();

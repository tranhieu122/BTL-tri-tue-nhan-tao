/**
 * comparison.js - Module so sánh thuật toán
 * Hiển thị bảng so sánh và biểu đồ bar chart.
 */

const Comparison = (() => {
    let comparisonData = null;

    // Màu sắc cho từng thuật toán
    const ALGO_COLORS = {
        'A*':       { bg: 'rgba(99, 102, 241, 0.7)',  border: '#6366f1' },
        'Greedy':   { bg: 'rgba(139, 92, 246, 0.7)',  border: '#8b5cf6' },
        'Dijkstra': { bg: 'rgba(34, 211, 238, 0.7)',  border: '#22d3ee' },
        'BFS':      { bg: 'rgba(249, 115, 22, 0.7)',  border: '#f97316' },
        'DFS':      { bg: 'rgba(244, 63, 94, 0.7)',   border: '#f43f5e' },
        'UCS':      { bg: 'rgba(245, 158, 11, 0.7)',  border: '#f59e0b' }
    };

    // Tên tiếng Việt cho type
    const TYPE_LABELS = {
        'informed': 'Có thông tin',
        'blind': 'Tìm kiếm mù'
    };

    /**
     * Hiển thị kết quả so sánh.
     */
    function show(data) {
        comparisonData = data.results || [];

        const section = document.getElementById('comparison-section');
        section.style.display = 'block';
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });

        renderTable();
        renderChart();
        generateAnalysis();
    }

    /**
     * Nhận xét & phân tích học thuật tự động.
     */
    function generateAnalysis() {
        const textEl = document.getElementById('comparison-analysis-text');
        if (!textEl) return;

        if (!comparisonData || comparisonData.length === 0) {
            textEl.innerHTML = 'Không có dữ liệu để phân tích.';
            return;
        }

        // Tìm các kết quả cụ thể
        const astar = comparisonData.find(r => r.algorithm === 'A*');
        const dijkstra = comparisonData.find(r => r.algorithm === 'Dijkstra');
        const bfs = comparisonData.find(r => r.algorithm === 'BFS');
        const dfs = comparisonData.find(r => r.algorithm === 'DFS');
        const greedy = comparisonData.find(r => r.algorithm === 'Greedy');
        const ucs = comparisonData.find(r => r.algorithm === 'UCS');

        let html = '<ul style="padding-left: 1.25rem; margin-top: 0.25rem; display: flex; flex-direction: column; gap: 0.45rem; list-style-type: disc;">';

        // 1. Phân tích về độ tối ưu đường đi (Optimality)
        const optimalCost = astar && astar.cost > 0 ? astar.cost : (dijkstra && dijkstra.cost > 0 ? dijkstra.cost : -1);
        if (optimalCost > 0) {
            html += `<li><strong>Độ tối ưu đường đi (Optimality):</strong> `;
            const optimalAlgos = comparisonData.filter(r => r.cost === optimalCost).map(r => r.algorithm);
            html += `Đường đi ngắn nhất tối ưu từ điểm đi tới điểm đến là <strong>${optimalCost} km</strong>. `;
            html += `Các thuật toán đảm bảo tính tối ưu (luôn tìm ra đúng độ dài này) gồm: <strong>${optimalAlgos.join(', ')}</strong>. `;
            
            let extra = [];
            if (greedy && greedy.cost > optimalCost) {
                extra.push(`<em>Greedy Best-First</em> chỉ tìm được đường dài <strong>${greedy.cost} km</strong> (lệch +${Math.round(greedy.cost - optimalCost)} km) do tính chất chỉ nhìn Heuristic cục bộ`);
            }
            if (bfs && bfs.cost > optimalCost) {
                extra.push(`<em>BFS</em> tìm được đường dài <strong>${bfs.cost} km</strong> do tối ưu số cạnh đi qua chứ không tối ưu theo khoảng cách thực tế`);
            }
            if (dfs && dfs.cost > optimalCost) {
                extra.push(`<em>DFS</em> đi vòng dài tới <strong>${dfs.cost} km</strong> vì duyệt ngẫu nhiên theo độ sâu mà không có bất kỳ ước lượng hay tối ưu nào`);
            }
            if (extra.length > 0) {
                html += `Trong khi đó, ` + extra.join('; ') + `.`;
            }
            html += `</li>`;
        }

        // 2. Phân tích về số lượng node duyệt và không gian tìm kiếm (Search Space)
        if (astar && dijkstra && astar.cost > 0 && dijkstra.cost > 0) {
            html += `<li><strong>Không gian tìm kiếm (Số node đã duyệt):</strong> `;
            html += `Thuật toán <strong>A*</strong> chỉ cần duyệt qua <strong>${astar.explored_count} tỉnh thành</strong>, trong khi <strong>Dijkstra</strong> phải duyệt tới <strong>${dijkstra.explored_count} tỉnh thành</strong> để tìm ra cùng một kết quả tối ưu. `;
            const reduction = Math.round((dijkstra.explored_count - astar.explored_count) / dijkstra.explored_count * 100);
            if (reduction > 0) {
                html += `Nhờ sử dụng hàm đánh giá Heuristic kết hợp khoảng cách thực tế <code>f(n) = g(n) + h(n)</code>, A* đã <strong>giảm được ${reduction}% số lượng node phải duyệt</strong> so với Dijkstra (vốn duyệt lan tỏa tròn không định hướng).`;
            } else {
                html += `Do khoảng cách giữa hai tỉnh rất gần, không gian tìm kiếm của hai thuật toán tương đối tương đương nhau.`;
            }
            html += `</li>`;
        }

        // 3. Phân tích thuật toán tham lam (Greedy Best-First)
        if (greedy && astar && greedy.cost > 0) {
            html += `<li><strong>Đánh giá Greedy Best-First Search:</strong> `;
            html += `Thuật toán này chỉ duyệt qua <strong>${greedy.explored_count} tỉnh thành</strong> (rất ít và nhanh), nhưng đường đi tìm được không tối ưu. Đây là ví dụ điển hình của việc đánh đổi giữa <em>tốc độ xử lý</em> và <em>chất lượng kết quả</em> trong Trí tuệ nhân tạo.</li>`;
        }

        // 4. Kết luận học thuật
        html += `<li><strong>Kết luận học thuật:</strong> `;
        html += `<strong>A* Search</strong> chứng minh được tính ưu việt tuyệt đối khi vừa thừa hưởng tính tối ưu (Complete &amp; Optimal) của Dijkstra/UCS, vừa có không gian tìm kiếm nhỏ gọn nhờ hàm Heuristic thông minh (Informed Search), tránh duyệt lan man các tỉnh nằm ngoài hướng đi.</li>`;

        html += '</ul>';
        textEl.innerHTML = html;
    }

    /**
     * Ẩn panel so sánh.
     */
    function hide() {
        document.getElementById('comparison-section').style.display = 'none';
    }

    /**
     * Render bảng so sánh.
     */
    function renderTable() {
        const tbody = document.getElementById('comparison-tbody');
        tbody.innerHTML = '';

        if (!comparisonData || comparisonData.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Không có dữ liệu</td></tr>';
            return;
        }

        // Tìm thuật toán tốt nhất (chi phí thấp nhất, có đường đi)
        const validResults = comparisonData.filter(r => r.cost > 0);
        const bestCost = validResults.length > 0
            ? Math.min(...validResults.map(r => r.cost))
            : -1;
        const fastestTime = validResults.length > 0
            ? Math.min(...validResults.map(r => r.time_ms))
            : -1;
        const leastExplored = validResults.length > 0
            ? Math.min(...validResults.map(r => r.explored_count))
            : -1;

        comparisonData.forEach(result => {
            const row = document.createElement('tr');
            const isBestCost = result.cost === bestCost && result.cost > 0;
            const isFastest = result.time_ms === fastestTime && result.cost > 0;
            const isLeastExplored = result.explored_count === leastExplored && result.cost > 0;

            if (isBestCost) row.classList.add('best-row');

            const typeClass = result.type === 'blind' ? 'badge-blind' : 'badge-informed';
            const typeLabel = TYPE_LABELS[result.type] || result.type;

            const pathStr = result.path && result.path.length > 0
                ? result.path.join(' → ')
                : 'Không tìm thấy';

            const costDisplay = result.cost > 0
                ? `${result.cost} ${isBestCost ? '⭐' : ''}`
                : '❌ N/A';

            const timeDisplay = result.cost > 0
                ? `${result.time_ms.toFixed(4)} ${isFastest ? '🚀' : ''}`
                : '❌ N/A';

            const exploredDisplay = `${result.explored_count} ${isLeastExplored && result.cost > 0 ? '✨' : ''}`;

            row.innerHTML = `
                <td><strong>${result.algorithm}</strong></td>
                <td><span class="algo-type-badge ${typeClass}">${typeLabel}</span></td>
                <td>${costDisplay}</td>
                <td>${timeDisplay}</td>
                <td>${exploredDisplay}</td>
                <td>${result.steps_count}</td>
                <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; font-size: 0.65rem; color: var(--text-muted);" title="${pathStr}">
                    ${pathStr}
                </td>
            `;

            tbody.appendChild(row);
        });
    }

    /**
     * Render biểu đồ bar chart so sánh.
     */
    function renderChart() {
        const canvas = document.getElementById('comparison-chart');
        const ctx = canvas.getContext('2d');

        // Set canvas size (high DPI)
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = 280 * dpr;
        canvas.style.width = rect.width + 'px';
        canvas.style.height = '280px';
        ctx.scale(dpr, dpr);

        const width = rect.width;
        const height = 280;

        // Clear
        ctx.clearRect(0, 0, width, height);

        if (!comparisonData || comparisonData.length === 0) return;

        const padding = { top: 30, right: 20, bottom: 55, left: 50 };
        const chartWidth = width - padding.left - padding.right;
        const chartHeight = height - padding.top - padding.bottom;

        const algorithms = comparisonData.map(r => r.algorithm);
        const exploredCounts = comparisonData.map(r => r.explored_count);
        const maxExplored = Math.max(...exploredCounts, 1);

        const barWidth = Math.min(chartWidth / algorithms.length * 0.6, 50);
        const barGap = chartWidth / algorithms.length;

        // Title
        ctx.fillStyle = '#9898b8';
        ctx.font = '11px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Số node đã duyệt (ít hơn = hiệu quả hơn)', width / 2, 15);

        // Y-axis gridlines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 1;
        const ySteps = 5;
        for (let i = 0; i <= ySteps; i++) {
            const y = padding.top + (chartHeight / ySteps) * i;
            ctx.beginPath();
            ctx.moveTo(padding.left, y);
            ctx.lineTo(width - padding.right, y);
            ctx.stroke();

            // Y labels
            const val = Math.round(maxExplored * (1 - i / ySteps));
            ctx.fillStyle = '#5a5a7a';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'right';
            ctx.fillText(val.toString(), padding.left - 8, y + 4);
        }

        // Draw bars
        algorithms.forEach((algo, i) => {
            const x = padding.left + barGap * i + (barGap - barWidth) / 2;
            const barHeight = (exploredCounts[i] / maxExplored) * chartHeight;
            const y = padding.top + chartHeight - barHeight;

            const colors = ALGO_COLORS[algo] || { bg: 'rgba(128, 128, 128, 0.7)', border: '#888' };

            // Bar gradient
            const gradient = ctx.createLinearGradient(x, y, x, y + barHeight);
            gradient.addColorStop(0, colors.border);
            gradient.addColorStop(1, colors.bg);

            // Draw bar with rounded top
            const radius = Math.min(4, barWidth / 2);
            ctx.beginPath();
            ctx.moveTo(x, y + barHeight);
            ctx.lineTo(x, y + radius);
            ctx.quadraticCurveTo(x, y, x + radius, y);
            ctx.lineTo(x + barWidth - radius, y);
            ctx.quadraticCurveTo(x + barWidth, y, x + barWidth, y + radius);
            ctx.lineTo(x + barWidth, y + barHeight);
            ctx.closePath();

            ctx.fillStyle = gradient;
            ctx.fill();

            // Border
            ctx.strokeStyle = colors.border;
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Glow effect
            ctx.shadowColor = colors.border;
            ctx.shadowBlur = 8;
            ctx.fill();
            ctx.shadowBlur = 0;

            // Value on top
            ctx.fillStyle = '#e8e8f0';
            ctx.font = 'bold 10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(exploredCounts[i].toString(), x + barWidth / 2, y - 6);

            // Algorithm name
            ctx.save();
            ctx.translate(x + barWidth / 2, padding.top + chartHeight + 12);
            ctx.rotate(-0.3);
            ctx.fillStyle = '#9898b8';
            ctx.font = '10px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(algo, 0, 0);
            ctx.restore();

            // Type badge
            const result = comparisonData[i];
            ctx.fillStyle = result.type === 'blind'
                ? 'rgba(249, 115, 22, 0.6)'
                : 'rgba(99, 102, 241, 0.6)';
            ctx.font = '8px Inter, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText(
                result.type === 'blind' ? 'Mù' : 'Có TT',
                x + barWidth / 2,
                padding.top + chartHeight + 38
            );
        });
    }

    /**
     * Lấy dữ liệu so sánh hiện tại.
     */
    function getData() {
        return comparisonData;
    }

    // Public API
    return {
        show,
        hide,
        renderChart,
        getData
    };
})();

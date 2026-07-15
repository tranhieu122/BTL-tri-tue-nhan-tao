/**
 * algorithms.js - Module gọi API backend
 * Xử lý giao tiếp REST API với Flask backend.
 */

const AlgorithmsAPI = (() => {
    // ---- Configuration ----
    const API_BASE = 'http://localhost:5000/api';

    /**
     * Gọi API lấy dữ liệu đồ thị.
     */
    async function fetchGraph() {
        try {
            const response = await fetch(`${API_BASE}/graph`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Lỗi lấy dữ liệu đồ thị:', error);
            throw error;
        }
    }

    /**
     * Gọi API tìm đường.
     * @param {string} start - Tên tỉnh xuất phát
     * @param {string} end - Tên tỉnh đích
     * @param {string} algorithm - Tên thuật toán
     * @param {Array} blockedEdges - Danh sách cạnh bị chặn
     */
    async function findPath(start, end, algorithm, blockedEdges = []) {
        try {
            const response = await fetch(`${API_BASE}/pathfind`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    start,
                    end,
                    algorithm,
                    blocked_edges: blockedEdges
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Lỗi tìm đường:', error);
            throw error;
        }
    }

    /**
     * Gọi API so sánh tất cả thuật toán.
     */
    async function compareAlgorithms(start, end, blockedEdges = []) {
        try {
            const response = await fetch(`${API_BASE}/compare`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    start,
                    end,
                    blocked_edges: blockedEdges
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Lỗi so sánh thuật toán:', error);
            throw error;
        }
    }

    /**
     * Phân tích các đoạn trọng yếu của lộ trình tối ưu.
     */
    async function getRouteInsights(start, end, blockedEdges = []) {
        try {
            const response = await fetch(`${API_BASE}/route-insights`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start, end, blocked_edges: blockedEdges })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Lỗi phân tích độ bền lộ trình:', error);
            throw error;
        }
    }

    /**
     * Gọi API quản lý chướng ngại vật.
     */
    async function manageObstacle(action, city1 = null, city2 = null) {
        try {
            const body = { action };
            if (city1) body.city1 = city1;
            if (city2) body.city2 = city2;

            const response = await fetch(`${API_BASE}/obstacles`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Lỗi quản lý chướng ngại vật:', error);
            throw error;
        }
    }

    /**
     * Gọi API lấy lịch sử.
     */
    async function getHistory(limit = 50) {
        try {
            const response = await fetch(`${API_BASE}/history?limit=${limit}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Lỗi lấy lịch sử:', error);
            throw error;
        }
    }

    /**
     * Gọi API cập nhật trọng số cạnh.
     */
    async function updateEdgeWeight(city1, city2, weight) {
        try {
            const response = await fetch(`${API_BASE}/edge/weight`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city1, city2, weight })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Lỗi cập nhật trọng số:', error);
            throw error;
        }
    }

    /**
     * Kiểm tra kết nối tới server.
     */
    async function checkConnection() {
        try {
            const response = await fetch(`${API_BASE}/cities`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    // Public API
    return {
        fetchGraph,
        findPath,
        compareAlgorithms,
        getRouteInsights,
        manageObstacle,
        getHistory,
        updateEdgeWeight,
        checkConnection
    };
})();

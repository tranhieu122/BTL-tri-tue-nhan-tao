/**
 * visualization.js - Module trực quan hóa từng bước thuật toán
 * Quản lý animation step-by-step và auto-play.
 */

const Visualization = (() => {
    // ---- State ----
    let explorationSteps = [];
    let currentStepIndex = -1;
    let isPlaying = false;
    let playTimer = null;
    let animationSpeed = 500; // ms
    let finalPath = [];
    let startCity = '';
    let endCity = '';
    let onStepUpdate = null;
    let onComplete = null;

    /**
     * Khởi tạo visualization với dữ liệu thuật toán.
     */
    function init(result, callbacks = {}) {
        stop();
        reset();

        explorationSteps = result.exploration_steps || [];
        finalPath = result.path || [];
        startCity = finalPath.length > 0 ? finalPath[0] : '';
        endCity = finalPath.length > 0 ? finalPath[finalPath.length - 1] : '';
        currentStepIndex = -1;

        onStepUpdate = callbacks.onStepUpdate || null;
        onComplete = callbacks.onComplete || null;

        // Cập nhật UI
        updateStepInfo();
        updateControls();

        return explorationSteps.length;
    }

    /**
     * Set tốc độ animation.
     */
    function setSpeed(speed) {
        animationSpeed = speed;
    }

    /**
     * Chạy bước tiếp theo.
     */
    function nextStep() {
        if (currentStepIndex >= explorationSteps.length - 1) {
            // Đã xong tất cả steps
            showFinalPath();
            return false;
        }

        currentStepIndex++;
        applyStep(currentStepIndex);
        updateStepInfo();
        updateControls();

        if (currentStepIndex === explorationSteps.length - 1) {
            // Step cuối cùng
            setTimeout(() => showFinalPath(), animationSpeed);
        }

        return true;
    }

    /**
     * Lùi về bước trước.
     */
    function prevStep() {
        if (currentStepIndex <= 0) return false;

        currentStepIndex--;

        // Re-render tất cả steps từ đầu đến current
        VietnamMap.resetAllStates();
        VietnamMap.setNodeState(startCity, 'start');
        VietnamMap.setNodeState(endCity, 'end');

        for (let i = 0; i <= currentStepIndex; i++) {
            applyStep(i, true);
        }

        updateStepInfo();
        updateControls();
        return true;
    }

    /**
     * Apply trạng thái visual cho một step.
     */
    function applyStep(stepIndex, skipAnimation = false) {
        const step = explorationSteps[stepIndex];
        if (!step) return;

        // Reset trạng thái từ step trước (trừ start/end)
        if (!skipAnimation && stepIndex > 0) {
            const prevStep = explorationSteps[stepIndex - 1];
            if (prevStep) {
                // Node trước đó chuyển thành visited
                VietnamMap.setNodeState(prevStep.current, 'visited');
            }
        }

        // Đặt trạng thái cho các node đã thăm
        step.visited.forEach(city => {
            if (city !== step.current && city !== startCity && city !== endCity) {
                VietnamMap.setNodeState(city, 'visited');
            }
        });

        // Đặt trạng thái cho frontier nodes
        step.frontier.forEach(city => {
            if (!step.visited.includes(city) && city !== startCity && city !== endCity) {
                VietnamMap.setNodeState(city, 'frontier');
            }
        });

        // Đặt trạng thái cho node hiện tại
        if (step.current !== startCity && step.current !== endCity) {
            VietnamMap.setNodeState(step.current, 'current');
        }

        // Đảm bảo start và end luôn giữ trạng thái
        VietnamMap.setNodeState(startCity, 'start');
        VietnamMap.setNodeState(endCity, 'end');

        // Highlight các edge trong current_path
        if (step.current_path && step.current_path.length > 1) {
            for (let i = 0; i < step.current_path.length - 1; i++) {
                VietnamMap.setEdgeState(
                    step.current_path[i], 
                    step.current_path[i + 1], 
                    'exploring'
                );
            }
        }

        // Callback
        if (onStepUpdate && !skipAnimation) {
            onStepUpdate(step, stepIndex, explorationSteps.length);
        }
    }

    /**
     * Hiển thị đường đi cuối cùng.
     */
    function showFinalPath() {
        stop();

        // Reset all states trước
        VietnamMap.resetAllStates();

        if (finalPath.length > 0) {
            // Đánh dấu start/end
            VietnamMap.setNodeState(startCity, 'start');
            VietnamMap.setNodeState(endCity, 'end');

            // Đánh dấu các node trên đường đi
            finalPath.forEach(city => {
                if (city !== startCity && city !== endCity) {
                    VietnamMap.setNodeState(city, 'in-path');
                }
            });

            // Đánh dấu các edge trên đường đi
            for (let i = 0; i < finalPath.length - 1; i++) {
                VietnamMap.setEdgeState(finalPath[i], finalPath[i + 1], 'in-path');
            }

            // Vẽ path animation
            VietnamMap.drawPath(finalPath);
        }

        updateControls();

        if (onComplete) {
            onComplete(finalPath);
        }
    }

    /**
     * Auto-play: chạy tự động từng bước.
     */
    function play() {
        if (isPlaying) return;
        isPlaying = true;
        updateControls();

        playTimer = setInterval(() => {
            const hasNext = nextStep();
            if (!hasNext) {
                stop();
            }
        }, animationSpeed);
    }

    /**
     * Tạm dừng auto-play.
     */
    function pause() {
        isPlaying = false;
        if (playTimer) {
            clearInterval(playTimer);
            playTimer = null;
        }
        updateControls();
    }

    /**
     * Dừng hoàn toàn.
     */
    function stop() {
        isPlaying = false;
        if (playTimer) {
            clearInterval(playTimer);
            playTimer = null;
        }
        updateControls();
    }

    /**
     * Toggle play/pause.
     */
    function togglePlay() {
        if (isPlaying) {
            pause();
        } else {
            play();
        }
    }

    /**
     * Reset visualization.
     */
    function reset() {
        stop();
        explorationSteps = [];
        currentStepIndex = -1;
        finalPath = [];
        VietnamMap.resetAllStates();
        updateStepInfo();
        updateControls();
    }

    /**
     * Cập nhật thông tin step hiện tại trên UI.
     */
    function updateStepInfo() {
        const stepInfo = document.getElementById('step-info');
        const stepNum = document.getElementById('step-num');
        const stepTotal = document.getElementById('step-total');
        const stepCurrent = document.getElementById('step-current');
        const stepCost = document.getElementById('step-cost');

        if (explorationSteps.length === 0) {
            stepInfo.style.display = 'none';
            return;
        }

        stepInfo.style.display = 'block';
        stepTotal.textContent = explorationSteps.length;

        if (currentStepIndex >= 0 && currentStepIndex < explorationSteps.length) {
            const step = explorationSteps[currentStepIndex];
            stepNum.textContent = currentStepIndex + 1;
            stepCurrent.textContent = step.current;
            stepCost.textContent = step.current_cost;
        } else {
            stepNum.textContent = '0';
            stepCurrent.textContent = '--';
            stepCost.textContent = '--';
        }
    }

    /**
     * Cập nhật trạng thái các nút điều khiển.
     */
    function updateControls() {
        const btnPrev = document.getElementById('btn-prev-step');
        const btnPlayPause = document.getElementById('btn-play-pause');
        const btnNext = document.getElementById('btn-next-step');
        const indicator = document.getElementById('running-indicator');

        const hasSteps = explorationSteps.length > 0;
        const atStart = currentStepIndex <= 0;
        const atEnd = currentStepIndex >= explorationSteps.length - 1;

        btnPrev.disabled = !hasSteps || atStart;
        btnNext.disabled = !hasSteps || atEnd;
        btnPlayPause.disabled = !hasSteps;

        if (isPlaying) {
            btnPlayPause.innerHTML = '⏸ Dừng';
            indicator.style.display = 'block';
        } else {
            btnPlayPause.innerHTML = atEnd ? '✅ Xong' : '▶️ Chạy';
            indicator.style.display = 'none';
        }
    }

    /**
     * Chạy nhanh - hiện kết quả ngay không animation.
     */
    function showResultInstantly() {
        stop();
        currentStepIndex = explorationSteps.length - 1;
        showFinalPath();
    }

    // Public API
    return {
        init,
        setSpeed,
        nextStep,
        prevStep,
        play,
        pause,
        stop,
        togglePlay,
        reset,
        showResultInstantly,
        showFinalPath,
        isPlaying: () => isPlaying,
        getCurrentStep: () => currentStepIndex,
        getTotalSteps: () => explorationSteps.length
    };
})();

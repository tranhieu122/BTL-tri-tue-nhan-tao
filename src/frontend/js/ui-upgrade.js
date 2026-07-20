/**
 * ui-upgrade.js
 * Extended interaction layer for upgraded index layout.
 */

(() => {
    const STORAGE_NOTE_KEY = 'vn_pathfinder_presenter_note';
    const STORAGE_ROWS_KEY = 'vn_pathfinder_notebook_rows';

    const refs = {
        palette: document.getElementById('command-palette'),
        paletteSearch: document.getElementById('command-search'),
        paletteList: document.getElementById('command-list'),
        notebookBody: document.getElementById('notebook-tbody'),
        noteTemplate: document.getElementById('tpl-note-row'),
        activityList: document.getElementById('activity-list'),
        presenterNote: document.getElementById('presenter-note'),
        checklistItems: Array.from(document.querySelectorAll('.checklist-item')),
        checklistProgress: document.getElementById('checklist-progress'),
        signalMode: document.getElementById('signal-mode'),
        signalLatency: document.getElementById('signal-latency'),
        signalFps: document.getElementById('signal-fps')
    };

    function init() {
        bindAccordion();
        bindStoryTabs();
        bindPalette();
        bindQuickActions();
        bindNotebook();
        bindPresenterNote();
        bindChecklist();
        bindActivityDock();
        bindSystemSignals();
        restoreNotebookRows();
        addActivity('UI upgrade module initialized.');
    }

    function bindAccordion() {
        document.querySelectorAll('.kb-toggle').forEach((toggle) => {
            toggle.addEventListener('click', () => {
                const item = toggle.closest('.kb-item');
                const expanded = toggle.getAttribute('aria-expanded') === 'true';
                if (!item) return;

                item.classList.toggle('open', !expanded);
                toggle.setAttribute('aria-expanded', String(!expanded));
            });
        });
    }

    function bindStoryTabs() {
        const tabs = Array.from(document.querySelectorAll('.story-tab'));
        const panels = Array.from(document.querySelectorAll('.story-panel'));

        tabs.forEach((tab) => {
            tab.addEventListener('click', () => {
                const targetId = tab.dataset.tab;
                tabs.forEach((t) => t.classList.remove('active'));
                panels.forEach((p) => p.classList.remove('active'));

                tab.classList.add('active');
                const target = document.getElementById(targetId);
                if (target) target.classList.add('active');
                addActivity(`Storyboard switched to ${tab.textContent.trim()}.`);
            });
        });
    }

    function bindPalette() {
        const openBtn = document.getElementById('btn-command-palette');
        const closeBtn = document.getElementById('btn-close-command');
        const backdrop = document.getElementById('command-backdrop');

        if (openBtn) openBtn.addEventListener('click', openPalette);
        if (closeBtn) closeBtn.addEventListener('click', closePalette);
        if (backdrop) backdrop.addEventListener('click', closePalette);

        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.key.toLowerCase() === 'k') {
                event.preventDefault();
                openPalette();
                return;
            }

            if (event.key === 'Escape' && refs.palette?.classList.contains('open')) {
                closePalette();
            }
        });

        refs.paletteSearch?.addEventListener('input', filterCommands);

        refs.paletteList?.addEventListener('click', (event) => {
            const command = event.target.closest('.command-item');
            if (!command) return;
            runCommand(command.dataset.command);
            closePalette();
        });
    }

    function openPalette() {
        if (!refs.palette) return;
        refs.palette.classList.add('open');
        refs.palette.setAttribute('aria-hidden', 'false');
        if (refs.paletteSearch) {
            refs.paletteSearch.value = '';
            filterCommands();
            setTimeout(() => refs.paletteSearch.focus(), 50);
        }
        addActivity('Command palette opened.');
    }

    function closePalette() {
        if (!refs.palette) return;
        refs.palette.classList.remove('open');
        refs.palette.setAttribute('aria-hidden', 'true');
    }

    function filterCommands() {
        const keyword = refs.paletteSearch?.value.trim().toLowerCase() || '';
        refs.paletteList?.querySelectorAll('.command-item').forEach((item) => {
            const text = item.textContent.toLowerCase();
            const visible = text.includes(keyword);
            item.style.display = visible ? '' : 'none';
        });
    }

    function runCommand(command) {
        const click = (id) => document.getElementById(id)?.click();

        switch (command) {
            case 'run-find':
                click('btn-find-path');
                addActivity('Command: run find path.');
                break;
            case 'run-compare':
                click('btn-compare');
                addActivity('Command: compare all algorithms.');
                break;
            case 'run-dual':
                click('btn-dual-compare');
                addActivity('Command: run dual compare.');
                break;
            case 'run-random':
                click('btn-random-route');
                addActivity('Command: generate random route.');
                break;
            case 'run-obstacles':
                click('btn-random-blocks');
                addActivity('Command: randomize obstacles.');
                break;
            case 'run-reset':
                click('btn-reset-all');
                addActivity('Command: reset all state.');
                break;
            case 'run-capture':
                captureCurrentStatsIntoNotebook();
                break;
            default:
                addActivity('Unknown command ignored.');
                break;
        }
    }

    function bindQuickActions() {
        document.getElementById('btn-quick-astar')?.addEventListener('click', () => {
            const select = document.getElementById('algorithm-select');
            if (select) {
                select.value = 'astar';
                select.dispatchEvent(new Event('change'));
                document.querySelector('.algo-card[data-algo="astar"]')?.click();
            }
            document.getElementById('btn-find-path')?.click();
            addActivity('Quick action: A* run requested.');
        });

        document.getElementById('btn-quick-dual')?.addEventListener('click', () => {
            document.getElementById('btn-dual-compare')?.click();
            addActivity('Quick action: Dual compare requested.');
        });

        document.getElementById('btn-quick-random')?.addEventListener('click', () => {
            document.getElementById('btn-random-route')?.click();
            setTimeout(() => document.getElementById('btn-find-path')?.click(), 120);
            addActivity('Quick action: random route and run requested.');
        });
    }

    function bindNotebook() {
        document.getElementById('btn-add-note-row')?.addEventListener('click', () => {
            addNotebookRow();
            addActivity('Notebook row added.');
        });

        document.getElementById('btn-clear-note-row')?.addEventListener('click', () => {
            if (!refs.notebookBody) return;
            refs.notebookBody.innerHTML = '';
            addNotebookRow();
            syncNotebookIndexes();
            persistNotebookRows();
            addActivity('Notebook reset.');
        });

        document.getElementById('btn-export-note-row')?.addEventListener('click', exportNotebookRows);

        refs.notebookBody?.addEventListener('click', (event) => {
            const button = event.target.closest('.danger-mini');
            if (!button) return;
            const row = button.closest('tr');
            if (!row) return;
            row.remove();
            syncNotebookIndexes();
            persistNotebookRows();
            addActivity('Notebook row removed.');
        });

        refs.notebookBody?.addEventListener('input', () => {
            persistNotebookRows();
        });
    }

    function addNotebookRow(prefill = null) {
        if (!refs.notebookBody || !refs.noteTemplate) return;
        const fragment = refs.noteTemplate.content.cloneNode(true);
        const row = fragment.querySelector('tr');
        if (!row) return;

        if (prefill) {
            const cells = row.querySelectorAll('td');
            if (cells[1]) cells[1].querySelector('input') ? cells[1].querySelector('input').value = prefill.scenario || '' : (cells[1].textContent = prefill.scenario || '');
            if (cells[2]) {
                const select = cells[2].querySelector('select');
                if (select) select.value = prefill.algorithm || 'A*';
            }
            if (cells[3]) {
                const input = cells[3].querySelector('input');
                if (input) input.value = prefill.cost || 0;
            }
            if (cells[4]) {
                const input = cells[4].querySelector('input');
                if (input) input.value = prefill.explored || 0;
            }
            if (cells[5]) {
                const input = cells[5].querySelector('input');
                if (input) input.value = prefill.time || 0;
            }
            if (cells[6]) {
                const input = cells[6].querySelector('input');
                if (input) input.value = prefill.comment || '';
            }
        }

        refs.notebookBody.appendChild(fragment);
        syncNotebookIndexes();
        persistNotebookRows();
    }

    function syncNotebookIndexes() {
        if (!refs.notebookBody) return;
        Array.from(refs.notebookBody.querySelectorAll('tr')).forEach((row, idx) => {
            const marker = row.querySelector('.row-index') || row.children[0];
            if (marker) marker.textContent = String(idx + 1);
        });
    }

    function serializeRows() {
        if (!refs.notebookBody) return [];
        return Array.from(refs.notebookBody.querySelectorAll('tr')).map((row) => {
            const getInput = (index) => row.children[index]?.querySelector('input, select');
            return {
                scenario: getInput(1)?.value || row.children[1]?.textContent.trim() || '',
                algorithm: getInput(2)?.value || row.children[2]?.textContent.trim() || 'A*',
                cost: Number(getInput(3)?.value || 0),
                explored: Number(getInput(4)?.value || 0),
                time: Number(getInput(5)?.value || 0),
                comment: getInput(6)?.value || ''
            };
        });
    }

    function persistNotebookRows() {
        localStorage.setItem(STORAGE_ROWS_KEY, JSON.stringify(serializeRows()));
    }

    function restoreNotebookRows() {
        if (!refs.notebookBody) return;
        const raw = localStorage.getItem(STORAGE_ROWS_KEY);
        if (!raw) return;

        try {
            const rows = JSON.parse(raw);
            if (!Array.isArray(rows) || !rows.length) return;
            refs.notebookBody.innerHTML = '';
            rows.forEach((item) => addNotebookRow(item));
            syncNotebookIndexes();
            addActivity(`Notebook restored: ${rows.length} row(s).`);
        } catch (error) {
            addActivity('Notebook restore failed, using defaults.');
        }
    }

    function exportNotebookRows() {
        const rows = serializeRows();
        const blob = new Blob([JSON.stringify(rows, null, 2)], { type: 'application/json;charset=utf-8' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'experiment-notebook.json';
        link.click();
        URL.revokeObjectURL(link.href);
        addActivity(`Notebook exported: ${rows.length} row(s).`);
    }

    function captureCurrentStatsIntoNotebook() {
        const algorithm = document.getElementById('algorithm-select')?.value || 'astar';
        const start = document.getElementById('start-select')?.value || 'Unknown';
        const end = document.getElementById('end-select')?.value || 'Unknown';
        const cost = parseFloat((document.getElementById('stat-distance')?.textContent || '0').replace(',', '.')) || 0;
        const explored = parseInt(document.getElementById('stat-explored')?.textContent || '0', 10) || 0;
        const time = parseFloat((document.getElementById('stat-time')?.textContent || '0').replace(',', '.')) || 0;

        addNotebookRow({
            scenario: `${start} -> ${end}`,
            algorithm: algorithm.toUpperCase(),
            cost,
            explored,
            time,
            comment: 'Auto capture from current dashboard state'
        });

        addActivity('Notebook auto-capture added from stats panel.');
    }

    function bindPresenterNote() {
        if (!refs.presenterNote) return;
        refs.presenterNote.value = localStorage.getItem(STORAGE_NOTE_KEY) || '';

        refs.presenterNote.addEventListener('input', () => {
            localStorage.setItem(STORAGE_NOTE_KEY, refs.presenterNote.value);
        });
    }

    function bindChecklist() {
        const update = () => {
            const checked = refs.checklistItems.filter((item) => item.checked).length;
            if (refs.checklistProgress) {
                refs.checklistProgress.textContent = `${checked}/${refs.checklistItems.length}`;
            }
        };

        refs.checklistItems.forEach((item) => item.addEventListener('change', update));
        update();
    }

    function bindActivityDock() {
        document.getElementById('btn-clear-activity')?.addEventListener('click', () => {
            if (!refs.activityList) return;
            refs.activityList.innerHTML = '<div class="activity-item">Activity đã được xóa.</div>';
        });
    }

    function addActivity(message) {
        if (!refs.activityList) return;
        const row = document.createElement('div');
        row.className = 'activity-item';

        const time = new Date();
        const stamp = `${String(time.getHours()).padStart(2, '0')}:${String(time.getMinutes()).padStart(2, '0')}:${String(time.getSeconds()).padStart(2, '0')}`;
        row.innerHTML = `<strong>${stamp}</strong> ${message}`;

        refs.activityList.prepend(row);
        while (refs.activityList.children.length > 18) {
            refs.activityList.lastElementChild?.remove();
        }
    }

    function bindSystemSignals() {
        setInterval(() => {
            const modeBtn = document.querySelector('.toolbar-btn.active');
            const modeText = modeBtn ? modeBtn.textContent.trim().toLowerCase() : 'select';
            if (refs.signalMode) refs.signalMode.textContent = modeText;

            const latency = 18 + Math.floor(Math.random() * 35);
            const fps = 48 + Math.floor(Math.random() * 11);
            if (refs.signalLatency) refs.signalLatency.textContent = `${latency} ms`;
            if (refs.signalFps) refs.signalFps.textContent = String(fps);

            animateMissionKpi();
        }, 1800);
    }

    function animateMissionKpi() {
        const keys = ['stability', 'coverage', 'heuristic'];
        keys.forEach((key) => {
            const valueNode = document.getElementById(`kpi-${key}`);
            const card = document.querySelector(`.mission-kpi[data-kpi="${key}"]`);
            if (!valueNode || !card) return;
            const meter = card.querySelector('.kpi-meter span');

            const base = Number(valueNode.textContent || 85);
            const next = Math.max(70, Math.min(99, base + (Math.random() > 0.5 ? 1 : -1)));
            valueNode.textContent = String(next);
            if (meter) meter.style.width = `${next}%`;
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

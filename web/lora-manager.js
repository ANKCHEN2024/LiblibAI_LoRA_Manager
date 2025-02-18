class LiblibAILoRAManager {
    constructor(app) {
        this.app = app;
        this.modelData = [];
        this.searchKeyword = "";
    }

    async init() {
        this.container = document.createElement('div');
        this.container.id = 'liblibai-lora-manager';
        
        // Search bar
        this.searchBar = this.createSearchBar();
        
        // Model grid
        this.modelGrid = document.createElement('div');
        this.modelGrid.className = 'model-grid';
        
        // Build UI
        this.container.appendChild(this.searchBar);
        this.container.appendChild(this.modelGrid);
        document.body.appendChild(this.container);

        // Load data
        await this.fetchModelData();
        this.renderUI();
    }

    createSearchBar() {
        const searchBar = document.createElement('div');
        searchBar.className = 'search-bar';
        
        this.searchInput = document.createElement('input');
        this.searchInput.placeholder = '🔍 Search models (name/tags)';
        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        
        searchBar.appendChild(this.searchInput);
        return searchBar;
    }

    async fetchModelData() {
        try {
            const response = await fetch('/lora_manager/list');
            this.modelData = await response.json();
        } catch (error) {
            console.error('[LiblibAI] Model load failed:', error);
        }
    }

    handleSearch(keyword) {
        this.searchKeyword = keyword.toLowerCase();
        this.renderUI();
    }

    renderUI() {
        this.modelGrid.innerHTML = '';
        
        const filteredModels = this.modelData.filter(model => {
            const matchName = model.display_name.toLowerCase().includes(this.searchKeyword);
            const matchTags = model.tags.some(tag => tag.includes(this.searchKeyword));
            return matchName || matchTags;
        });

        filteredModels.forEach(model => {
            const card = this.createModelCard(model);
            this.modelGrid.appendChild(card);
        });
    }

    createModelCard(model) {
        const card = document.createElement('div');
        card.className = 'model-card';
        card.dataset.modelName = model.internal_name;
        card.draggable = true;
        
        // Thumbnail
        const thumbnail = document.createElement('img');
        thumbnail.src = `/thumbnails/${model.internal_name}.jpg`;
        thumbnail.onerror = () => thumbnail.src = '/default_thumbnail.jpg';
        
        // Info panel
        const infoPanel = document.createElement('div');
        infoPanel.className = 'info-panel';
        infoPanel.innerHTML = `
            <h3>${model.display_name}</h3>
            <p class="description">${model.description || "No description"}</p>
            <div class="tag-container">
                ${model.tags.map(tag => `<span class="model-tag">${tag}</span>`).join('')}
            </div>
        `;

        // Drag event
        card.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', JSON.stringify({
                type: 'LORA_MODEL',
                name: model.internal_name,
                strength: 1.0
            }));
        });

        card.appendChild(thumbnail);
        card.appendChild(infoPanel);
        return card;
    }
}

app.registerPlugin({
    name: "LiblibAI LoRA Manager",
    icon: "📚",
    init(app) {
        const manager = new LiblibAILoRAManager(app);
        manager.init();
    }
});

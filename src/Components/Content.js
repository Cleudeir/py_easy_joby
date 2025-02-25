class Content extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `
        <div id="documentationContent" style="display: none;">
            <h2>Generated</h2>
            <div id="documentationOutput"></div>
        </div>
        <div class="loading-overlay" id="loadingOverlay">
            <div id="loading">Generation...</div>
        </div>     
        <my-floating-button></my-floating-button>   
        `;
    }
}

customElements.define('my-content', Content);
export default Content;
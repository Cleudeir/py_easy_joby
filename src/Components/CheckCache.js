class CheckCache extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `
            <div>
            <input type="checkbox" id="useCache" name="useCache" checked>
                Use cache
            </div>
        `;
    }
}

customElements.define('my-check-cache', CheckCache);
export default CheckCache;
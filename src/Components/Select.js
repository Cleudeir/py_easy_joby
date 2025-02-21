class MySelect extends HTMLElement {
    constructor() {
        super();
        this.render();
    }

    static get observedAttributes() {
        return ["options", "title"];
    }

    attributeChangedCallback() {
        this.render();
    }

    render() {
        const title = this.getAttribute("title") || "Select an option";
        const options = JSON.parse(this.getAttribute("options") || "[]");
        const id = this.getAttribute("myid");
        const onChange = this.getAttribute("onchange");
        const functionOnChange = window[onChange];

        this.innerHTML = `
            <label style="margin-top: 10px;" for="${id}">${title}</label>
            <select id="${id}" name="${id}" required ${onChange ? `onchange="${functionOnChange}"` : ""}>
                ${options.map(opt => `<option value="${opt.value}">${opt.label}</option>`).join("")}
            </select>
        `;

        this.selectElement = this.querySelector(`#${id}`);

        this.loadLastSelection();
        this.selectElement.addEventListener("change", this.saveSelection.bind(this));
    }

    loadLastSelection() {
        const lastSelection = localStorage.getItem("lastSplitMethod");
        if (lastSelection && this.selectElement.querySelector(`option[value="${lastSelection}"]`)) {
            this.selectElement.value = lastSelection;
        }
    }

    saveSelection() {
        localStorage.setItem("lastSplitMethod", this.selectElement.value);

        // Trigger external functions if they exist
        if (typeof toggleSplitValueInput === "function") {
            toggleSplitValueInput();
        }
        if (typeof saveFormData === "function") {
            saveFormData();
        }
    }
}

customElements.define('my-select', MySelect);
export default MySelect;

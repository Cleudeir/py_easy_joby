class MyInputText extends HTMLElement {
    constructor() {
        super();
        const label = this.getAttribute('label');
        const id = this.getAttribute('myid');
        this.innerHTML = `
            <label style="margin-top: 10px;" for="${id}">${label}</label>
            <input type="text" id="${id}" name="${id}">
        `;

        this.inputField = this.querySelector(`#${id}`);
        this.loadLastInput(id);
        this.inputField.addEventListener("input", () => this.saveInput(id));
    }
    loadLastInput(id) {
        const lastInput = localStorage.getItem(id);
        if (lastInput) {
            this.inputField.value = lastInput;
        }
    }
    saveInput(id) {
        localStorage.setItem(id, this.inputField.value);
    }
}

customElements.define('my-input-text', MyInputText);
export default MyInputText;

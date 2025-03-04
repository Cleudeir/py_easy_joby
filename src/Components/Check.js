class MyCheck extends HTMLElement {
    constructor() {
        super();
        this.label = this.getAttribute('label');
        this.myId = this.getAttribute('myId');
        this.innerHTML = `
            <div>
                <input type="checkbox" id="${this.myId}" name="${this.myId}" checked>
                ${this.label}             
            </div>
        `;
    }
}

customElements.define('my-check', MyCheck);
export default MyCheck;

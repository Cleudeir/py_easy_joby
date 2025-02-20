class InputFile extends HTMLElement {
    constructor() {
        super();
        this.innerHTML = `
            <label for="file">Choose a file:</label>
            <input type="file" id="file" name="file" required>
        `;
    }
}

customElements.define('my-input-file', InputFile);
export default InputFile;